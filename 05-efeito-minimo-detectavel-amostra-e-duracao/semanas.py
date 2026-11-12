"""O calendário no histórico de 2025: dia da semana, Carnaval e as semanas fora do normal.

Uso:
    python3 semanas.py

Lê dados/gatilho_por_dia_2025.csv. Semana é de segunda a domingo. Semana comum é a que não tem
nenhum dia com evento no calendário.
"""
import sys
from pathlib import Path

import pandas as pd

AQUI = Path(__file__).resolve().parent
DIAS = ['segunda', 'terça', 'quarta', 'quinta', 'sexta', 'sábado', 'domingo']


def ler(caminho=AQUI / 'dados' / 'gatilho_por_dia_2025.csv'):
    h = pd.read_csv(caminho, keep_default_na=False)
    h['data'] = pd.to_datetime(h['data'], format='%Y-%m-%d')
    if h['data'].duplicated().any():
        raise ValueError('o mesmo dia aparece duas vezes no histórico')
    if (h['compraram_7d'] > h['contas_no_gatilho']).any():
        raise ValueError('dia com mais compras do que contas no gatilho')
    if h['data'].min().weekday() != 0 or len(h) % 7:
        raise ValueError('o histórico precisa começar numa segunda e ter semanas inteiras')
    h['semana'] = h['data'] - pd.to_timedelta(h['data'].dt.weekday, unit='D')
    h['dia'] = h['data'].dt.weekday
    com_evento = set(h.loc[h['evento'] != '', 'semana'])
    h['comum'] = ~h['semana'].isin(com_evento)
    return h


def por_semana(h):
    s = h.groupby('semana').agg(contas=('contas_no_gatilho', 'sum'), compraram=('compraram_7d', 'sum'),
                                comum=('comum', 'first'),
                                evento=('evento', lambda e: ', '.join(dict.fromkeys(x for x in e if x))))
    s['compra'] = s['compraram'] / s['contas']
    return s


def pct(x, casas=1):
    return f'{100 * x:.{casas}f}%'.replace('.', ',')


def mil(x):
    return f'{x:,.0f}'.replace(',', '.')


def main():
    h = ler()
    s = por_semana(h)
    comum = h[h['comum']]
    n_comuns = int(s['comum'].sum())

    print(f'Por dia da semana, nas {n_comuns} semanas comuns de 2025')
    print(f'{"dia":<10}{"contas por dia":>15}{"parte da semana":>17}{"compra em 7 dias":>18}')
    d = comum.groupby('dia').agg(contas=('contas_no_gatilho', 'sum'), compraram=('compraram_7d', 'sum'),
                                 dias=('data', 'count'))
    for i, linha in d.iterrows():
        print(f'{DIAS[i]:<10}{mil(linha.contas / linha.dias):>15}{pct(linha.contas / d.contas.sum()):>17}'
              f'{pct(linha.compraram / linha.contas):>18}')
    print(f'{"semana":<10}{mil(d.contas.sum() / n_comuns):>15}{"100,0%":>17}{pct(d.compraram.sum() / d.contas.sum()):>18}')

    # Um teste de 15 dias que começa numa segunda tem 3 segundas e 2 de cada outro dia.
    peso15 = d.contas / d.dias * [3, 2, 2, 2, 2, 2, 2]
    print()
    print('Teste que começa numa segunda: quanto a segunda pesa nas contas')
    print(f'  14 ou 21 dias (semanas inteiras): {pct(d.contas[0] / d.contas.sum())}')
    print(f'  15 dias (3 segundas, 2 sábados):  {pct(peso15[0] / peso15.sum())}')

    carnaval = h.loc[h['evento'] == 'Carnaval', 'semana'].iloc[0]
    comuns = s[s['comum']]
    antes = comuns[comuns.index < carnaval].tail(4)
    depois = comuns[comuns.index > carnaval].head(4)
    print()
    print(f'Carnaval de 2025 (segunda e terça, {h.loc[h["evento"] == "Carnaval", "data"].dt.strftime("%d/%m").str.cat(sep=" e ")})')
    print(f'{"":<24}{"contas por semana":>19}{"compra":>9}')
    for nome, bloco in (('4 semanas comuns antes', antes), ('semana do Carnaval', s.loc[[carnaval]]),
                        ('4 semanas comuns depois', depois)):
        print(f'{nome:<24}{mil(bloco.contas.mean()):>19}{pct(bloco.compraram.sum() / bloco.contas.sum()):>9}')

    mediana = comuns['contas'].median()
    fora = s.assign(desvio=s['contas'] / mediana - 1).reindex(
        (s['contas'] / mediana - 1).abs().sort_values(ascending=False).index).head(6)
    print()
    print(f'As 6 semanas mais longe da semana comum típica ({mil(mediana)} contas)')
    print(f'{"semana":<8}{"contas":>7}{"diferença":>11}{"compra":>8}  evento')
    for semana, linha in fora.iterrows():
        sinal = '+' if linha.desvio > 0 else '-'
        print(f'{semana:%d/%m}{mil(linha.contas):>9}{sinal + pct(abs(linha.desvio), 0):>11}'
              f'{pct(linha.compra):>8}  {linha.evento or "sem evento"}')
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (ValueError, FileNotFoundError) as erro:
        print(f'Erro: {erro}')
        sys.exit(1)
