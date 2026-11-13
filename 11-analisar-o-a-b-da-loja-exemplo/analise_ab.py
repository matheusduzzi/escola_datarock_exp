"""Funções do relatório de teste A/B da aula «Analisar o A/B da Loja Exemplo».

O relatorio.py usa estas funções na ordem do plano:
1. ler_plano: lê os campos do plano e para se falta algum ou se a data não vem antes do início;
2. ler_visitas: lê o arquivo do teste (uma linha por visita);
3. checar_execucao: tamanho do teste, visitas sem grupo e divisão dos grupos, antes do efeito;
4. efeito: taxas, diferença B menos A e intervalo pela aproximação normal;
5. decidir: aplica a regra escrita no plano ao intervalo.

Só pandas e a biblioteca padrão. O z do intervalo vem de statistics.NormalDist, que dá o mesmo
1,96 de scipy.stats.norm.ppf(0.975).
"""
import datetime as dt
import hashlib
import math
import re
from pathlib import Path
from statistics import NormalDist

import pandas as pd

CAMPOS = ['teste', 'combinado_em', 'inicio', 'dados', 'unidade', 'metrica', 'comparacao', 'minimo_pontos',
          'visitas_planejadas', 'sem_grupo_max_pct', 'linha_divisao', 'nivel', 'regra']
REGRAS = {
    'pior_caso': 'seguir se o limite de baixo do intervalo chega ao mínimo; não seguir se nem o limite de cima chega; '
                 'nos outros casos, os dados ainda não decidem',
    'estimativa': 'seguir se o intervalo fica todo acima de zero e a diferença chega ao mínimo; '
                  'nos outros casos, não seguir',
}


class ErroPlano(Exception):
    """O plano não permite analisar: falta campo, valor inválido ou data que não vem antes do início."""


class ParadaExecucao(Exception):
    """A execução saiu do plano: a análise para antes de calcular o efeito."""


def sha256(caminho):
    return hashlib.sha256(Path(caminho).read_bytes()).hexdigest()


def data_br(d):
    return d.strftime('%d/%m/%Y')


def virgula(texto):
    return texto.replace('.', ',')


def mil(n):
    return f'{n:,}'.replace(',', '.')


def ler_plano(caminho):
    """Lê as linhas `campo: valor` do bloco ```plano do arquivo e valida o que o relatório usa."""
    caminho = Path(caminho)
    texto = caminho.read_text(encoding='utf-8')
    m = re.search(r'```plano\n([\s\S]*?)\n```', texto)
    if not m:
        raise ErroPlano(f'{caminho.name} não tem o bloco ```plano com os campos')
    plano = {}
    for linha in m.group(1).splitlines():
        if not linha.strip():
            continue
        if ':' not in linha:
            raise ErroPlano(f'linha sem "campo: valor" no plano: {linha!r}')
        campo, valor = (p.strip() for p in linha.split(':', 1))
        plano[campo] = valor
    faltam = [c for c in CAMPOS if not plano.get(c)]
    if faltam:
        raise ErroPlano(f'faltam campos no plano: {", ".join(faltam)}')
    try:
        plano['combinado_em'] = dt.date.fromisoformat(plano['combinado_em'])
        plano['inicio'] = dt.date.fromisoformat(plano['inicio'])
    except ValueError as e:
        raise ErroPlano(f'data do plano fora do formato AAAA-MM-DD: {e}') from None
    if plano['combinado_em'] >= plano['inicio']:
        raise ErroPlano(f'o plano foi combinado em {data_br(plano["combinado_em"])}, que não vem antes do início do teste '
                        f'({data_br(plano["inicio"])}); um critério escrito depois não decide este teste')
    try:
        for campo in ('minimo_pontos', 'sem_grupo_max_pct', 'linha_divisao', 'nivel'):
            plano[campo] = float(plano[campo].replace(',', '.'))
        plano['visitas_planejadas'] = int(plano['visitas_planejadas'].replace('.', ''))
    except ValueError as e:
        raise ErroPlano(f'número inválido no plano: {e}') from None
    if plano['regra'] not in REGRAS:
        raise ErroPlano(f'regra desconhecida: {plano["regra"]} (use {" ou ".join(REGRAS)})')
    if not 0 < plano['nivel'] < 100:
        raise ErroPlano('o nível do intervalo vai entre 0 e 100')
    plano['dados'] = (caminho.parent / plano['dados']).resolve()
    plano['arquivo_plano'] = caminho
    return plano


def ler_visitas(caminho, metrica):
    v = pd.read_csv(caminho, dtype={'grupo': 'string'})
    for coluna in ('id_visita', 'grupo', metrica):
        if coluna not in v.columns:
            raise ParadaExecucao(f'o arquivo não tem a coluna {coluna}')
    if v['id_visita'].duplicated().any():
        raise ParadaExecucao(f'id_visita repetido em {int(v["id_visita"].duplicated().sum())} linhas')
    grupos = set(v['grupo'].dropna().unique())
    if not grupos <= {'A', 'B'}:
        raise ParadaExecucao(f'grupo diferente de A e B: {sorted(grupos - {"A", "B"})}')
    if not set(v[metrica].dropna().unique()) <= {0, 1} or v[metrica].isna().any():
        raise ParadaExecucao(f'a coluna {metrica} precisa ser 0 ou 1 em toda visita')
    return v


def teste_divisao(n_a, n_b):
    """Qui-quadrado da divisão meio a meio, com 1 grau de liberdade."""
    esperado = (n_a + n_b) / 2
    qui2 = ((n_a - esperado) ** 2 + (n_b - esperado) ** 2) / esperado
    return qui2, math.erfc(math.sqrt(qui2 / 2))


def checar_execucao(visitas, plano):
    total = len(visitas)
    sem_grupo = int(visitas['grupo'].isna().sum())
    n_a = int((visitas['grupo'] == 'A').sum())
    n_b = int((visitas['grupo'] == 'B').sum())
    qui2, p = teste_divisao(n_a, n_b)
    c = {'total': total, 'sem_grupo': sem_grupo, 'pct_sem_grupo': 100 * sem_grupo / total,
         'n_a': n_a, 'n_b': n_b, 'parte_a': n_a / (n_a + n_b), 'qui2': qui2, 'p_divisao': p, 'paradas': []}
    if total != plano['visitas_planejadas']:
        c['paradas'].append(f'o teste tem {mil(total)} visitas e o plano previa {mil(plano["visitas_planejadas"])}: '
                            'ele parou fora do tamanho combinado')
    if c['pct_sem_grupo'] > plano['sem_grupo_max_pct']:
        pct, lim = virgula(f'{c["pct_sem_grupo"]:.2f}'), virgula(f'{plano["sem_grupo_max_pct"]:g}')
        c['paradas'].append(f'{sem_grupo} visitas sem grupo ({pct}%), acima de {lim}% do plano')
    if p < plano['linha_divisao']:
        pv, linha = virgula(f'{p:.2g}'), virgula(f'{plano["linha_divisao"]:g}')
        c['paradas'].append(f'a divisão dos grupos deu p = {pv}, abaixo da linha de {linha}')
    return c


def efeito(visitas, plano):
    v = visitas.dropna(subset=['grupo'])
    a = v.loc[v['grupo'] == 'A', plano['metrica']]
    b = v.loc[v['grupo'] == 'B', plano['metrica']]
    taxa_a, taxa_b = float(a.mean()), float(b.mean())
    diferenca = taxa_b - taxa_a
    erro = math.sqrt(taxa_a * (1 - taxa_a) / len(a) + taxa_b * (1 - taxa_b) / len(b))
    z = NormalDist().inv_cdf(0.5 + plano['nivel'] / 200)
    return {'compras_a': int(a.sum()), 'compras_b': int(b.sum()), 'taxa_a': taxa_a, 'taxa_b': taxa_b,
            'diferenca': diferenca, 'inferior': diferenca - z * erro, 'superior': diferenca + z * erro, 'z': z}


def decidir(inferior, superior, diferenca, minimo, regra):
    """Retorna "seguir", "nao_seguir" ou "inconclusivo". O mínimo vem como fração (1 ponto = 0.01)."""
    if regra == 'pior_caso':
        if inferior >= minimo:
            return 'seguir'
        if superior < minimo:
            return 'nao_seguir'
        return 'inconclusivo'
    if regra == 'estimativa':
        return 'seguir' if inferior > 0 and diferenca >= minimo else 'nao_seguir'
    raise ValueError(f'regra desconhecida: {regra}')
