"""Confere as duas tabelas gravadas por sortear_grupos.py contra o plano.

    python3 conferir_grupos.py regras_retire

Refaz as regras e o sorteio a partir da lista, embaralha a lista e sorteia de novo, mostra a
divisão e o equilíbrio das colunas de antes do início. Sai com código 1 se algo não bate.
"""
import importlib
import sys
from collections import Counter
from pathlib import Path

import grupos


def main(nome_plano):
    plano = importlib.import_module(nome_plano)
    pasta = Path("saida") / plano.NOME_TESTE
    alocacao = grupos.ler_tabela(pasta / "alocacao.csv")
    exclusoes = grupos.ler_tabela(pasta / "exclusoes.csv")
    problemas = grupos.conferir(plano, alocacao, exclusoes)

    n = Counter(a["grupo"] for a in alocacao)
    m, v = grupos.milhar, grupos.virgula
    print(f"Divisão: A {m(n['A'])}, B {m(n['B'])}, p = {v(grupos.p_divisao(n['A'], n['B']))}")
    if not problemas:
        clientes = grupos.ler_clientes(plano.CLIENTES)
        elegiveis, _ = grupos.aplicar_regras(clientes, plano.REGRAS)
        print("Antes do início      média A  média B  diferença (desvios padrão)")
        for col, ma, mb, dif in grupos.equilibrio(elegiveis, alocacao, plano.EQUILIBRIO):
            sinal = "+" if dif >= 0 else "-"
            print(f"  {col:<18} {v(ma):>7}  {v(mb):>7}  {sinal}{v(abs(dif), 3)}")
        print("Nenhum problema: as tabelas batem com o plano, e a lista em outra ordem dá os mesmos grupos.")
        return 0
    print(f"{len(problemas)} problema(s):")
    for p in problemas[:20]:
        print(" ", p)
    if len(problemas) > 20:
        print(f"  ... e mais {len(problemas) - 20}")
    return 1


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("uso: python3 conferir_grupos.py <arquivo do plano sem o .py>, por exemplo regras_retire")
    nome = sys.argv[1]
    sys.exit(main(nome[:-3] if nome.endswith(".py") else nome))
