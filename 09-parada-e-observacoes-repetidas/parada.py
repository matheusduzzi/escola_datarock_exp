"""Contas da aula «Parada e observações repetidas», do curso Experimentação e teste A/B.

ler_diario     lê o arquivo de um teste, um dia por linha, e recusa contagem errada
acumulado      soma os dias e calcula, a cada dia, a diferença de conversão, o z e o p
teste_proporcoes   o teste de duas proporções (z) com as contagens somadas até um dia
alarme_falso   a chance de pelo menos uma olhada cruzar a linha, com ou sem efeito de verdade
linhas_parada  as linhas de cada olhada para que o teste inteiro tenha a chance de alarme falso combinada
simular_teste  roda muitos testes com uma regra de parada e diz onde cada um parou
simular_aa     roda muitos testes A/A e conta quantos cruzam a linha em alguma olhada

As olhadas são os dias em que alguém abre o resultado. A conta supõe visitas parecidas em cada
dia, então a fração do teste que já rodou numa olhada é o dia dela dividido pelo último dia.
Usa a biblioteca padrão, o NumPy e o pandas. Não precisa do SciPy.
"""
import math

import numpy as np
import pandas as pd

COLUNAS = ["dia", "visitas_A", "compras_A", "visitas_B", "compras_B"]


def _inteiro(nome, valor, minimo=0):
    if isinstance(valor, bool) or not isinstance(valor, (int, np.integer)):
        raise ValueError(f"{nome} precisa ser um número inteiro, veio {valor!r}")
    if valor < minimo:
        raise ValueError(f"{nome} precisa ser pelo menos {minimo}, veio {valor}")
    return int(valor)


def p_de_z(z):
    """p dos dois lados para um z."""
    return math.erfc(abs(z) / math.sqrt(2))


def teste_proporcoes(compras_a, visitas_a, compras_b, visitas_b):
    """Diferença de conversão (B - A), z e p dos dois lados, com a taxa juntando os grupos."""
    ca = _inteiro("compras_A", compras_a)
    va = _inteiro("visitas_A", visitas_a, 1)
    cb = _inteiro("compras_B", compras_b)
    vb = _inteiro("visitas_B", visitas_b, 1)
    if ca > va or cb > vb:
        raise ValueError("um grupo tem mais compras que visitas")
    junto = (ca + cb) / (va + vb)
    erro = math.sqrt(junto * (1 - junto) * (1 / va + 1 / vb))
    dif = cb / vb - ca / va
    if erro == 0:
        return dif, 0.0, 1.0
    z = dif / erro
    return dif, z, p_de_z(z)


def ler_diario(caminho):
    """Lê o teste, um dia por linha, com as colunas de COLUNAS. Recusa dia fora de ordem e contagem errada."""
    tabela = pd.read_csv(caminho)
    faltam = [c for c in COLUNAS if c not in tabela.columns]
    if faltam:
        raise ValueError(f"faltam as colunas {faltam} em {caminho}")
    if tabela[COLUNAS].isna().any().any():
        raise ValueError(f"{caminho} tem célula vazia")
    if list(tabela["dia"]) != list(range(1, len(tabela) + 1)):
        raise ValueError("os dias precisam ir de 1 em 1, começando no 1")
    for c in COLUNAS[1:]:
        if (tabela[c] < 0).any():
            raise ValueError(f"a coluna {c} tem contagem negativa")
    if (tabela["compras_A"] > tabela["visitas_A"]).any() or (tabela["compras_B"] > tabela["visitas_B"]).any():
        raise ValueError("algum dia tem mais compras que visitas")
    return tabela[COLUNAS].astype(int)


def acumulado(diario):
    """Soma os dias. Em cada dia: as taxas até ali, a diferença B - A, o z e o p."""
    soma = diario.set_index("dia")[COLUNAS[1:]].cumsum()
    linhas = []
    for dia, r in soma.iterrows():
        dif, z, p = teste_proporcoes(int(r.compras_A), int(r.visitas_A), int(r.compras_B), int(r.visitas_B))
        linhas.append({"dia": dia, "visitas_A": int(r.visitas_A), "visitas_B": int(r.visitas_B),
                       "taxa_A": r.compras_A / r.visitas_A, "taxa_B": r.compras_B / r.visitas_B,
                       "dif": dif, "z": z, "p": p})
    return pd.DataFrame(linhas).set_index("dia")


def _fracoes(olhadas):
    olhadas = list(olhadas)
    if not olhadas:
        raise ValueError("precisa de pelo menos uma olhada")
    for o in olhadas:
        if isinstance(o, bool) or not isinstance(o, (int, float, np.integer, np.floating)) or o <= 0:
            raise ValueError(f"cada olhada precisa ser um número positivo, veio {o!r}")
    if any(b <= a for a, b in zip(olhadas, olhadas[1:])):
        raise ValueError("as olhadas precisam estar em ordem crescente, sem repetir")
    return [o / olhadas[-1] for o in olhadas]


def _linhas(linhas, k):
    if isinstance(linhas, (int, float, np.integer, np.floating)) and not isinstance(linhas, bool):
        linhas = [float(linhas)] * k
    linhas = [float(x) for x in linhas]
    if len(linhas) != k:
        raise ValueError(f"são {k} olhadas e {len(linhas)} linhas")
    if any(x <= 0 for x in linhas):
        raise ValueError("cada linha precisa ser um z positivo")
    return linhas


def _phi(x):
    return np.exp(-0.5 * x * x) / math.sqrt(2 * math.pi)


def _cauda(x):
    """Chance de uma normal padrão passar de x."""
    return 0.5 * math.erfc(x / math.sqrt(2))


def _por_olhada(fracoes, linhas, deriva, passo):
    """Chance de o teste parar em cada olhada, cruzando a linha para cima ou para baixo.

    S(t) é o placar acumulado na escala do teste inteiro: S(t) = z(t) × raiz(t), com média deriva × t.
    Entre duas olhadas ele anda uma normal com variância igual ao pedaço de teste que rodou.
    Em cada olhada guardo a densidade de quem ainda não cruzou, numa grade de passo fino.
    """
    t1, l1 = fracoes[0], linhas[0] * math.sqrt(fracoes[0])
    chances = [_cauda((l1 - deriva * t1) / math.sqrt(t1)) + _cauda((l1 + deriva * t1) / math.sqrt(t1))]
    n = max(2, math.ceil(2 * l1 / passo))
    h = 2 * l1 / n
    x = -l1 + h * (np.arange(n) + 0.5)
    massa = _phi((x - deriva * t1) / math.sqrt(t1)) / math.sqrt(t1) * h
    for k in range(1, len(fracoes)):
        delta = fracoes[k] - fracoes[k - 1]
        dp = math.sqrt(delta)
        lk = linhas[k] * math.sqrt(fracoes[k])
        n_dentro = max(2, math.ceil(2 * lk / passo))
        h = 2 * lk / n_dentro
        fora = math.ceil(9 * dp / h)
        y = -lk - fora * h + h * (np.arange(n_dentro + 2 * fora) + 0.5)
        nucleo = _phi((y[:, None] - x[None, :] - deriva * delta) / dp) / dp * h
        with np.errstate(all="ignore"):  # o BLAS do macOS solta aviso falso no produto de matrizes
            nova = nucleo @ massa
        if not np.isfinite(nova).all():
            raise ArithmeticError("a conta da grade saiu com valor inválido")
        dentro = (y > -lk) & (y < lk)
        chances.append(float(nova[~dentro].sum()))
        x, massa = y[dentro], nova[dentro]
    return chances


def alarme_falso(olhadas, linhas=1.96, deriva=0.0, por_olhada=False, passo=0.01):
    """Chance de alguma olhada cruzar a linha (para cima ou para baixo).

    olhadas: os dias (ou visitas) em que se olha, em ordem. linhas: um z para todas ou um por olhada.
    deriva: o z esperado no fim do teste se houver efeito; 0 é o teste sem efeito, e aí a chance é o
    alarme falso. Com deriva, a mesma conta dá o poder. por_olhada=True dá a chance de parar em cada olhada.
    """
    fracoes = _fracoes(olhadas)
    linhas = _linhas(linhas, len(fracoes))
    chances = _por_olhada(fracoes, linhas, float(deriva), passo)
    return chances if por_olhada else sum(chances)


def linhas_parada(olhadas, alfa=0.05, forma="obf"):
    """Linhas de z para cada olhada, com chance total de alarme falso igual a alfa.

    forma="obf": a linha de O'Brien e Fleming, alta no começo e perto de 1,96 no fim
    (c × raiz(último dia ÷ dia da olhada)). forma="pocock": a mesma linha em todas as olhadas.
    """
    if isinstance(alfa, bool) or not isinstance(alfa, (int, float)) or not 0 < alfa < 1:
        raise ValueError(f"alfa precisa ser uma fração entre 0 e 1, veio {alfa!r}")
    if forma not in ("obf", "pocock"):
        raise ValueError('forma precisa ser "obf" ou "pocock"')
    fracoes = _fracoes(olhadas)

    def linhas_de(c):
        return [c / math.sqrt(t) for t in fracoes] if forma == "obf" else [c] * len(fracoes)

    baixo, cima = 0.5, 8.0
    for _ in range(45):
        meio = (baixo + cima) / 2
        if sum(_por_olhada(fracoes, linhas_de(meio), 0.0, 0.01)) > alfa:
            baixo = meio
        else:
            cima = meio
    return linhas_de((baixo + cima) / 2)


def simular_teste(testes, dias, visitas_dia, taxa_a, taxa_b, olhadas, linhas, rng):
    """Roda testes com a regra de parada e retorna, por teste, o dia em que parou e a diferença naquele dia.

    Cada dia, cada grupo recebe visitas_dia visitas. Uma visita do A compra com taxa_a e uma do B com
    taxa_b. O teste para na primeira olhada em que o z cruza a linha, para cima ou para baixo.
    parou_no_dia = 0 quer dizer que nenhuma olhada cruzou; aí a diferença é a do último dia.
    """
    testes = _inteiro("testes", testes, 1)
    dias = _inteiro("dias", dias, 1)
    visitas_dia = _inteiro("visitas_dia", visitas_dia, 1)
    for nome, taxa in (("taxa_a", taxa_a), ("taxa_b", taxa_b)):
        if isinstance(taxa, bool) or not isinstance(taxa, float) or not 0 < taxa < 1:
            raise ValueError(f"{nome} precisa ser uma fração entre 0 e 1, veio {taxa!r}")
    olhadas = list(olhadas)
    _fracoes(olhadas)
    if any(isinstance(o, bool) or o not in range(1, dias + 1) for o in olhadas):
        raise ValueError(f"cada olhada precisa ser um dia de 1 a {dias}")
    linhas = np.array(_linhas(linhas, len(olhadas)))
    ca = rng.binomial(visitas_dia, taxa_a, size=(testes, dias)).cumsum(axis=1)
    cb = rng.binomial(visitas_dia, taxa_b, size=(testes, dias)).cumsum(axis=1)
    idx = np.array(olhadas) - 1
    n = visitas_dia * (idx + 1)
    a, b = ca[:, idx], cb[:, idx]
    junto = (a + b) / (2 * n)
    erro = np.sqrt(junto * (1 - junto) * (2 / n))
    dif = b / n - a / n
    z = np.divide(dif, erro, out=np.zeros_like(erro), where=erro > 0)
    cruzou = np.abs(z) >= linhas
    algum = cruzou.any(axis=1)
    primeira = np.where(algum, cruzou.argmax(axis=1), len(olhadas) - 1)
    return pd.DataFrame({"parou_no_dia": np.where(algum, np.array(olhadas)[primeira], 0),
                         "dif": dif[np.arange(testes), primeira]})


def simular_aa(testes, dias, visitas_dia, taxa, olhadas, linhas, rng):
    """Roda testes A/A (A e B iguais) e retorna a fração que cruzou a linha em alguma olhada."""
    resultado = simular_teste(testes, dias, visitas_dia, taxa, taxa, olhadas, linhas, rng)
    return float((resultado["parou_no_dia"] > 0).mean())
