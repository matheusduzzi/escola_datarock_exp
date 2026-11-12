"""As quatro checagens da aula «Instrumentar e testar A/A», juntas, e o teste delas.

    checar(eventos)                    as falhas que as quatro checagens acham, com os ids
    tabela_de_visitas(eventos)         uma linha por visita: grupo do primeiro sorteio e converteu
    semana_sintetica(n, taxa, rng)     uma semana de eventos sem nenhuma falha
    plantar(eventos, rng, ...)         planta falhas que você escolhe e diz quais plantou

Os eventos têm as colunas momento, id_evento, id_visita, id_sessao, evento e grupo, como os
arquivos de dados/. É o mesmo código das seções 5 e 6 da aula.
"""
import datetime as dt

import pandas as pd

COLUNAS = ["momento", "id_evento", "id_visita", "id_sessao", "evento", "grupo"]


def _partes(eventos):
    faltando = [c for c in COLUNAS if c not in eventos.columns]
    if faltando:
        raise ValueError(f"faltam as colunas {faltando} nos eventos")
    tipos = set(eventos["evento"].dropna().unique()) - {"exposicao", "compra"}
    if tipos:
        raise ValueError(f"tipo de evento que a checagem não conhece: {sorted(tipos)}")
    if eventos[["id_evento", "id_visita", "id_sessao"]].isna().any().any():
        raise ValueError("há evento com id vazio: corrija o registro antes de checar")
    exposicoes = eventos[eventos["evento"] == "exposicao"]
    compras = eventos[eventos["evento"] == "compra"].drop(columns="grupo")
    return exposicoes, compras


def _primeiras(exposicoes):
    unicas = exposicoes.drop_duplicates("id_evento")
    return unicas.sort_values(["momento", "id_evento"]).drop_duplicates("id_visita")


def checar(eventos):
    """Dicionário com o conjunto de ids de cada falha:
    reenvio (id_evento de exposição repetido), troca_de_grupo (id_visita com os dois grupos),
    compra_com_id_trocado (id_evento da compra cuja sessão viu o checkout com outro id_visita) e
    compra_sem_exposicao (id_evento da compra de uma sessão que não viu o checkout)."""
    exposicoes, compras = _partes(eventos)
    reenvio = set(exposicoes.loc[exposicoes.duplicated("id_evento"), "id_evento"])
    unicas = exposicoes.drop_duplicates("id_evento")
    grupos = unicas.groupby("id_visita")["grupo"].nunique()
    troca = set(grupos[grupos > 1].index)
    primeiras = _primeiras(exposicoes)
    sem_id = compras[~compras["id_visita"].isin(primeiras["id_visita"])]
    pela_sessao = sem_id["id_sessao"].isin(primeiras["id_sessao"])
    return {"reenvio": reenvio,
            "troca_de_grupo": troca,
            "compra_com_id_trocado": set(sem_id.loc[pela_sessao, "id_evento"]),
            "compra_sem_exposicao": set(sem_id.loc[~pela_sessao, "id_evento"])}


def tabela_de_visitas(eventos):
    """Uma linha por visita que viu o checkout: id_visita, grupo do primeiro sorteio e
    converteu (1 se comprou, pelo id da visita ou pela sessão). Compra de fora do teste fica de fora."""
    exposicoes, compras = _partes(eventos)
    primeiras = _primeiras(exposicoes)
    visita_da_sessao = primeiras.set_index("id_sessao")["id_visita"]
    pelo_id = compras["id_visita"].where(compras["id_visita"].isin(primeiras["id_visita"]))
    visita = pelo_id.fillna(compras["id_sessao"].map(visita_da_sessao))
    visitas = primeiras[["id_visita", "grupo"]].reset_index(drop=True)
    visitas["converteu"] = visitas["id_visita"].isin(visita.dropna()).astype(int)
    return visitas


def _novos_ids(rng, quantos, usados, largura):
    saida = []
    while len(saida) < quantos:
        s = format(int(rng.integers(0, 16 ** largura)), f"0{largura}x")
        if s not in usados:
            usados.add(s)
            saida.append(s)
    return saida


def semana_sintetica(n_visitas, taxa, rng, inicio="2026-03-02"):
    """n_visitas em 7 dias, meio a meio entre A e B, cada uma com chance `taxa` de comprar.
    Nenhuma falha: um evento por exposição, um id por visita, uma compra por comprador."""
    if n_visitas < 2:
        raise ValueError("a semana precisa de pelo menos duas visitas")
    if not 0 < taxa < 1:
        raise ValueError(f"taxa precisa ficar entre 0 e 1 (10% é 0.10), veio {taxa}")
    usados = set()
    v = _novos_ids(rng, n_visitas, usados, 8)
    s = _novos_ids(rng, n_visitas, usados, 8)
    e = _novos_ids(rng, 2 * n_visitas, usados, 10)
    zero = dt.datetime.fromisoformat(inicio)
    segundos = rng.uniform(0, 7 * 86400, size=n_visitas)
    grupos = rng.choice(["A", "B"], size=n_visitas)
    compra = rng.random(n_visitas) < taxa
    linhas = []
    for i in range(n_visitas):
        t = zero + dt.timedelta(seconds=float(segundos[i]))
        linhas.append([t, e[i], v[i], s[i], "exposicao", grupos[i]])
        if compra[i]:
            linhas.append([t + dt.timedelta(minutes=5), e[n_visitas + i], v[i], s[i], "compra", None])
    return pd.DataFrame(linhas, columns=COLUNAS).sort_values("momento").reset_index(drop=True)


def plantar(eventos, rng, reenvio_b=0, troca=0, login=0, sem_exposicao=0):
    """Cópia dos eventos com falhas novas, cada uma numa visita diferente e limpa, e o dicionário
    com os ids plantados, no mesmo formato de checar()."""
    antes = checar(eventos)
    exposicoes, compras = _partes(eventos)
    primeiras = _primeiras(exposicoes)
    sujas = set(antes["troca_de_grupo"]) | set(exposicoes.loc[exposicoes["id_evento"].isin(antes["reenvio"]), "id_visita"])
    limpas = primeiras[~primeiras["id_visita"].isin(sujas)]
    usados = set(eventos["id_evento"]) | set(eventos["id_visita"]) | set(eventos["id_sessao"])
    novas, plantadas = [], {k: set() for k in antes}
    ocupadas = set()

    def sortear_linhas(tabela, quantos, nome):
        livres = tabela[~tabela["id_visita"].isin(ocupadas)]
        if quantos > len(livres):
            raise ValueError(f"{nome}: pediu {quantos}, só há {len(livres)} visitas limpas")
        pegas = livres.iloc[sorted(rng.choice(len(livres), size=quantos, replace=False))] if quantos else livres.iloc[:0]
        ocupadas.update(pegas["id_visita"])
        return pegas

    for _, r in sortear_linhas(limpas[limpas["grupo"] == "B"], reenvio_b, "reenvio_b").iterrows():
        novas.append([r["momento"] + pd.Timedelta(seconds=2), r["id_evento"], r["id_visita"], r["id_sessao"], "exposicao", "B"])
        plantadas["reenvio"].add(r["id_evento"])
    trocas = sortear_linhas(limpas, troca, "troca")
    for (_, r), e in zip(trocas.iterrows(), _novos_ids(rng, len(trocas), usados, 10)):
        outro = "B" if r["grupo"] == "A" else "A"
        novas.append([r["momento"] + pd.Timedelta(seconds=60), e, r["id_visita"], r["id_sessao"], "exposicao", outro])
        plantadas["troca_de_grupo"].add(r["id_visita"])
    saida = eventos.copy()
    compradores = limpas[limpas["id_visita"].isin(compras["id_visita"])]
    logins = sortear_linhas(compradores, login, "login")
    for visita, novo in zip(logins["id_visita"], _novos_ids(rng, len(logins), usados, 8)):
        linha = (saida["evento"] == "compra") & (saida["id_visita"] == visita)
        plantadas["compra_com_id_trocado"].update(saida.loc[linha, "id_evento"])
        saida.loc[linha, "id_visita"] = novo
    if sem_exposicao:
        v = _novos_ids(rng, sem_exposicao, usados, 8)
        s = _novos_ids(rng, sem_exposicao, usados, 8)
        e = _novos_ids(rng, sem_exposicao, usados, 10)
        momentos = eventos["momento"].sample(sem_exposicao, random_state=int(rng.integers(0, 2 ** 31))).tolist()
        for i in range(sem_exposicao):
            novas.append([momentos[i], e[i], v[i], s[i], "compra", None])
            plantadas["compra_sem_exposicao"].add(e[i])
    if novas:
        saida = pd.concat([saida, pd.DataFrame(novas, columns=COLUNAS)], ignore_index=True)
    saida = saida.sort_values(["momento", "id_evento"]).reset_index(drop=True)
    return saida, {k: antes[k] | plantadas[k] for k in antes}
