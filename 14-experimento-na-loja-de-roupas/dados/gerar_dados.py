"""Gera as duas tabelas da rede Trama: as 24 lojas e 27 semanas de cada loja.

Uso: python3 gerar_dados.py   (na pasta dados/)

Sai igual toda vez. Só usa a biblioteca padrão.

Como os números nascem (as hipóteses do gerador, para quem quiser mexer):
- cada loja tem um tamanho de venda próprio, que varia muito de uma loja para outra;
- toda loja sobe e desce junto nas datas da rede (Dia das Mães, Dia dos Namorados, liquidação);
- cada loja tem uma tendência própria nas 27 semanas e um ruído semanal que puxa a semana seguinte;
- cada loja tem a sua taxa de devolução; uns 55% do que volta em 30 dias volta nos 7 primeiros;
- a falta de tamanho acompanha as entradas, com uma taxa própria de cada loja.
Nenhuma semana tem o look pronto: as 27 semanas são de antes do teste.
"""
import csv
import datetime as dt
import math
import random
from pathlib import Path

AQUI = Path(__file__).resolve().parent
PRIMEIRA_SEMANA = dt.date(2026, 1, 19)  # segunda-feira
SEMANAS = 27  # até a semana que começa em 20/07/2026
TENDENCIA = 0.03  # desvio da tendência de cada loja, de ponta a ponta
RUIDO = 0.045  # ruído semanal de cada loja

CIDADES = [('Campinas', 4), ('Ribeirão Preto', 3), ('Sorocaba', 3), ('São José dos Campos', 3),
           ('Piracicaba', 2), ('Jundiaí', 2), ('Bauru', 2), ('Limeira', 2), ('São Carlos', 2),
           ('Araraquara', 1)]

# Datas da rede: semana (segunda) -> fator comum a todas as lojas
DATAS = {dt.date(2026, 2, 16): 0.90,   # Carnaval
         dt.date(2026, 5, 4): 1.28,    # semana do Dia das Mães (10/05)
         dt.date(2026, 6, 8): 1.12,    # Dia dos Namorados (12/06)
         dt.date(2026, 7, 6): 1.15,    # liquidação de inverno
         dt.date(2026, 7, 13): 1.10,
         dt.date(2026, 7, 20): 1.05}


def gerar():
    rng = random.Random(1409)
    lojas, semanas = [], []
    n = 0
    for cidade, qtd in CIDADES:
        for _ in range(qtd):
            n += 1
            tamanho = math.exp(rng.gauss(math.log(52000), 0.38))
            area = int(round(tamanho / 230 / 10) * 10)
            lojas.append({'loja': f'L{n:02d}', 'cidade': cidade, 'area_m2': area,
                          'provadores': max(3, round(area / 45))})
            tendencia = rng.gauss(0, TENDENCIA)        # variação de ponta a ponta nas 27 semanas
            taxa_dev = rng.gauss(0.092, 0.014)
            taxa_falta = rng.gauss(4.0, 0.9) / 1000
            por_entrada = rng.gauss(38, 4)
            ruido = 0.0
            for s in range(SEMANAS):
                segunda = PRIMEIRA_SEMANA + dt.timedelta(weeks=s)
                ruido = 0.45 * ruido + rng.gauss(0, RUIDO)
                fator = DATAS.get(segunda, 1.0) * (1 + tendencia * s / (SEMANAS - 1)) * math.exp(ruido)
                vendas = tamanho * fator
                entradas = vendas / por_entrada * math.exp(rng.gauss(0, 0.04))
                dev30 = vendas * max(0.03, taxa_dev) * math.exp(rng.gauss(0, 0.13))
                dev7 = dev30 * min(0.9, max(0.3, rng.gauss(0.55, 0.05)))
                falta = sum(1 for _ in range(int(entradas)) if rng.random() < max(0.001, taxa_falta))
                semanas.append({'loja': f'L{n:02d}', 'semana': segunda.isoformat(),
                                'entradas': int(round(entradas)), 'vendas': round(vendas, 2),
                                'devolvido_7d': round(dev7, 2), 'devolvido_30d': round(dev30, 2),
                                'falta_tamanho': falta})
    return lojas, semanas


def salvar(nome, linhas):
    with open(AQUI / nome, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(linhas[0]))
        w.writeheader()
        w.writerows(linhas)


if __name__ == '__main__':
    lojas, semanas = gerar()
    salvar('lojas.csv', lojas)
    salvar('semanas.csv', semanas)
    print(f'lojas={len(lojas)} semanas={len(semanas)} cidades={len(CIDADES)}')
