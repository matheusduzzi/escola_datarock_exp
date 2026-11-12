"""Contas do comitê de decisão: efeito, intervalo, regra do plano e o que um teste maior compra.

Uso, na pasta dessa aula do kit:

    python3 comite.py        mostra os três testes do dossiê, cada um pela regra do seu plano

No Python aberto nessa pasta:

    from comite import *

Só usa a biblioteca padrão (Python 3.9 ou mais novo). As hipóteses principais:
- o intervalo da diferença é o da aproximação normal, o mesmo de «Analisar o A/B da Loja
  Exemplo»: bom com centenas de casos em cada grupo;
- a chance de cada leitura de um teste futuro supõe que a taxa do grupo A e o efeito são os
  informados e que as visitas são independentes;
- o intervalo de Wilson do crédito é o de «Intervalo para proporção», do curso Estatística
  para decisão.
As taxas entram como fração (0.1014 para 10,14%). Os efeitos e os mínimos entram em pontos
percentuais (1 para 1 ponto).
"""
import csv
import math
import sys
from pathlib import Path
from statistics import NormalDist

Z95 = NormalDist().inv_cdf(0.975)
VISITAS_POR_DIA = 2100
PASTA = Path(__file__).resolve().parent


def _contagem(nome, sim, total):
    for rotulo, x in ((f'{nome}_sim', sim), (f'{nome}_total', total)):
        if not isinstance(x, int) or isinstance(x, bool):
            raise ValueError(f'{rotulo} precisa ser um número inteiro (veio {x!r})')
    if total < 1:
        raise ValueError(f'{nome}_total precisa ser maior que zero (veio {total})')
    if not 0 <= sim <= total:
        raise ValueError(f'{nome}_sim precisa estar entre 0 e {nome}_total (veio {sim} de {total})')


def _fracao(nome, x):
    if not isinstance(x, (int, float)) or isinstance(x, bool) or math.isnan(x) or not 0 < x < 1:
        raise ValueError(f'{nome} precisa ser uma fração entre 0 e 1 (veio {x}); use 0.1014 para 10,14%')


def diferenca(a_sim, a_total, b_sim, b_total, z=Z95):
    """B menos A, em pontos, com o intervalo de 95% da aproximação normal: (diferença, de, até)."""
    _contagem('a', a_sim, a_total)
    _contagem('b', b_sim, b_total)
    pa, pb = a_sim / a_total, b_sim / b_total
    erro = math.sqrt(pa * (1 - pa) / a_total + pb * (1 - pb) / b_total)
    d = pb - pa
    return 100 * d, 100 * (d - z * erro), 100 * (d + z * erro)


def leitura_pior_caso(de, ate, minimo):
    """Regra do botão e do frete: o pior caso plausível precisa pagar o mínimo."""
    if de >= minimo:
        return 'seguir'
    if ate < minimo:
        return 'não seguir'
    return 'não decide'


def leitura_estimativa(dif, de, ate, minimo):
    """Regra do contrato do «Retire hoje»: intervalo acima de zero e estimativa no mínimo."""
    if ate < 0:
        return 'piorou'
    if de <= 0:
        return 'não mostra efeito'
    if dif >= minimo:
        return 'paga o mínimo'
    return 'existe e não paga'


def protecao_barra(dif, de, limite):
    """Uma proteção barra quando a piora chega ao limite e o intervalo fica todo acima de zero."""
    return dif >= limite and de > 0


def visitas_por_grupo(semanas, visitas_por_dia=VISITAS_POR_DIA):
    """Visitas de cada grupo num teste meio a meio do checkout."""
    if not isinstance(semanas, (int, float)) or isinstance(semanas, bool) or semanas <= 0:
        raise ValueError(f'semanas precisa ser maior que zero (veio {semanas})')
    return int(visitas_por_dia * 7 * semanas / 2)


def meia_largura(n_por_grupo, taxa_a, efeito, z=Z95):
    """Metade da largura do intervalo de 95% da diferença, em pontos, com n_por_grupo em cada grupo."""
    _fracao('taxa_a', taxa_a)
    taxa_b = taxa_a + efeito / 100
    _fracao('taxa_a + efeito', taxa_b)
    if not isinstance(n_por_grupo, int) or n_por_grupo < 1:
        raise ValueError(f'n_por_grupo precisa ser um inteiro maior que zero (veio {n_por_grupo})')
    return 100 * z * math.sqrt((taxa_a * (1 - taxa_a) + taxa_b * (1 - taxa_b)) / n_por_grupo)


def chance_de_cada_leitura(n_por_grupo, taxa_a, efeito, minimo, z=Z95):
    """Chance de «seguir», «não decide» e «não seguir» pela regra do pior caso, num teste futuro.

    Supõe que o efeito verdadeiro é `efeito` pontos e que a diferença medida sai em volta dele,
    com o erro padrão de n_por_grupo visitas em cada grupo.
    """
    _fracao('taxa_a', taxa_a)
    taxa_b = taxa_a + efeito / 100
    _fracao('taxa_a + efeito', taxa_b)
    erro = meia_largura(n_por_grupo, taxa_a, efeito, z) / z
    medida = NormalDist(efeito, erro)
    seguir = 1 - medida.cdf(minimo + z * erro)
    nao_seguir = medida.cdf(minimo - z * erro)
    return {'seguir': seguir, 'não decide': 1 - seguir - nao_seguir, 'não seguir': nao_seguir}


def wilson(k, n, z=Z95):
    """Intervalo de Wilson para k casos em n (aula «Intervalo para proporção»)."""
    if not isinstance(n, int) or isinstance(n, bool) or n < 1:
        raise ValueError('n precisa ser um inteiro maior que zero')
    if not isinstance(k, int) or isinstance(k, bool) or not 0 <= k <= n:
        raise ValueError('k precisa ser um inteiro entre 0 e n')
    p = k / n
    centro = (p + z * z / (2 * n)) / (1 + z * z / n)
    meia = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return centro - meia, centro + meia


def empate(margem, lgd, valor):
    """Taxa de maus em que a margem paga a perda: margem ÷ (LGD × valor)."""
    for nome, x in (('margem', margem), ('valor', valor)):
        if not isinstance(x, (int, float)) or isinstance(x, bool) or x <= 0:
            raise ValueError(f'{nome} precisa ser maior que zero (veio {x})')
    _fracao('lgd', lgd)
    taxa = margem / (lgd * valor)
    if taxa >= 1:
        raise ValueError(f'com essa margem o empate passa de 100% ({taxa:.2f}): confira os valores')
    return taxa


def leitura_credito(maus, contratos, taxa_empate):
    """Regra do piloto de crédito: Wilson inteiro abaixo do empate, acima ou cruzando."""
    _fracao('taxa_empate', taxa_empate)
    de, ate = wilson(maus, contratos)
    if ate < taxa_empate:
        return 'vira política'
    if de > taxa_empate:
        return 'para'
    return 'reformula'


def br(x, casas=2):
    return f'{x:.{casas}f}'.replace('.', ',').replace('-', '−')


def ler_resultados(caminho=PASTA / 'resultados.csv'):
    linhas = []
    with open(caminho, encoding='utf-8', newline='') as f:
        for r in csv.DictReader(f):
            for campo in ('a_sim', 'a_total', 'b_sim', 'b_total'):
                r[campo] = int(r[campo])
            r['minimo_pontos'] = float(r['minimo_pontos'])
            linhas.append(r)
    return linhas


def ler_linha(teste, papel, linhas):
    achou = [r for r in linhas if r['teste'] == teste and r['papel'] == papel]
    if len(achou) != 1:
        raise ValueError(f'esperava uma linha de {teste}/{papel} em resultados.csv, achei {len(achou)}')
    return achou[0]


def main():
    linhas = ler_resultados()
    for r in linhas:
        dif, de, ate = diferenca(r['a_sim'], r['a_total'], r['b_sim'], r['b_total'])
        m = r['minimo_pontos']
        if r['regra'] == 'pior_caso':
            decide = leitura_pior_caso(de, ate, m)
        elif r['regra'] == 'estimativa':
            decide = leitura_estimativa(dif, de, ate, m)
        elif r['regra'] == 'protecao':
            decide = 'barra' if protecao_barra(dif, de, m) else 'dentro do limite'
        else:
            raise ValueError(f'regra desconhecida em resultados.csv: {r["regra"]}')
        print(f'{r["teste"]} | {r["metrica"]} | A {br(100 * r["a_sim"] / r["a_total"])}% '
              f'B {br(100 * r["b_sim"] / r["b_total"])}% | B - A {br(dif)} ponto, de {br(de)} a {br(ate)} '
              f'| mínimo {br(m, 0)} | {decide}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
