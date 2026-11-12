"""Quanto a métrica varia: a compra em 7 dias contra a receita por conta, nos dados da aula anterior.

Uso:
    python3 variacao.py           a compra e a receita
    python3 variacao.py --todas   e também as 9.000 contas inteiras no denominador

Usa os dados e o metricas.py da pasta da aula «Métricas de sucesso e proteção»
(../04-metricas-de-sucesso-e-protecao/), que vêm no mesmo kit. Nada é gravado lá.
"""
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
AULA4 = AQUI.parent / '04-metricas-de-sucesso-e-protecao'
sys.path.insert(0, str(AQUI))
sys.path.insert(1, str(AULA4))

import pandas as pd  # noqa: E402
from cenarios import mde_proporcao, n_media, n_proporcao  # noqa: E402

BASE, MINIMO = 0.32, 0.02  # a base e o mínimo do plano


def br(x, casas=0):
    return f'{x:,.{casas}f}'.replace(',', '_').replace('.', ',').replace('_', '.')


def main(args):
    if not (AULA4 / 'metricas.py').is_file():
        raise FileNotFoundError(f'não achei {AULA4.name}/metricas.py: rode de dentro do kit do curso, '
                                'com a pasta da aula 04 ao lado desta')
    from metricas import ler, por_cliente
    t = ler()
    tab = por_cliente(t, '2026-01-05', '2026-01-18')
    compra, receita = tab['comprou'], tab['receita']
    print(f'Contas do ensaio da aula anterior (1º gatilho de 05/01 a 18/01): {br(len(tab))}')
    print(f'{"por conta, em 7 dias":<22}{"média":>10}{"desvio":>11}{"desvio/média":>14}')
    print(f'{"compra (0 ou 1)":<22}{br(100 * compra.mean(), 1) + "%":>10}{br(compra.std(), 3):>11}'
          f'{br(compra.std() / compra.mean(), 2):>14}')
    print(f'{"receita":<22}{"R$ " + br(receita.mean(), 2):>10}{"R$ " + br(receita.std(), 2):>11}'
          f'{br(receita.std() / receita.mean(), 2):>14}')

    relativo = MINIMO / BASE
    n_compra = n_proporcao(BASE, MINIMO)
    efeito_receita = relativo * receita.mean()
    n_receita = n_media(efeito_receita, receita.std())
    print()
    print(f'Contas por grupo para ver {br(100 * relativo, 2)}% a mais (2 pontos sobre 32%):')
    print(f'  compra:  {br(n_compra):>6}')
    print(f'  receita: {br(n_receita):>6}  (R$ {br(efeito_receita, 2)} a mais por conta; '
          f'{br(n_receita / n_compra, 1)} vezes a compra)')

    if '--todas' not in args:
        return 0
    # E se o denominador fossem as 9.000 contas do sorteio, sem gatilho?
    aloc = t['alocacao']
    ped = t['pedidos']
    no_periodo = ped[ped['id_cliente'].isin(aloc['id_cliente'])]
    base_todas = no_periodo['id_cliente'].nunique() / len(aloc)
    chegaram = t['gatilhos'].merge(aloc, on='id_cliente')['id_cliente'].nunique()
    diluido = MINIMO * chegaram / len(aloc)
    mde_todas = mde_proporcao(len(aloc) // 2, base_todas)
    print()
    print('Se o denominador fossem as 9.000 contas, nas mesmas 4 semanas:')
    print(f'  chegaram ao gatilho: {br(chegaram)} de {br(len(aloc))} ({br(100 * chegaram / len(aloc), 1)}%)')
    print(f'  compraram alguma vez: {br(100 * base_todas, 1)}%')
    print(f'  os 2 pontos de quem chega ao gatilho viram {br(100 * diluido, 2)} ponto nas 9.000')
    print(f'  com {br(len(aloc) // 2)} por grupo, o teste vê a partir de {br(100 * mde_todas, 1)} pontos')
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main(sys.argv[1:]))
    except (ValueError, FileNotFoundError) as erro:
        print(f'Erro: {erro}')
        sys.exit(1)
