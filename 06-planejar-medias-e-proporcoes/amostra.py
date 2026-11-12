"""Contas de amostra da aula «Planejar médias e proporções».

Fórmulas pela aproximação normal, teste de dois lados, dois grupos do mesmo tamanho.
Só usa a biblioteca padrão; as simulações usam o NumPy, que vem com o pandas.

    n_proporcoes(p_a, p_b, alfa, poder)    visitas por grupo para ver p_a contra p_b
    n_medias(diferenca, desvio, alfa, poder)  observações por grupo para ver a diferença
    visitas_para(observacoes, taxa)        visitas para juntar as observações (pedidos)
    poder_proporcoes / poder_medias        o poder de um tamanho que já está escolhido
    simular_proporcoes / simular_medias    contam testes que passam da linha
"""
import math
from statistics import NormalDist

Z = NormalDist()


def _checar(alfa, poder):
    if not 0 < alfa < 1:
        raise ValueError(f"alfa precisa ficar entre 0 e 1, veio {alfa}")
    if not 0 < poder < 1:
        raise ValueError(f"poder precisa ficar entre 0 e 1, veio {poder}")


def _checar_taxa(nome, p):
    if not 0 < p < 1:
        raise ValueError(f"{nome} precisa ficar entre 0 e 1 (10% é 0.10), veio {p}")


def n_proporcoes(p_a, p_b, alfa=0.05, poder=0.80):
    """Visitas por grupo. Linha do teste com a taxa média dos dois grupos (como na hipótese
    de que não há efeito) e poder com a taxa de cada grupo. É a conta do power.prop.test do R."""
    _checar(alfa, poder)
    _checar_taxa("p_a", p_a)
    _checar_taxa("p_b", p_b)
    if p_a == p_b:
        raise ValueError("p_a e p_b iguais: não há diferença para ver")
    za, zb = Z.inv_cdf(1 - alfa / 2), Z.inv_cdf(poder)
    media = (p_a + p_b) / 2
    linha = za * math.sqrt(2 * media * (1 - media))
    folga = zb * math.sqrt(p_a * (1 - p_a) + p_b * (1 - p_b))
    return math.ceil(((linha + folga) / (p_b - p_a)) ** 2)


def n_medias(diferenca, desvio, alfa=0.05, poder=0.80):
    """Observações por grupo para ver uma diferença de médias, com o mesmo desvio nos dois."""
    _checar(alfa, poder)
    if diferenca == 0:
        raise ValueError("diferenca igual a zero: não há diferença para ver")
    if desvio <= 0:
        raise ValueError(f"desvio precisa ser maior que zero, veio {desvio}")
    za, zb = Z.inv_cdf(1 - alfa / 2), Z.inv_cdf(poder)
    return math.ceil(2 * ((za + zb) * desvio / diferenca) ** 2)


def visitas_para(observacoes, taxa):
    """Quantas visitas juntam essa quantidade de pedidos, se a taxa de compra for essa."""
    _checar_taxa("taxa", taxa)
    return math.ceil(observacoes / taxa)


def poder_proporcoes(p_a, p_b, n, alfa=0.05):
    """Chance de passar da linha com n visitas por grupo, se as taxas forem p_a e p_b."""
    za = Z.inv_cdf(1 - alfa / 2)
    media = (p_a + p_b) / 2
    linha = za * math.sqrt(2 * media * (1 - media) / n)
    ep = math.sqrt((p_a * (1 - p_a) + p_b * (1 - p_b)) / n)
    return 1 - Z.cdf((linha - abs(p_b - p_a)) / ep)


def poder_medias(diferenca, desvio, n, alfa=0.05):
    """Chance de passar da linha com n observações por grupo."""
    za = Z.inv_cdf(1 - alfa / 2)
    ep = desvio * math.sqrt(2 / n)
    return 1 - Z.cdf(za - abs(diferenca) / ep)


def simular_proporcoes(p_a, p_b, n, rodadas, rng, alfa=0.05):
    """Sorteia `rodadas` testes de n visitas por grupo e conta a fração que passa da linha."""
    za = Z.inv_cdf(1 - alfa / 2)
    compras_a = rng.binomial(n, p_a, rodadas)
    compras_b = rng.binomial(n, p_b, rodadas)
    taxa_a, taxa_b = compras_a / n, compras_b / n
    media = (compras_a + compras_b) / (2 * n)
    ep = (2 * media * (1 - media) / n) ** 0.5
    return float(((abs(taxa_b - taxa_a) / ep) > za).mean())


def tiquetes(rng, media, desvio, tamanho):
    """Tíquetes tortos para a direita (lognormal) com a média e o desvio pedidos."""
    s2 = math.log(1 + (desvio / media) ** 2)
    return rng.lognormal(math.log(media) - s2 / 2, math.sqrt(s2), tamanho)


def simular_medias(media, diferenca, desvio, n, rodadas, rng, alfa=0.05):
    """Sorteia `rodadas` testes com n pedidos por grupo e tíquetes tortos; conta quantos passam."""
    za = Z.inv_cdf(1 - alfa / 2)
    a = tiquetes(rng, media, desvio, (rodadas, n))
    b = tiquetes(rng, media + diferenca, desvio, (rodadas, n))
    ep = (a.var(axis=1, ddof=1) / n + b.var(axis=1, ddof=1) / n) ** 0.5
    return float(((abs(b.mean(axis=1) - a.mean(axis=1)) / ep) > za).mean())
