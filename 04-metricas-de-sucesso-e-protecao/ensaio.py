"""Roda o contrato de métricas do "Retire hoje" nos dados das 4 semanas ANTES do início.

Ninguém viu o "Retire hoje" nessas semanas. Então A e B têm que sair parecidos: se não saem,
o erro está no código da métrica ou na alocação, e não no teste. E os números de hoje servem
de base para o mínimo que paga a mudança e para os limites de proteção.

Uso: python3 ensaio.py [--ate AAAA-MM-DD]
  --ate  último dia do 1º gatilho que entra (padrão 2026-01-18)
"""
import argparse
import math
import sys

import pandas as pd

from metricas import br, ler, loja_por_dia, por_cliente, resumo

PRIMEIRO_DE, PRIMEIRO_ATE = '2026-01-05', '2026-01-18'


def main(argv=None):
    ap = argparse.ArgumentParser(description='Ensaio do contrato retire-hoje nos dados de antes do início.')
    ap.add_argument('--ate', default=PRIMEIRO_ATE, help='último dia do 1º gatilho que entra (AAAA-MM-DD)')
    args = ap.parse_args(argv)
    t = ler()
    try:
        tab = por_cliente(t, PRIMEIRO_DE, args.ate, janela=7, janela_reclamacao=14)
    except ValueError as erro:
        print(f'Erro: {erro}')
        return 1
    ate = pd.Timestamp(args.ate)
    s = resumo(tab)
    a, b = s.loc['A'], s.loc['B']
    print('Ensaio do contrato retire-hoje nas 4 semanas antes do início (05/01 a 01/02)')
    print(f'Clientes com o 1º gatilho de 05/01 a {ate:%d/%m} (as duas janelas cabem até 01/02)')
    print(f'                                     A          B')
    print(f'  clientes expostos           {br(a.clientes, 0):>9}  {br(b.clientes, 0):>9}')
    print(f'  compraram em 7 dias         {br(a.compraram, 0):>9}  {br(b.compraram, 0):>9}')
    print(f'  pedidos em 7 dias           {br(a.pedidos, 0):>9}  {br(b.pedidos, 0):>9}')
    print('Sucesso')
    print(f'  compra em 7 dias            {br(100 * a.compra_7d):>8}%  {br(100 * b.compra_7d):>8}%')
    print('Leitura (não decide)')
    print(f'  receita por cliente, 7 dias  R$ {br(a.receita_por_cliente, 2):>6}  R$ {br(b.receita_por_cliente, 2):>6}')
    print(f'  tíquete por pedido           R$ {br(a.ticket_por_pedido, 2):>6}  R$ {br(b.ticket_por_pedido, 2):>6}')
    print('Proteção do cliente')
    print(f'  reclamou da retirada, 14 dias {br(100 * a.reclamacao_14d):>6}%  {br(100 * b.reclamacao_14d):>8}%')
    loja = loja_por_dia(t)
    pior = loja.loc[loja['atraso'].idxmax()]
    sem = loja.groupby(loja['data'].dt.isocalendar().week)[['retiradas', 'retiradas_atrasadas', 'vendas_balcao']].sum()
    atraso_sem = sem['retiradas_atrasadas'] / sem['retiradas']
    acima = loja['atraso'] > 0.10
    seguidos = int((acima & acima.shift(fill_value=False)).sum())
    print('Proteção da loja, por dia (todas as retiradas, os dois grupos juntos)')
    print(f'  retiradas atrasadas: {br(100 * loja.retiradas_atrasadas.sum() / loja.retiradas.sum())}% nas 4 semanas, '
          f'pior dia {pior.data:%d/%m} com {br(100 * pior.atraso)}% '
          f'({int(pior.retiradas_atrasadas)} de {int(pior.retiradas)})')
    print(f'  retiradas atrasadas por semana: de {br(100 * atraso_sem.min())}% a {br(100 * atraso_sem.max())}%')
    print(f'  dias acima de 10%: {int(acima.sum())}; dois dias seguidos acima de 10%: {seguidos}')
    print(f'  vendas do balcão por semana: de R$ {br(sem.vendas_balcao.min(), 0)} a R$ {br(sem.vendas_balcao.max(), 0)}')
    p_junto = (a.compraram + b.compraram) / (a.clientes + b.clientes)
    erro = math.sqrt(p_junto * (1 - p_junto) * (1 / a.clientes + 1 / b.clientes))
    dif = b.compra_7d - a.compra_7d
    p = math.erfc(abs(dif) / erro / math.sqrt(2))
    print(f'Diferença B - A na compra em 7 dias, antes do início: {br(100 * dif)} pontos, p = {br(p, 2)}')
    if p < 0.001:
        print('Atenção: diferença grande demais para o acaso, sem ninguém ver o "Retire hoje". '
              'Veja o código da métrica e a alocação.')
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
