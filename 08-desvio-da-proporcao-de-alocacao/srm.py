"""Contas da aula «Desvio da proporção de alocação».

    ler_visitas(caminho)                  lê um teste com os ids como texto
    teste_srm(contagens, proporcoes)      qui-quadrado da divisão contra a proporção planejada
    divisao_por(visitas, coluna)          a divisão do painel em cada valor de uma coluna (dia, navegador)
    conversao(visitas)                    taxa de cada grupo, diferença B - A e intervalo de 95%

Cada linha dos CSVs é uma visita sorteada pelo serviço de sorteio. A coluna `exposicao` diz se o
evento do navegador chegou ao registro, e é o que o painel do teste conta. A coluna `comprou` vem
do sistema de pedidos.

Só usa a biblioteca padrão nas contas (math e statistics). A leitura e as tabelas usam o pandas.
"""
import math
import operator
from statistics import NormalDist

Z = NormalDist()
COLUNAS = ["id_visita", "dia", "navegador", "grupo", "exposicao", "comprou"]


def ler_visitas(caminho):
    """Lê um teste. Os ids ficam como texto e as colunas 0/1 como números inteiros."""
    import pandas as pd
    visitas = pd.read_csv(caminho, dtype={"id_visita": str, "dia": str, "navegador": str, "grupo": str})
    faltam = [c for c in COLUNAS if c not in visitas.columns]
    if faltam:
        raise ValueError(f"faltam colunas no arquivo: {faltam}")
    return visitas


def _contagem(valor):
    if isinstance(valor, bool):
        raise ValueError(f"contagem precisa ser um número inteiro, veio {valor!r}")
    try:
        valor = operator.index(valor)
    except TypeError:
        raise ValueError(f"contagem precisa ser um número inteiro, veio {valor!r}") from None
    if valor < 0:
        raise ValueError(f"contagem não pode ser negativa, veio {valor}")
    return valor


def _cauda_qui2(x, gl):
    """P(qui-quadrado com gl graus de liberdade > x), pela fórmula fechada para gl inteiro."""
    if x <= 0:
        return 1.0
    if gl % 2 == 0:
        termo, soma = 1.0, 1.0
        for i in range(1, gl // 2):
            termo *= (x / 2) / i
            soma += termo
        return min(1.0, math.exp(-x / 2) * soma)
    p = math.erfc(math.sqrt(x / 2))
    termo = math.sqrt(2 * x / math.pi)
    soma = 0.0
    for i in range(1, (gl - 1) // 2 + 1):
        if i > 1:
            termo *= x / (2 * i - 1)
        soma += termo
    return min(1.0, p + math.exp(-x / 2) * soma)


def teste_srm(contagens, proporcoes=None):
    """(qui2, p) da divisão observada contra a planejada.

    contagens: visitas de cada grupo, na ordem dos grupos (por exemplo [n_a, n_b]).
    proporcoes: a divisão planejada, na mesma ordem (padrão: partes iguais). Precisa somar 1.
    É o mesmo teste do scipy.stats.chisquare(contagens, f_exp=total * proporcoes)."""
    contagens = [_contagem(c) for c in contagens]
    if len(contagens) < 2:
        raise ValueError("precisa de pelo menos dois grupos")
    total = sum(contagens)
    if total == 0:
        raise ValueError("sem visitas nos grupos")
    if proporcoes is None:
        proporcoes = [1 / len(contagens)] * len(contagens)
    proporcoes = list(proporcoes)
    if len(proporcoes) != len(contagens):
        raise ValueError(f"{len(contagens)} grupos e {len(proporcoes)} proporções")
    if any(not 0 < p < 1 for p in proporcoes) or abs(sum(proporcoes) - 1) > 1e-9:
        raise ValueError(f"as proporções ficam entre 0 e 1 e somam 1 (meio a meio é [0.5, 0.5]), veio {proporcoes}")
    esperado = [total * p for p in proporcoes]
    qui2 = sum((o - e) ** 2 / e for o, e in zip(contagens, esperado))
    return qui2, _cauda_qui2(qui2, len(contagens) - 1)


def divisao_por(visitas, coluna, so_painel=True):
    """Uma linha por valor da coluna: visitas do A, do B, B - A e o p da divisão meio a meio.
    Com so_painel=True conta só o que o painel conta (exposicao = 1); com False, todo o sorteio."""
    base = visitas[visitas["exposicao"] == 1] if so_painel else visitas
    tabela = base.groupby([coluna, "grupo"]).size().unstack(fill_value=0)
    for g in ("A", "B"):
        if g not in tabela.columns:
            tabela[g] = 0
    tabela = tabela[["A", "B"]]
    tabela["B - A"] = tabela["B"] - tabela["A"]
    tabela["p"] = [round(teste_srm([int(a), int(b)])[1], 4) if a + b > 0 else float("nan")
                   for a, b in zip(tabela["A"], tabela["B"])]
    tabela.columns.name = None
    return tabela


def conversao(visitas):
    """(taxa_a, taxa_b, diferença b - a, limite de baixo, limite de cima), com o intervalo de 95%
    da diferença de duas proporções. A taxa é compras dividido pelas visitas da tabela recebida."""
    taxas, ns = {}, {}
    for g in ("A", "B"):
        parte = visitas[visitas["grupo"] == g]
        if len(parte) == 0:
            raise ValueError(f"o grupo {g} não tem nenhuma visita nessa tabela")
        ns[g], taxas[g] = len(parte), float(parte["comprou"].mean())
    ta, tb = taxas["A"], taxas["B"]
    ep = math.sqrt(ta * (1 - ta) / ns["A"] + tb * (1 - tb) / ns["B"])
    dif = tb - ta
    z = Z.inv_cdf(0.975)
    return ta, tb, dif, dif - z * ep, dif + z * ep
