"""Quatro jeitos de dividir as 9.000 contas do "Retire hoje" e o que acontece com cada um.

    python3 jeitos_de_sortear.py

Para cada jeito, o programa refaz a divisão em três situações e conta quantas das 9.000 contas
mudaram de grupo: rodar de novo, a lista vir em outra ordem e entrar uma conta nova no começo.

O jeito 3 roda o Python duas vezes, como dois dias de trabalho. Cada vez que o Python abre, ele
escolhe por conta própria a mistura do hash() de textos. Para a saída deste programa sair igual
em todo computador, ele fixa essa escolha em 1 e em 2 pela variável PYTHONHASHSEED. Sem isso,
o número muda a cada rodada, mas fica sempre perto da metade.
"""
import os
import random
import subprocess
import sys

import grupos
import regras_retire as plano


def metade_de_cima(ids):
    meio = len(ids) // 2
    return {i: ("B" if k < meio else "A") for k, i in enumerate(ids)}


def embaralhar(ids, numero=2026):
    copia = list(ids)
    random.Random(numero).shuffle(copia)
    meio = len(copia) // 2
    return {i: ("A" if k < meio else "B") for k, i in enumerate(copia)}


def hash_embutido(ids, mistura):
    """Roda outro Python, com a mistura do hash() fixada, e traz os grupos de volta."""
    codigo = ("import sys\n"
              "ids = sys.stdin.read().split()\n"
              "print(''.join('A' if hash('retire-hoje:' + i) % 2 == 0 else 'B' for i in ids))")
    env = dict(os.environ, PYTHONHASHSEED=str(mistura))
    saida = subprocess.run([sys.executable, "-c", codigo], input="\n".join(ids),
                           capture_output=True, text=True, env=env, check=True).stdout.strip()
    return dict(zip(ids, saida))


def sha256(ids, nome_teste="retire-hoje"):
    return {i: grupos.sortear(i, nome_teste) for i in ids}


def mudaram(antes, depois):
    return sum(antes[i] != depois[i] for i in antes)


def pct(n, total):
    return grupos.virgula(100 * n / total, 1) + "%"


def main():
    clientes = grupos.ler_clientes(plano.CLIENTES)
    elegiveis, _ = grupos.aplicar_regras(clientes, plano.REGRAS)
    ids = [c["id_cliente"] for c in elegiveis]          # na ordem do export: mais pedidos primeiro
    outra_ordem = sorted(ids)                           # a mesma lista, ordenada pelo id
    com_nova = ["C99999"] + ids                         # uma conta nova no começo
    total = len(ids)
    pedidos = {c["id_cliente"]: int(c["pedidos_90d"]) for c in elegiveis}

    def media_pedidos(g):
        a = [pedidos[i] for i in ids if g[i] == "A"]
        b = [pedidos[i] for i in ids if g[i] == "B"]
        return grupos.virgula(sum(a) / len(a)), grupos.virgula(sum(b) / len(b))

    m = grupos.milhar
    print(f"{m(total)} contas elegíveis. Quantas delas mudam de grupo quando:")
    print(f"{'':32}{'rodo de novo':>14}{'outra ordem':>14}{'conta nova':>13}")

    jeitos = [
        ("1. metade de cima vai para o B", metade_de_cima, metade_de_cima, metade_de_cima),
        ("2. embaralhar com número fixo", embaralhar, embaralhar, embaralhar),
        ("3. hash() do Python", lambda x: hash_embutido(x, 1), lambda x: hash_embutido(x, 2),
         lambda x: hash_embutido(x, 2)),
        ("4. SHA-256 do teste com o id", sha256, sha256, sha256),
    ]
    divisoes = {}
    for nome, primeira, segunda, _ in jeitos:
        g = primeira(ids)
        divisoes[nome] = g
        de_novo = mudaram(g, segunda(ids))
        ordem = mudaram(g, segunda(outra_ordem))
        nova = mudaram(g, {i: v for i, v in segunda(com_nova).items() if i != "C99999"})
        print(f"{nome:<32}{m(de_novo):>14}{m(ordem):>14}{m(nova):>13}")

    print("Média de pedidos nos 90 dias antes, A e B:")
    for nome, g in divisoes.items():
        a, b = media_pedidos(g)
        print(f"  {nome:<32}A {a}   B {b}")
    outro_teste = mudaram(sha256(ids), sha256(ids, "frete-gratis"))
    print(f"SHA-256 com outro nome de teste (frete-gratis): {pct(outro_teste, total)} das contas em grupo diferente")


if __name__ == "__main__":
    main()
