"""Gera o histórico de 2025 do gatilho do "Retire hoje" no site da Loja Exemplo, um dia por linha.

Como os dados nascem (abra depois de fazer as contas da aula):

- 52 semanas, de segunda, 06/01/2025, a domingo, 04/01/2026. Uma linha por dia.
- contas_no_gatilho: contas que chegaram, naquele dia, à escolha da entrega com um produto em
  estoque na loja física. É o site todo, não só as 9.000 contas do teste. A mesma conta pode
  aparecer em dias diferentes.
- compraram_7d: dessas contas, quantas fizeram um pedido do dia até 6 dias depois.
- Num dia comum, perto de 270 contas chegam ao gatilho. A segunda tem mais gente e o sábado
  menos: o peso de cada dia está em PESO_CONTAS. Quem chega no sábado compra mais (quer a peça
  para o fim de semana): a chance de cada dia está em COMPRA.
- Feriado nacional tira 30% das contas do dia. Na segunda e na terça de Carnaval a loja física
  abre só de manhã e sai 45%; a Quarta-feira de Cinzas tira 15%.
- A semana antes do Dia das Mães tem 30% mais contas e 3 pontos a mais de compra. A semana da
  Black Friday da loja tem 90% mais contas e 6 pontos a mais. De 08/12 a 23/12, a temporada de
  Natal tem 30% mais contas. Véspera de Natal e de Ano Novo, Natal e 1º de janeiro, bem menos.
- A coluna evento só marca o calendário (o nome do dia), não o efeito.

Supõe, e uma loja de verdade não garante: o mesmo padrão de semana o ano todo, sem tendência
de crescimento e sem promoção fora das datas acima. Só usa a biblioteca padrão e
Random.random(), cuja sequência o Python garante entre versões; a saída é igual toda vez.
"""
import csv
import random
from datetime import date, timedelta
from pathlib import Path

AQUI = Path(__file__).resolve().parent
DADOS = AQUI / 'dados'
INICIO = date(2025, 1, 6)
DIAS = 364
MEDIA = 270
PESO_CONTAS = [1.18, 1.10, 1.04, 1.00, 0.90, 0.80, 0.98]  # segunda a domingo
COMPRA = [0.29, 0.30, 0.31, 0.31, 0.33, 0.37, 0.34]

FERIADOS = {
    date(2025, 4, 18): 'Paixão de Cristo', date(2025, 4, 21): 'Tiradentes', date(2025, 5, 1): 'Dia do Trabalho',
    date(2025, 9, 7): 'Independência', date(2025, 10, 12): 'Nossa Senhora Aparecida', date(2025, 11, 2): 'Finados',
    date(2025, 11, 15): 'Proclamação da República', date(2025, 11, 20): 'Consciência Negra',
}
OUTROS = {
    date(2025, 3, 3): ('Carnaval', 0.55, 0.0), date(2025, 3, 4): ('Carnaval', 0.55, 0.0),
    date(2025, 3, 5): ('Cinzas', 0.85, 0.0), date(2025, 4, 20): ('Páscoa', 0.90, 0.0),
    date(2025, 6, 19): ('Corpus Christi', 0.85, 0.0), date(2025, 5, 11): ('Dia das Mães', 0.90, 0.0),
    date(2025, 11, 28): ('Black Friday da loja', 1.0, 0.0), date(2025, 12, 24): ('véspera de Natal', 0.60, 0.0),
    date(2025, 12, 25): ('Natal', 0.40, 0.0), date(2025, 12, 31): ('véspera de Ano Novo', 0.50, 0.0),
    date(2026, 1, 1): ('Ano Novo', 0.45, 0.0),
}


def binomial(r, n, p):
    return sum(1 for _ in range(n) if r.random() < p)


def efeito(d):
    """Multiplicador das contas, pontos a mais de compra e o nome do evento do dia."""
    mult, mais, evento = 1.0, 0.0, ''
    if d in FERIADOS:
        mult, evento = 0.70, FERIADOS[d]
    if d in OUTROS:
        evento, m, mais = OUTROS[d]
        mult *= m
    if date(2025, 5, 5) <= d <= date(2025, 5, 10):
        mult, mais = mult * 1.30, mais + 0.03
    if date(2025, 11, 24) <= d <= date(2025, 11, 30):
        mult, mais = mult * 1.90, mais + 0.06
    if date(2025, 12, 8) <= d <= date(2025, 12, 23):
        mult = mult * 1.30
        evento = evento or 'Natal (temporada)'
    return mult, mais, evento


def main():
    r = random.Random(20250106)
    linhas = []
    for i in range(DIAS):
        d = INICIO + timedelta(days=i)
        mult, mais, evento = efeito(d)
        media = MEDIA * PESO_CONTAS[d.weekday()] * mult
        contas = binomial(r, 3000, media / 3000)
        compraram = binomial(r, contas, COMPRA[d.weekday()] + mais)
        linhas.append((d.isoformat(), contas, compraram, evento))
    DADOS.mkdir(exist_ok=True)
    with open(DADOS / 'gatilho_por_dia_2025.csv', 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f, lineterminator='\n')
        w.writerow(['data', 'contas_no_gatilho', 'compraram_7d', 'evento'])
        w.writerows(linhas)
    print(f'dias={len(linhas)} contas={sum(l[1] for l in linhas)} compraram={sum(l[2] for l in linhas)}')


if __name__ == '__main__':
    main()
