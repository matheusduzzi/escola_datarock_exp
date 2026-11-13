"""Gera os dois testes da aula 13: o do checkout e o da calculadora de frete.

Rode de dentro da pasta da aula:  python3 gerar_dados.py
Só usa a biblioteca padrão. Os arquivos saem iguais toda vez.

Como os dados nascem (abra depois de fazer as contas da aula):

Checkout em uma página (B) contra o checkout de hoje (A).
- 20.000 visitas no site e 10.000 no app. O sorteio põe 50% no B no site e 20% no B no app.
- Compra na visita, no A: 4,0% no site e 12,0% no app. No B: 4,8% no site e 13,2% no app.
  Cliente recorrente compra 1,15 vez a taxa do canal; cliente novo, 0,72 vez.
- Chegar ao pagamento, no A: 10% no site e 25% no app. No B: 14% e 31%.
  Só compra quem chegou ao pagamento.
- Região, origem, período e dia são sorteados sem nenhuma ligação com o grupo ou com a compra.

Calculadora de frete na página do produto (B) contra a página de hoje (A).
- Semana 1: 15.000 visitas, 10% no B. Semana 2: 25.000 visitas, 50% no B.
- Compra no A: 5,0% na semana 1 e 9,0% na semana 2. Mesmos pesos de cliente novo e recorrente.
- Efeito do B, em pontos da taxa da semana: +0,5 ponto no cliente novo e -0,6 ponto no recorrente,
  vezes a taxa da semana dividida por 7,0%.
- A calculadora só existe no B. Quem comprou usou a calculadora 70 vezes em 100; quem não comprou, 27.
- Região, categoria e dispositivo são sorteados sem ligação com o grupo ou com a compra.
"""
import csv
import random
from pathlib import Path

AQUI = Path(__file__).resolve().parent
SORTEIO_CHECKOUT = 16
SORTEIO_FRETE = 190

REGIOES = [("Sudeste", 0.45), ("Nordeste", 0.22), ("Sul", 0.15), ("Centro-Oeste", 0.09), ("Norte", 0.09)]
CLIENTE = [("recorrente", 0.65), ("novo", 0.35)]
PESO_CLIENTE = {"recorrente": 1.15, "novo": 0.72}


def escolher(rng, opcoes):
    x = rng.random()
    acumulado = 0.0
    for valor, peso in opcoes:
        acumulado += peso
        if x < acumulado:
            return valor
    return opcoes[-1][0]


def checkout(semente):
    rng = random.Random(semente)
    canais = {"site": (20000, 0.5, 0.040, 0.048, 0.10, 0.14), "app": (10000, 0.2, 0.120, 0.132, 0.25, 0.31)}
    linhas = []
    for canal, (n, parte_b, compra_a, compra_b, pag_a, pag_b) in canais.items():
        for _ in range(n):
            grupo = "B" if rng.random() < parte_b else "A"
            cliente = escolher(rng, CLIENTE)
            linha = {
                "canal": canal, "grupo": grupo,
                "regiao": escolher(rng, REGIOES), "cliente": cliente,
                "origem": escolher(rng, [("busca", 0.40), ("anuncio", 0.25), ("direto", 0.20), ("email", 0.15)]),
                "periodo": escolher(rng, [("tarde", 0.40), ("noite", 0.35), ("manha", 0.25)]),
                "dia": escolher(rng, [("util", 0.72), ("fim_de_semana", 0.28)]),
            }
            compra = (compra_b if grupo == "B" else compra_a) * PESO_CLIENTE[cliente]
            pagamento = pag_b if grupo == "B" else pag_a
            chegou = rng.random() < pagamento
            comprou = chegou and rng.random() < compra / pagamento
            linha["chegou_pagamento"] = int(chegou)
            linha["comprou"] = int(comprou)
            linhas.append(linha)
    rng.shuffle(linhas)
    for i, linha in enumerate(linhas, 1):
        linha["id_visita"] = f"c{i:05d}"
    return linhas


def frete(semente):
    rng = random.Random(semente)
    semanas = {1: (15000, 0.10, 0.050), 2: (25000, 0.50, 0.090)}
    efeito = {"novo": 0.005, "recorrente": -0.006}
    linhas = []
    for semana, (n, parte_b, compra_a) in semanas.items():
        for _ in range(n):
            grupo = "B" if rng.random() < parte_b else "A"
            cliente = escolher(rng, CLIENTE)
            linha = {
                "semana": semana, "grupo": grupo, "cliente": cliente, "regiao": escolher(rng, REGIOES),
                "categoria": escolher(rng, [("roupas", 0.40), ("calcados", 0.25), ("casa", 0.20), ("beleza", 0.15)]),
                "dispositivo": escolher(rng, [("celular", 0.62), ("computador", 0.31), ("tablet", 0.07)]),
            }
            taxa = compra_a * PESO_CLIENTE[cliente]
            if grupo == "B":
                taxa += efeito[cliente] * compra_a / 0.07
            comprou = rng.random() < taxa
            if grupo == "B":
                linha["usou_calculadora"] = int(rng.random() < (0.70 if comprou else 0.27))
            else:
                linha["usou_calculadora"] = ""
            linha["comprou"] = int(comprou)
            linhas.append(linha)
    rng.shuffle(linhas)
    for i, linha in enumerate(linhas, 1):
        linha["id_visita"] = f"f{i:05d}"
    return linhas


def gravar(nome, linhas, colunas):
    with open(AQUI / nome, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=colunas, lineterminator="\n")
        w.writeheader()
        for linha in sorted(linhas, key=lambda x: x["id_visita"]):
            w.writerow(linha)


if __name__ == "__main__":
    c = checkout(SORTEIO_CHECKOUT)
    gravar("visitas_checkout.csv", c, ["id_visita", "canal", "grupo", "regiao", "cliente", "origem", "periodo", "dia",
                                       "chegou_pagamento", "comprou"])
    f = frete(SORTEIO_FRETE)
    gravar("visitas_frete.csv", f, ["id_visita", "semana", "grupo", "cliente", "regiao", "categoria", "dispositivo",
                                    "usou_calculadora", "comprou"])
    print(f"visitas_checkout={len(c)} visitas_frete={len(f)}")
