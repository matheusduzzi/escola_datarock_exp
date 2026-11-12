"""Compara duas janelas para a mesma compra, por semana do primeiro gatilho.

"Até o fim dos dados": conta toda compra do gatilho até 01/02, o último dia dos dados.
"Em 7 dias": conta a compra do dia do gatilho e dos 6 seguintes, igual para todo cliente.

Uso: python3 janelas.py
"""
import pandas as pd

from metricas import br, ler, por_cliente

SEMANAS = [('2026-01-05', '2026-01-11'), ('2026-01-12', '2026-01-18'),
           ('2026-01-19', '2026-01-25'), ('2026-01-26', '2026-02-01')]


def main():
    t = ler()
    print('Semana do 1º gatilho   clientes   até 01/02   em 7 dias')
    for de, ate in SEMANAS:
        aberta = por_cliente(t, de, ate, janela=None, janela_reclamacao=1)
        n = len(aberta)
        try:
            sete = por_cliente(t, de, ate, janela=7, janela_reclamacao=1)
            txt7 = f'{br(100 * sete.comprou.mean()):>8}%'
        except ValueError:
            txt7 = '  não cabe'
        rot = f'{pd.Timestamp(de):%d/%m} a {pd.Timestamp(ate):%d/%m}'
        print(f'{rot:<20} {br(n, 0):>9}   {br(100 * aberta.comprou.mean()):>8}%  {txt7}')


if __name__ == '__main__':
    main()
