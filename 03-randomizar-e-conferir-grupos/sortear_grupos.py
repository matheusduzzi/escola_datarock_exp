"""Aplica as regras do plano, sorteia quem entra e grava as duas tabelas.

    python3 sortear_grupos.py regras_retire

Grava saida/<nome do teste>/alocacao.csv e exclusoes.csv e mostra o resumo.
"""
import importlib
import sys
from collections import Counter
from pathlib import Path

import grupos


def main(nome_plano):
    plano = importlib.import_module(nome_plano)
    clientes = grupos.ler_clientes(plano.CLIENTES)
    elegiveis, exclusoes = grupos.aplicar_regras(clientes, plano.REGRAS)
    alocacao = grupos.alocar(elegiveis, plano.NOME_TESTE)

    pasta = Path("saida") / plano.NOME_TESTE
    pasta.mkdir(parents=True, exist_ok=True)
    grupos.salvar_tabela(pasta / "alocacao.csv", alocacao, grupos.CAMPOS_ALOCACAO)
    grupos.salvar_tabela(pasta / "exclusoes.csv", exclusoes, grupos.CAMPOS_EXCLUSAO)

    por_regra = Counter(e["regra"] for e in exclusoes)
    ordem = [grupos.SEM_ID[0], grupos.REPETIDA[0]] + [r.codigo for r in plano.REGRAS]
    por_grupo = Counter(a["grupo"] for a in alocacao)
    m = grupos.milhar
    print(f"Teste {plano.NOME_TESTE}: {m(len(clientes))} linhas na lista")
    print(f"  saíram {m(len(exclusoes))}:", ", ".join(f"{k} {por_regra[k]}" for k in ordem))
    print(f"  entraram {m(len(elegiveis))}: A {m(por_grupo['A'])}, B {m(por_grupo['B'])}")
    print(f"  gravado em {pasta}/alocacao.csv e {pasta}/exclusoes.csv")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("uso: python3 sortear_grupos.py <arquivo do plano sem o .py>, por exemplo regras_retire")
    nome = sys.argv[1]
    main(nome[:-3] if nome.endswith(".py") else nome)
