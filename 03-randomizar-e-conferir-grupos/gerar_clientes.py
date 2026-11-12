"""Gera dados/clientes_retire.csv, a lista de contas que a Lia mandou para o teste do "Retire hoje".

O arquivo imita o export do cadastro tirado no domingo, 01/02/2026, véspera do início do teste:
uma linha por conta, ordenada como o export sai (mais pedidos primeiro). O gerador só usa a
biblioteca padrão e sai igual toda vez.

O que vai no arquivo:
- 9.000 contas que passam nas regras do plano;
- 214 contas ativas sem acesso nos 30 dias antes do início;
- 118 contas encerradas ou bloqueadas (3 delas também são de funcionário);
- 58 contas internas ativas: 41 de funcionário e 17 de teste do time;
- 6 linhas repetidas (a mesma conta duas vezes, linha igual);
- 4 linhas com o id vazio.
"""
import csv
import datetime as dt
import random
from pathlib import Path

PASTA = Path(__file__).resolve().parent
SAIDA = PASTA / "dados" / "clientes_retire.csv"
COLUNAS = ["id_cliente", "status", "tipo", "cadastro", "ultimo_acesso", "pedidos_90d",
           "mora_perto", "usou_retirada"]
EXPORT = dt.date(2026, 2, 1)       # dia em que o export foi tirado
JANELA = 30                        # acessos de 03/01 a 01/02 contam como "entrou no mês anterior"


def dia(d):
    return d.isoformat()


def conta(rng, numero, ativo_no_mes=True):
    """Uma conta. Quem é cliente há mais tempo tende a ter mais pedidos e a morar perto."""
    cadastro = dt.date(2019, 1, 1) + dt.timedelta(days=int(numero * 0.27) + rng.randrange(0, 20))
    if cadastro > EXPORT - dt.timedelta(days=40):
        cadastro = EXPORT - dt.timedelta(days=40 + rng.randrange(0, 30))
    anos = (EXPORT - cadastro).days / 365
    if ativo_no_mes:
        ultimo = EXPORT - dt.timedelta(days=rng.randrange(0, JANELA))
    else:
        ultimo = EXPORT - dt.timedelta(days=rng.randrange(JANELA, 400))
    media = 0.6 + 0.45 * anos
    pedidos = 0
    while pedidos < 15 and rng.random() < media / (media + 1):
        pedidos += 1
    perto = rng.random() < 0.30 + 0.03 * anos
    retirada = rng.random() < 0.15 + 0.03 * anos
    return {"id_cliente": f"C{10000 + numero}", "status": "ativa", "tipo": "cliente",
            "cadastro": dia(cadastro), "ultimo_acesso": dia(ultimo), "pedidos_90d": pedidos,
            "mora_perto": "sim" if perto else "nao", "usou_retirada": "sim" if retirada else "nao"}


def gerar():
    rng = random.Random(20260201)
    numeros = list(range(1, 9395))
    rng.shuffle(numeros)
    linhas = []
    fila = iter(numeros)

    for _ in range(9000):
        linhas.append(conta(rng, next(fila)))
    for _ in range(214):
        linhas.append(conta(rng, next(fila), ativo_no_mes=False))
    for i in range(118):
        c = conta(rng, next(fila), ativo_no_mes=rng.random() < 0.5)
        c["status"] = "encerrada" if i % 3 else "bloqueada"
        if i < 3:
            c["tipo"] = "funcionario"
        linhas.append(c)
    for i in range(58):
        c = conta(rng, next(fila))
        c["tipo"] = "funcionario" if i < 41 else "teste"
        if c["tipo"] == "teste":
            c["pedidos_90d"] = rng.randrange(8, 40)
        linhas.append(c)
    for _ in range(4):
        c = conta(rng, next(fila))
        c["id_cliente"] = ""
        linhas.append(c)
    repetidas = rng.sample(linhas[:9000], 6)
    linhas.extend(dict(c) for c in repetidas)

    sobra = list(fila)
    assert sobra == [], sobra
    linhas.sort(key=lambda c: (-c["pedidos_90d"], c["cadastro"], c["id_cliente"]))
    SAIDA.parent.mkdir(exist_ok=True)
    with SAIDA.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLUNAS, lineterminator="\n")
        w.writeheader()
        w.writerows(linhas)
    return len(linhas)


if __name__ == "__main__":
    print(f"clientes_retire.csv: {gerar()} linhas")
