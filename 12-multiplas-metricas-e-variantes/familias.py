"""Regras para uma família de testes: Bonferroni, Holm e Benjamini-Hochberg.

Só biblioteca padrão. Cada regra recebe a lista de p-valores de uma família e retorna
uma lista de True/False na mesma ordem: True quer dizer que o teste passou na regra.
"""
import csv
from statistics import NormalDist

z = NormalDist()


def ler(caminho):
    """Lê um CSV de resultados (uma linha por teste) e converte as colunas de número."""
    with open(caminho, encoding="utf-8") as f:
        linhas = list(csv.DictReader(f))
    for l in linhas:
        for c in ("taxa_a", "taxa_versao", "diferenca", "erro_padrao", "p_valor"):
            l[c] = float(l[c])
    return linhas


def bonferroni(ps, alfa=0.05):
    """Cada teste passa se o p fica na linha alfa dividida pelo tamanho da família."""
    m = len(ps)
    return [p <= alfa / m for p in ps]


def holm(ps, alfa=0.05):
    """Do menor p para o maior: o 1º usa alfa/m, o 2º alfa/(m-1), e assim por diante.
    Para no primeiro que não passa; dali para a frente, nenhum passa."""
    m = len(ps)
    ordem = sorted(range(m), key=lambda i: ps[i])
    passa = [False] * m
    for passo, i in enumerate(ordem):
        if ps[i] > alfa / (m - passo):
            break
        passa[i] = True
    return passa


def bh(ps, q=0.10):
    """Benjamini-Hochberg. Ordena os p. O de posição i é comparado com i/m * q.
    Acha a maior posição que fica na linha; ela e todas as de p menor passam."""
    m = len(ps)
    ordem = sorted(range(m), key=lambda i: ps[i])
    k = 0
    for posicao, i in enumerate(ordem, 1):
        if ps[i] <= posicao / m * q:
            k = posicao
    passa = [False] * m
    for i in ordem[:k]:
        passa[i] = True
    return passa


def simular(m, reais, efeito, vezes, rng, alfa=0.05, q=0.10):
    """Sorteia `vezes` famílias de m testes. Os `reais` primeiros têm efeito de verdade
    (o z deles sai em torno de `efeito`); os outros não têm efeito nenhum.

    Retorna, para cada regra:
    - a parte das famílias com pelo menos um alarme falso;
    - a média da parte falsa entre os testes que passaram (zero quando nada passa);
    - quantos efeitos de verdade passaram, em média.
    """
    regras = {
        "sem correção": lambda ps: [p <= alfa for p in ps],
        "Bonferroni": lambda ps: bonferroni(ps, alfa),
        "Holm": lambda ps: holm(ps, alfa),
        "BH": lambda ps: bh(ps, q),
    }
    conta = {r: [0, 0.0, 0] for r in regras}
    for _ in range(vezes):
        ps = []
        for i in range(m):
            zi = rng.gauss(efeito if i < reais else 0.0, 1.0)
            ps.append(2 * (1 - z.cdf(abs(zi))))
        for r, regra in regras.items():
            passa = regra(ps)
            falsos = sum(passa[reais:])
            total = sum(passa)
            conta[r][0] += falsos > 0
            conta[r][1] += falsos / total if total else 0.0
            conta[r][2] += sum(passa[:reais])
    return {r: (round(a / vezes, 3), round(b / vezes, 3), round(c / vezes, 2))
            for r, (a, b, c) in conta.items()}
