"""Relatório de um teste A/B a partir do plano combinado antes do início.

    python3 relatorio.py plano-botao.md
    python3 relatorio.py plano-botao.md --saida relatorio-botao.md

A ordem é a do plano: primeiro o que foi combinado, depois a execução, só então o efeito e a
decisão pela regra do plano. Se o plano não vale (campo faltando, data que não vem antes do início) ou se a
execução saiu do plano (tamanho, visitas sem grupo, divisão), o programa para antes do efeito e
sai com código 1. O mínimo e a regra só mudam no arquivo do plano, nunca na linha de comando.
"""
import argparse
import platform
import sys
from pathlib import Path

import pandas as pd

from analise_ab import REGRAS, ErroPlano, ParadaExecucao, checar_execucao, data_br, decidir, efeito, ler_plano
from analise_ab import ler_visitas, sha256

# A frase da decisão depende da regra do plano: cada regra explica com o critério que ela usa.
LEITURA = {
    'pior_caso': {
        'seguir': 'Seguir: o intervalo inteiro paga o mínimo de {m} ponto.',
        'nao_seguir': 'Não seguir: com o que o teste mostra, a mudança não paga o mínimo de {m} ponto.',
        'inconclusivo': 'Os dados ainda não decidem: o intervalo cruza o mínimo de {m} ponto.',
    },
    'estimativa': {
        'seguir': 'Seguir: o intervalo fica todo acima de zero e a diferença de {d} ponto chega ao mínimo de {m} ponto.',
        'nao_seguir_zero': 'Não seguir: o intervalo começa em {inf} ponto e não fica todo acima de zero.',
        'nao_seguir_minimo': 'Não seguir: a diferença de {d} ponto não chega ao mínimo de {m} ponto.',
    },
}


def leitura(decisao, plano, e):
    chave = decisao
    if plano['regra'] == 'estimativa' and decisao == 'nao_seguir':
        chave = 'nao_seguir_zero' if e['inferior'] <= 0 else 'nao_seguir_minimo'
    return LEITURA[plano['regra']][chave].format(m=num(plano['minimo_pontos']), d=br(100 * e['diferenca']),
                                                 inf=br(100 * e['inferior']))


def br(x, casas=2):
    return f'{x:.{casas}f}'.replace('.', ',')


def mil(n):
    return f'{n:,}'.replace(',', '.')


def num(x):
    return f'{x:g}'.replace('.', ',')


def p_br(p):
    return f'{p:.3g}'.replace('.', ',')


def montar(plano, visitas):
    linhas = [f'# Relatório do teste: {plano["teste"]}', '', '## 1. O plano, combinado antes do início', '',
              f'- Plano: {plano["arquivo_plano"].name}, combinado em {data_br(plano["combinado_em"])}; '
              f'início do teste em {data_br(plano["inicio"])}',
              f'- Unidade do sorteio: {plano["unidade"]}. Métrica: {plano["metrica"]}, 1 se a visita comprou',
              f'- Comparação: {plano["comparacao"]}',
              f'- Mínimo que paga a mudança: {num(plano["minimo_pontos"])} ponto',
              f'- Tamanho: {mil(plano["visitas_planejadas"])} visitas, um olhar no fim',
              f'- Regra ({plano["regra"]}): {REGRAS[plano["regra"]]}',
              f'- Intervalo de {num(plano["nivel"])}%, aproximação normal', '',
              '## 2. A execução, antes do efeito', '']
    c = checar_execucao(visitas, plano)
    linhas += [f'- Visitas no arquivo: {mil(c["total"])} de {mil(plano["visitas_planejadas"])} do plano',
               f'- Sem grupo: {c["sem_grupo"]} ({br(c["pct_sem_grupo"])}%), limite do plano '
               f'{num(plano["sem_grupo_max_pct"])}%; ficam fora da conta',
               f'- Divisão: A {mil(c["n_a"])}, B {mil(c["n_b"])} (A com {br(100 * c["parte_a"], 1)}%); '
               f'qui-quadrado {br(c["qui2"], 4)}, p = {p_br(c["p_divisao"])}; linha do plano '
               f'{num(plano["linha_divisao"])}']
    if c['paradas']:
        linhas += ['', '## 3. Parada', '', 'A execução saiu do plano. Nenhuma conta de efeito até descobrir o motivo:', '']
        linhas += [f'- {motivo}' for motivo in c['paradas']] + ['']
        return linhas, None
    linhas += ['- A execução seguiu o plano', '']
    e = efeito(visitas, plano)
    minimo = plano['minimo_pontos'] / 100
    decisao = decidir(e['inferior'], e['superior'], e['diferenca'], minimo, plano['regra'])
    linhas += ['## 3. O efeito', '',
               '| | A | B |', '|---|---|---|',
               f'| Visitas com grupo | {mil(c["n_a"])} | {mil(c["n_b"])} |',
               f'| Compras | {mil(e["compras_a"])} | {mil(e["compras_b"])} |',
               f'| Conversão | {br(100 * e["taxa_a"])}% | {br(100 * e["taxa_b"])}% |', '',
               f'- Diferença B menos A: {br(100 * e["diferenca"])} ponto',
               f'- Intervalo de {num(plano["nivel"])}%: {br(100 * e["inferior"])} a {br(100 * e["superior"])} ponto', '',
               '## 4. A decisão pela regra do plano', '',
               leitura(decisao, plano, e), '']
    return linhas, decisao


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('plano')
    ap.add_argument('--saida', help='grava o relatório neste arquivo')
    args = ap.parse_args(argv)
    try:
        plano = ler_plano(args.plano)
        visitas = ler_visitas(plano['dados'], plano['metrica'])
    except (ErroPlano, ParadaExecucao, FileNotFoundError) as e:
        print(f'Erro: {e}')
        return 1
    linhas, decisao = montar(plano, visitas)
    linhas += ['## 5. Para refazer' if decisao else '## 4. Para refazer', '',
               f'- Comando: python3 relatorio.py {Path(args.plano).name}',
               f'- Dados: {plano["dados"].name}, SHA-256 {sha256(plano["dados"])}',
               f'- Plano: {plano["arquivo_plano"].name}, SHA-256 {sha256(plano["arquivo_plano"])}',
               f'- Python {platform.python_version()}, pandas {pd.__version__}']
    texto = '\n'.join(linhas) + '\n'
    if args.saida:
        Path(args.saida).write_text(texto, encoding='utf-8')
        print(f'relatório gravado em {args.saida}')
    else:
        print(texto, end='')
    return 0 if decisao else 1


if __name__ == '__main__':
    sys.exit(main())
