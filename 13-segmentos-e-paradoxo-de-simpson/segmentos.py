"""Funções da aula 13: total, composição, divisão e efeito por segmento num teste A/B.

Use de dentro da pasta da aula:  from segmentos import ler, taxas, ...
Precisa do pandas. O sorteio_sem_efeito usa o NumPy, que vem com o pandas.
"""
import math

import pandas as pd


def _p_dois_lados(z):
    return math.erfc(abs(z) / math.sqrt(2))


def ler(caminho):
    """Lê um CSV de visitas e para se algo não bate: id repetido, grupo fora de A e B, compra fora de 0 e 1."""
    df = pd.read_csv(caminho, dtype={"id_visita": str, "grupo": str})
    if df["id_visita"].duplicated().any():
        raise ValueError(f"id_visita repetido: {df.loc[df['id_visita'].duplicated(), 'id_visita'].iloc[0]}")
    if df["grupo"].isna().any():
        raise ValueError(f"grupo vazio em {int(df['grupo'].isna().sum())} visita(s); toda visita do teste tem A ou B")
    grupos = set(df["grupo"])
    if not grupos <= {"A", "B"}:
        raise ValueError(f"grupo precisa ser A ou B; veio {sorted(grupos)}")
    if not set(df["comprou"].unique()) <= {0, 1}:
        raise ValueError("comprou precisa ser 0 ou 1")
    return df


def _efeito(n_a, c_a, n_b, c_b):
    if min(n_a, n_b) == 0:
        raise ValueError("um dos grupos está vazio nesse corte")
    pa, pb = c_a / n_a, c_b / n_b
    ep = math.sqrt(pa * (1 - pa) / n_a + pb * (1 - pb) / n_b)
    return pa, pb, pb - pa, ep


def taxas(df, por=None, metrica="comprou"):
    """Uma linha por valor de `por` (ou uma linha só, o total): visitas, taxas, diferença B - A, erro padrão, z e p.

    A diferença é simples, sem olhar a composição: é o número do painel."""
    grupos = [("total", df)] if por is None else list(df.groupby(por, sort=True))
    linhas = []
    for valor, d in grupos:
        a, b = d[d["grupo"] == "A"][metrica], d[d["grupo"] == "B"][metrica]
        pa, pb, dif, ep = _efeito(len(a), a.sum(), len(b), b.sum())
        z = dif / ep if ep > 0 else 0.0
        linhas.append({"segmento": valor, "n_a": len(a), "n_b": len(b), "taxa_a": round(pa, 4), "taxa_b": round(pb, 4),
                       "diferenca": round(dif, 4), "ep": round(ep, 4), "z": round(z, 2), "p": round(_p_dois_lados(z), 4)})
    return pd.DataFrame(linhas).set_index("segmento")


def composicao(df, por):
    """Em cada grupo, que parte das visitas é de cada valor de `por`. Cada coluna soma 1."""
    return pd.crosstab(df[por], df["grupo"], normalize="columns").round(3)


def divisao(df, por, parte_b):
    """Divisão A/B em cada valor de `por`, contra a parte planejada para o B (um número ou um dicionário por valor).

    O p é o do qui-quadrado com 1 grau de liberdade, o mesmo teste da aula «Desvio da proporção de alocação»."""
    linhas = []
    for valor, d in df.groupby(por, sort=True):
        planejada = parte_b[valor] if isinstance(parte_b, dict) else parte_b
        n = len(d)
        n_b = int((d["grupo"] == "B").sum())
        esperado_b = n * planejada
        esperado_a = n - esperado_b
        qui2 = (n_b - esperado_b) ** 2 / esperado_b + ((n - n_b) - esperado_a) ** 2 / esperado_a
        linhas.append({"segmento": valor, "n": n, "n_a": n - n_b, "n_b": n_b, "parte_b": round(n_b / n, 3),
                       "planejada": planejada, "p": round(math.erfc(math.sqrt(qui2 / 2)), 3)})
    return pd.DataFrame(linhas).set_index("segmento")


def estratificado(df, estrato, metrica="comprou"):
    """Diferença B - A calculada dentro de cada estrato e somada com o mesmo peso para A e B.

    O peso de cada estrato é a parte dele em todas as visitas (A e B juntos).
    Retorna um dicionário com a diferença, o erro padrão, o intervalo de 95% e o p."""
    n_total = len(df)
    dif = var = 0.0
    for _, d in df.groupby(estrato, sort=True):
        a, b = d[d["grupo"] == "A"][metrica], d[d["grupo"] == "B"][metrica]
        _, _, dk, epk = _efeito(len(a), a.sum(), len(b), b.sum())
        peso = len(d) / n_total
        dif += peso * dk
        var += (peso * epk) ** 2
    ep = math.sqrt(var)
    z = dif / ep if ep > 0 else 0.0
    return {"diferenca": round(float(dif), 4), "ep": round(ep, 4),
            "ic95": (round(float(dif - 1.96 * ep), 4), round(float(dif + 1.96 * ep), 4)), "p": round(_p_dois_lados(z), 4)}


def cortes(df, colunas, estrato, metrica="comprou"):
    """Para cada coluna e cada valor dela, a diferença estratificada dentro daquele pedaço das visitas."""
    linhas = []
    for col in colunas:
        for valor, d in df.groupby(col, sort=True):
            r = estratificado(d, estrato, metrica)
            linhas.append({"coluna": col, "valor": valor, "n": len(d), "diferenca": r["diferenca"], "ep": r["ep"],
                           "p": r["p"]})
    return pd.DataFrame(linhas)


def interacao(r1, r2):
    """O efeito de um pedaço é diferente do de outro? Recebe dois resultados com diferenca e ep e retorna (diferença, z, p)."""
    d = float(r1["diferenca"]) - float(r2["diferenca"])
    ep = math.sqrt(float(r1["ep"]) ** 2 + float(r2["ep"]) ** 2)
    z = d / ep
    return round(d, 4), round(z, 2), round(_p_dois_lados(z), 4)


def sorteio_sem_efeito(df, colunas, estrato, vezes, semente, metrica="comprou", linha=0.05):
    """Embaralha os grupos dentro de cada estrato, como se o B não mudasse nada, e refaz todos os cortes.

    Retorna a parte dos sorteios com pelo menos um corte de p até `linha` e a média da maior diferença a favor do B."""
    import numpy as np

    rng = np.random.default_rng(semente)
    y = df[metrica].to_numpy()
    eh_b = (df["grupo"] == "B").to_numpy()
    est = pd.factorize(df[estrato], sort=True)[0]
    n_est = est.max() + 1
    blocos = [np.flatnonzero(est == k) for k in range(n_est)]
    cods = [pd.factorize(df[c], sort=True)[0] for c in colunas]
    algum = 0
    maiores = []
    for _ in range(vezes):
        b = eh_b.copy()
        for idx in blocos:
            b[idx] = rng.permutation(b[idx])
        menor_p, maior_d = 1.0, -1.0
        for cod in cods:
            for v in range(cod.max() + 1):
                no_corte = cod == v
                n_corte = no_corte.sum()
                dif = var = 0.0
                for k in range(n_est):
                    m = no_corte & (est == k)
                    mb, ma = m & b, m & ~b
                    na, nb = ma.sum(), mb.sum()
                    pa, pb = y[ma].mean(), y[mb].mean()
                    peso = m.sum() / n_corte
                    dif += peso * (pb - pa)
                    var += peso ** 2 * (pa * (1 - pa) / na + pb * (1 - pb) / nb)
                z = dif / math.sqrt(var)
                menor_p = min(menor_p, _p_dois_lados(z))
                maior_d = max(maior_d, dif)
        algum += menor_p <= linha
        maiores.append(maior_d)
    return round(algum / vezes, 3), round(float(sum(maiores)) / vezes, 4)
