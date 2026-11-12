"""Contas da aula «Randomizar e conferir grupos».

    Regra(codigo, coluna, motivo, passa)       uma regra de quem pode entrar no teste
    ler_clientes(caminho)                      lê a lista de contas, com tudo como texto
    aplicar_regras(clientes, regras)           separa quem entra de quem sai, com o motivo
    sortear(id_cliente, nome_teste)            A ou B, sempre o mesmo para o mesmo id e o mesmo teste
    alocar(elegiveis, nome_teste)              a tabela de alocação: um grupo por conta
    p_divisao(n_a, n_b)                        a divisão meio a meio está em ordem? (p de dois lados)
    milhar(n), virgula(x)                      números escritos como na aula: 9.000 e 0,78
    equilibrio(elegiveis, alocacao, colunas)   média de cada coluna de antes do teste, por grupo
    conferir(plano, alocacao, exclusoes)       refaz tudo a partir da lista e diz o que não bate

Só usa a biblioteca padrão do Python.
"""
import csv
import hashlib
import math
import random
from collections import namedtuple
from statistics import NormalDist

Regra = namedtuple("Regra", "codigo coluna motivo passa")
SEM_ID = ("sem-id", "id_cliente", "Sem id não dá para sortear nem ligar a compra ao grupo.")
REPETIDA = ("repetida", "id_cliente", "A mesma conta já apareceu numa linha anterior; ela entra uma vez só.")
CAMPOS_ALOCACAO = ["id_cliente", "teste", "grupo"]
CAMPOS_EXCLUSAO = ["linha", "id_cliente", "regra", "coluna", "valor", "motivo"]


def ler_clientes(caminho):
    """Uma lista de dicionários, um por linha, com o número da linha do arquivo (o cabeçalho é a 1)."""
    with open(caminho, newline="", encoding="utf-8") as f:
        leitor = csv.DictReader(f)
        colunas = leitor.fieldnames or []
        if "id_cliente" not in colunas:
            raise ValueError(f"o arquivo {caminho} não tem a coluna id_cliente; colunas: {colunas}")
        clientes = []
        for numero, linha in enumerate(leitor, start=2):
            linha = {k: (v or "").strip() for k, v in linha.items()}
            linha["_linha"] = numero
            clientes.append(linha)
    return clientes


def aplicar_regras(clientes, regras):
    """(elegiveis, exclusoes). Cada linha sai pela primeira regra em que falha.
    Antes das regras do plano, duas que valem para todo teste: id vazio e conta repetida."""
    if not clientes:
        raise ValueError("a lista de clientes está vazia")
    colunas = set(clientes[0])
    for r in regras:
        if r.coluna not in colunas:
            raise ValueError(f"a regra {r.codigo!r} usa a coluna {r.coluna!r}, que não está no arquivo")
        if not r.motivo.strip():
            raise ValueError(f"a regra {r.codigo!r} está sem motivo")
    codigos = [SEM_ID[0], REPETIDA[0]] + [r.codigo for r in regras]
    if len(set(codigos)) != len(codigos):
        raise ValueError(f"código de regra repetido: {codigos}")

    elegiveis, exclusoes, vistos = [], [], set()
    for c in clientes:
        id_cliente = c["id_cliente"]
        saiu = None
        if not id_cliente:
            saiu = SEM_ID
        elif id_cliente in vistos:
            saiu = REPETIDA
        else:
            vistos.add(id_cliente)
            for r in regras:
                if not r.passa(c[r.coluna]):
                    saiu = (r.codigo, r.coluna, r.motivo)
                    break
        if saiu:
            codigo, coluna, motivo = saiu
            exclusoes.append({"linha": c["_linha"], "id_cliente": id_cliente, "regra": codigo,
                              "coluna": coluna, "valor": c[coluna], "motivo": motivo})
        else:
            elegiveis.append(c)
    return elegiveis, exclusoes


def sortear(id_cliente, nome_teste):
    """A ou B pelo resumo SHA-256 do nome do teste com o id do cliente.
    O mesmo id dá sempre o mesmo grupo, em qualquer ordem da lista e em qualquer computador."""
    if not isinstance(nome_teste, str) or not nome_teste.strip():
        raise ValueError(f"nome do teste vazio: ele entra na conta do sorteio, veio {nome_teste!r}")
    if not isinstance(id_cliente, str) or not id_cliente.strip():
        raise ValueError(f"id_cliente vazio: não dá para sortear, veio {id_cliente!r}")
    resumo = hashlib.sha256(f"{nome_teste}:{id_cliente}".encode("utf-8")).digest()
    return "A" if resumo[0] % 2 == 0 else "B"


def alocar(elegiveis, nome_teste):
    """A tabela de alocação, na ordem da lista: id_cliente, teste e grupo."""
    return [{"id_cliente": c["id_cliente"], "teste": nome_teste,
             "grupo": sortear(c["id_cliente"], nome_teste)} for c in elegiveis]


def p_divisao(n_a, n_b):
    """p de dois lados para a divisão n_a contra n_b, se o sorteio for meio a meio."""
    n = n_a + n_b
    if n_a < 0 or n_b < 0 or n == 0:
        raise ValueError(f"contagens inválidas: {n_a} e {n_b}")
    z = (n_b - n / 2) / math.sqrt(n / 4)
    return 2 * (1 - NormalDist().cdf(abs(z)))


def _numero(valor):
    if valor in ("sim", "nao"):
        return 1.0 if valor == "sim" else 0.0
    return float(valor)


def equilibrio(elegiveis, alocacao, colunas):
    """Para cada coluna: média no A, média no B e a diferença em desvios padrão.
    Colunas sim/nao viram a parte de "sim"."""
    grupo = {a["id_cliente"]: a["grupo"] for a in alocacao}
    linhas = []
    for col in colunas:
        val = {"A": [], "B": []}
        for c in elegiveis:
            val[grupo[c["id_cliente"]]].append(_numero(c[col]))
        media = {g: sum(v) / len(v) for g, v in val.items()}
        var = {g: sum((x - media[g]) ** 2 for x in v) / (len(v) - 1) for g, v in val.items()}
        dp = math.sqrt((var["A"] + var["B"]) / 2)
        dif = 0.0 if dp == 0 else (media["B"] - media["A"]) / dp
        linhas.append((col, media["A"], media["B"], dif))
    return linhas


def milhar(n):
    """9000 vira 9.000, como o texto da aula escreve."""
    return f"{n:,}".replace(",", ".")


def virgula(x, casas=2):
    """0.78 vira 0,78."""
    return f"{x:.{casas}f}".replace(".", ",")


def ler_tabela(caminho):
    with open(caminho, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def salvar_tabela(caminho, linhas, campos):
    with open(caminho, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=campos, lineterminator="\n")
        w.writeheader()
        w.writerows(linhas)


def conferir(plano, alocacao, exclusoes, embaralhar=7):
    """Refaz regras e sorteio a partir da lista do plano e compara com as duas tabelas.
    Retorna a lista de problemas (vazia se está tudo certo)."""
    clientes = ler_clientes(plano.CLIENTES)
    elegiveis, refeitas = aplicar_regras(clientes, plano.REGRAS)
    problemas = []

    sem_motivo = [e for e in exclusoes if not (e.get("regra") or "").strip() or not (e.get("motivo") or "").strip()]
    for e in sem_motivo:
        problemas.append(f"exclusão sem regra ou sem motivo na linha {e.get('linha')} ({e.get('id_cliente')!r})")

    if len(alocacao) + len(exclusoes) != len(clientes):
        problemas.append(f"a lista tem {len(clientes)} linhas, mas alocação ({len(alocacao)}) "
                         f"mais exclusões ({len(exclusoes)}) somam {len(alocacao) + len(exclusoes)}")

    ids_aloc = [a["id_cliente"] for a in alocacao]
    if len(set(ids_aloc)) != len(ids_aloc):
        problemas.append("a mesma conta aparece mais de uma vez na alocação")
    excluidas = {(e["id_cliente"], str(e["linha"])) for e in exclusoes}
    esperadas = {(e["id_cliente"], str(e["linha"])) for e in refeitas}
    for id_cliente, linha in sorted(excluidas - esperadas):
        problemas.append(f"a linha {linha} ({id_cliente!r}) está nas exclusões, mas passa nas regras do plano")
    for id_cliente, linha in sorted(esperadas - excluidas):
        problemas.append(f"a linha {linha} ({id_cliente!r}) falha numa regra do plano e não está nas exclusões")
    saiu_e_entrou = {e["id_cliente"] for e in exclusoes if e["regra"] != REPETIDA[0]} & set(ids_aloc)
    for id_cliente in sorted(saiu_e_entrou):
        problemas.append(f"a conta {id_cliente} está nas exclusões e na alocação")
    elegiveis_ids = {c["id_cliente"] for c in elegiveis}
    for id_cliente in sorted(set(ids_aloc) - elegiveis_ids):
        problemas.append(f"a conta {id_cliente} está na alocação, mas não é elegível pelo plano")

    for a in alocacao:
        if a.get("teste") != plano.NOME_TESTE:
            problemas.append(f"a conta {a['id_cliente']} está com o teste {a.get('teste')!r}, e o plano é {plano.NOME_TESTE!r}")
        elif a["id_cliente"] and a.get("grupo") != sortear(a["id_cliente"], plano.NOME_TESTE):
            problemas.append(f"a conta {a['id_cliente']} está no grupo {a.get('grupo')!r}, e o sorteio dá "
                             f"{sortear(a['id_cliente'], plano.NOME_TESTE)}")

    referencia = {a["id_cliente"]: a["grupo"] for a in alocar(elegiveis, plano.NOME_TESTE)}
    for rodada in range(embaralhar):
        outra = clientes[:]
        random.Random(rodada).shuffle(outra)
        elegiveis_2, _ = aplicar_regras(outra, plano.REGRAS)
        if {a["id_cliente"]: a["grupo"] for a in alocar(elegiveis_2, plano.NOME_TESTE)} != referencia:
            problemas.append(f"com a lista em outra ordem (rodada {rodada}), os grupos mudaram")
            break
    return problemas
