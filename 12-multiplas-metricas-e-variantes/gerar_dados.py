"""Gera os dois arquivos de resultados dessa aula. Só biblioteca padrão; sai igual toda vez.

Como os dados nascem:
- Cada conta é sorteada para uma versão, com a mesma chance para todas.
- Cada métrica é sim ou não por conta (comprou em 7 dias, devolveu em 30 dias...).
  A chance de cada uma depende só da versão. As métricas são sorteadas soltas umas das
  outras, menos duas: quem comprou também pôs no carrinho, e só quem comprou pode devolver.
- Para cada versão contra a A, o programa calcula a diferença de taxas, o erro padrão sem
  juntar os grupos e o p-valor de dois lados pela curva normal.

Em algumas métricas a versão nova muda a chance de verdade; nas outras, não muda nada.
Os sorteios usam random.Random com um número fixo, por isso o arquivo sai igual.
"""
import csv
import math
import random
from statistics import NormalDist

z = NormalDist()

# Teste da página do produto: A é a página de hoje, B tem fotos grandes, C traz as avaliações no topo.
PAGINA = {
    "arquivo": "resultados_pagina.csv",
    "sorteio": 85,
    "contas": 18000,
    "versoes": ["A", "B", "C"],
    "metricas": {
        "comprou_7d": {"A": 0.080, "B": 0.092, "C": 0.083},
        "devolveu_30d": {"A": 0.18, "B": 0.18, "C": 0.18},  # parte de quem comprou
        "chamou_atendimento_7d": {"A": 0.030, "B": 0.030, "C": 0.039},
        "pos_no_carrinho": {"A": 0.200, "B": 0.215, "C": 0.208},
        "abriu_fotos": {"A": 0.350, "B": 0.410, "C": 0.350},
        "leu_avaliacoes": {"A": 0.250, "B": 0.250, "C": 0.320},
        "voltou_7d": {"A": 0.300, "B": 0.300, "C": 0.300},
        "favoritou": {"A": 0.050, "B": 0.050, "C": 0.050},
    },
}

# Teste do lembrete de carrinho: A sem lembrete, B lembrete em 1 hora, C em 24 horas, D em 24 horas com cupom.
LEMBRETE = {
    "arquivo": "resultados_lembrete.csv",
    "sorteio": 377,
    "contas": 24000,
    "versoes": ["A", "B", "C", "D"],
    "metricas": {
        "comprou_7d": {"A": 0.060, "B": 0.070, "C": 0.066, "D": 0.076},
        "saiu_da_lista_30d": {"A": 0.010, "B": 0.015, "C": 0.011, "D": 0.011},
        "cancelou_7d": {"A": 0.15, "B": 0.15, "C": 0.15, "D": 0.15},  # parte de quem comprou
        "voltou_2d": {"A": 0.150, "B": 0.180, "C": 0.170, "D": 0.180},
        "comprou_outro_item": {"A": 0.020, "B": 0.020, "C": 0.020, "D": 0.020},
        "recomprou_30d": {"A": 0.040, "B": 0.040, "C": 0.040, "D": 0.047},
        "avaliou_produto": {"A": 0.020, "B": 0.020, "C": 0.020, "D": 0.020},
    },
}

# Métricas que só existem para quem comprou: a chance da tabela vale para quem comprou.
SO_QUEM_COMPROU = {"devolveu_30d", "cancelou_7d"}


def sortear(teste, sorteio=None):
    rng = random.Random(teste["sorteio"] if sorteio is None else sorteio)
    contas = {v: {"n": 0, **{m: 0 for m in teste["metricas"]}} for v in teste["versoes"]}
    for _ in range(teste["contas"]):
        v = rng.choice(teste["versoes"])
        c = contas[v]
        c["n"] += 1
        comprou = False
        for m, chance in teste["metricas"].items():
            if m in SO_QUEM_COMPROU:
                sim = comprou and rng.random() < chance[v]
            else:
                sim = rng.random() < chance[v]
            if m == "comprou_7d":
                comprou = sim
            if m == "pos_no_carrinho":
                sim = sim or comprou
            c[m] += sim
    return contas


def comparar(teste, contas):
    a = contas["A"]
    linhas = []
    for v in teste["versoes"][1:]:
        b = contas[v]
        for m in teste["metricas"]:
            pa, pb = a[m] / a["n"], b[m] / b["n"]
            ep = math.sqrt(pa * (1 - pa) / a["n"] + pb * (1 - pb) / b["n"])
            p = 2 * (1 - z.cdf(abs(pb - pa) / ep))
            linhas.append({"versao": v, "metrica": m, "contas_a": a["n"], "contas_versao": b["n"],
                           "taxa_a": round(pa, 4), "taxa_versao": round(pb, 4), "diferenca": round(pb - pa, 4),
                           "erro_padrao": round(ep, 4), "p_valor": round(p, 4)})
    return linhas


def escrever(teste):
    linhas = comparar(teste, sortear(teste))
    with open(teste["arquivo"], "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(linhas[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(linhas)
    return len(linhas)


if __name__ == "__main__":
    print(f"resultados_pagina={escrever(PAGINA)} resultados_lembrete={escrever(LEMBRETE)}")
