"""Contas da aula «Instrumentar e testar A/A».

    ler_eventos(caminho)                     lê o CSV de eventos com os ids como texto
    p_divisao(n_a, n_b)                      a divisão meio a meio está em ordem? (p de dois lados)
    comparar_conversao(c_a, n_a, c_b, n_b)   taxa de cada grupo, diferença e p de dois lados
    sortear(id_visita, nome_teste)           o grupo de uma visita, sempre o mesmo para o mesmo id
    simular_aa(n_visitas, taxa, rodadas, rng, reenvio_b)   muitos A/A sorteados de uma vez

As contas usam a curva normal da biblioteca padrão (statistics.NormalDist). A leitura usa o
pandas, e a simulação, o NumPy, que vem com ele.
"""
import hashlib
import math
import operator
from statistics import NormalDist

Z = NormalDist()
COLUNAS_TEXTO = {"id_evento": str, "id_visita": str, "id_sessao": str, "evento": str, "grupo": str}


def ler_eventos(caminho):
    """Lê os eventos. Os ids ficam como texto: 00012345 continua 00012345."""
    import pandas as pd
    eventos = pd.read_csv(caminho, dtype=COLUNAS_TEXTO, parse_dates=["momento"])
    return eventos


def _contagem(nome, valor):
    if isinstance(valor, bool):
        raise ValueError(f"{nome} precisa ser um número inteiro, veio {valor!r}")
    try:
        valor = operator.index(valor)
    except TypeError:
        raise ValueError(f"{nome} precisa ser um número inteiro, veio {valor!r}") from None
    if valor < 0:
        raise ValueError(f"{nome} não pode ser negativo, veio {valor}")
    return valor


def p_divisao(n_a, n_b):
    """p de dois lados para a divisão n_a contra n_b, se o sorteio for meio a meio.
    É o mesmo p do qui-quadrado com um grau de liberdade."""
    n_a, n_b = _contagem("n_a", n_a), _contagem("n_b", n_b)
    n = n_a + n_b
    if n == 0:
        raise ValueError("sem visitas nos dois grupos")
    z = (n_b - n / 2) / math.sqrt(n / 4)
    return 2 * (1 - Z.cdf(abs(z)))


def comparar_conversao(c_a, n_a, c_b, n_b):
    """(taxa_a, taxa_b, diferença b - a, p de dois lados), teste de duas proporções com a taxa
    dos dois grupos juntos na linha do teste."""
    c_a, n_a = _contagem("c_a", c_a), _contagem("n_a", n_a)
    c_b, n_b = _contagem("c_b", c_b), _contagem("n_b", n_b)
    if n_a == 0 or n_b == 0:
        raise ValueError("cada grupo precisa de pelo menos uma visita")
    if c_a > n_a or c_b > n_b:
        raise ValueError("mais compras que visitas: alguma compra foi contada duas vezes?")
    ta, tb = c_a / n_a, c_b / n_b
    junto = (c_a + c_b) / (n_a + n_b)
    ep = math.sqrt(junto * (1 - junto) * (1 / n_a + 1 / n_b))
    p = 1.0 if ep == 0 else 2 * (1 - Z.cdf(abs(tb - ta) / ep))
    return ta, tb, tb - ta, p


def sortear(id_visita, nome_teste="parcelamento"):
    """A ou B pelo resumo SHA-256 do nome do teste com o id da visita.
    O mesmo id dá sempre o mesmo grupo, em qualquer página e em qualquer recarga."""
    if not isinstance(id_visita, str) or not id_visita.strip():
        raise ValueError(f"id_visita vazio: não dá para sortear, veio {id_visita!r}")
    resumo = hashlib.sha256(f"{nome_teste}:{id_visita}".encode("utf-8")).digest()
    return "A" if resumo[0] % 2 == 0 else "B"


def simular_aa(n_visitas, taxa, rodadas, rng, reenvio_b=0.0):
    """Sorteia `rodadas` testes A/A de `n_visitas` cada um, com a mesma `taxa` de compra nos
    dois grupos. Com reenvio_b > 0, essa fração das exposições do B é contada duas vezes como
    visita, como no reenvio do app. Retorna dois arrays de p: o da divisão e o da conversão."""
    import numpy as np
    if not 0 < taxa < 1:
        raise ValueError(f"taxa precisa ficar entre 0 e 1 (10% é 0.10), veio {taxa}")
    if not 0 <= reenvio_b < 1:
        raise ValueError(f"reenvio_b precisa ficar entre 0 e 1, veio {reenvio_b}")
    n_b = rng.binomial(n_visitas, 0.5, size=rodadas)
    n_a = n_visitas - n_b
    c_a = rng.binomial(n_a, taxa)
    c_b = rng.binomial(n_b, taxa)
    n_b_contado = n_b + rng.binomial(n_b, reenvio_b)
    p_div = np.array([p_divisao(int(a), int(b)) for a, b in zip(n_a, n_b_contado)])
    p_conv = np.array([comparar_conversao(int(ca), int(a), int(cb), int(b))[3]
                       for ca, a, cb, b in zip(c_a, n_a, c_b, n_b_contado)])
    return p_div, p_conv
