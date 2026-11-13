"""Gera os dois testes A/B da Loja Exemplo usados no curso Experimentação e teste A/B.

Só biblioteca padrão (Python 3.9 ou mais novo). Rodar duas vezes dá os mesmos arquivos, byte a byte.

    python3 gerar.py                 # escreve nesta pasta
    python3 gerar.py --saida /tmp/x  # escreve em outra pasta

Como os dados nascem (o mecanismo):
- cada teste tem 12.000 visitas; o sorteio põe 6.000 no grupo A e 6.000 no grupo B;
- cada visita compra ou não com uma taxa fixa do seu grupo, sorteada de forma independente;
- ab_botao.csv: taxa de 10,0% no A e 11,5% no B (efeito pequeno e real de 1,5 ponto);
- ab_frete.csv: taxa de 10,0% nos dois grupos (efeito nenhum);
- em cada arquivo, 7 visitas perdem o grupo depois do sorteio (erro de registro).

Hipóteses que o gerador assume e uma loja de verdade não garante: visitas independentes, uma
visita por pessoa, taxa constante ao longo do teste e nenhuma visita trocando de grupo.

Os sorteios seguem a mesma sequência do gerador antigo dos dados de estatística: antes dos testes
A/B, ele sorteia 400 tíquetes e 48 entregas. Esses sorteios são refeitos aqui e descartados, para
que ab_botao.csv e ab_frete.csv saiam iguais aos arquivos que já existiam.
"""
import argparse
import csv
import math
import pathlib
import random

SEMENTE = 42

# Sorteios anteriores do gerador antigo (refeitos e descartados para manter a sequência).
CANAIS = [("site", 240, 120.0, 0.35), ("loja_fisica", 160, 85.0, 0.30)]
N_ENTREGAS, HORAS_MEDIA, HORAS_DP, N_ENTREGA_SEM_BAIXA = 48, 46.0, 9.0, 3

N_POR_GRUPO = 6000
N_SEM_GRUPO = 7
TESTES_AB = {
    # arquivo: (taxa do grupo A, taxa do grupo B)
    "ab_botao.csv": (0.100, 0.115),
    "ab_frete.csv": (0.100, 0.100),
}


def descartar_sorteios_anteriores(rng):
    linhas = []
    for _canal, n, mediana, espalhamento in CANAIS:
        for _ in range(n):
            linhas.append(math.exp(rng.gauss(math.log(mediana), espalhamento)))
    rng.shuffle(linhas)
    for _ in range(N_ENTREGAS):
        rng.gauss(HORAS_MEDIA, HORAS_DP)
    rng.sample(range(N_ENTREGAS), N_ENTREGA_SEM_BAIXA)


def gerar_ab(rng, taxa_a, taxa_b):
    grupos = ["A"] * N_POR_GRUPO + ["B"] * N_POR_GRUPO
    rng.shuffle(grupos)
    linhas = []
    for i, g in enumerate(grupos):
        taxa = taxa_a if g == "A" else taxa_b
        linhas.append([i + 1, g, 1 if rng.random() < taxa else 0])
    for i in rng.sample(range(len(linhas)), N_SEM_GRUPO):
        linhas[i][1] = ""
    return linhas


def gerar(saida):
    rng = random.Random(SEMENTE)
    saida.mkdir(parents=True, exist_ok=True)
    descartar_sorteios_anteriores(rng)
    resumo = {}
    for nome, (taxa_a, taxa_b) in TESTES_AB.items():
        linhas = gerar_ab(rng, taxa_a, taxa_b)
        with open(saida / nome, "w", encoding="utf-8", newline="") as f:
            w = csv.writer(f, lineterminator="\n")
            w.writerow(["id_visita", "grupo", "converteu"])
            w.writerows(linhas)
        resumo[nome[:-4]] = len(linhas)
    resumo["visitas_sem_grupo_por_teste"] = N_SEM_GRUPO
    return resumo


def main():
    parser = argparse.ArgumentParser(description="Gera os testes A/B da Loja Exemplo.")
    parser.add_argument("--saida", default=str(pathlib.Path(__file__).resolve().parent))
    args = parser.parse_args()
    resumo = gerar(pathlib.Path(args.saida))
    print(" ".join("%s=%s" % (k, v) for k, v in resumo.items()))


if __name__ == "__main__":
    main()
