# Primeira olhada nos dois testes do checkout da Loja Exemplo.
# Rode de dentro da pasta 00-apresentacao:  python3 primeira_olhada.py
#
# Para cada teste, na ordem em que eu olho:
#   1. a divisão dos grupos, antes de qualquer conta de efeito;
#   2. a conversão de cada grupo, com o seu próprio denominador;
#   3. a diferença B menos A e o intervalo de 95% (aproximação normal);
#   4. o intervalo contra o mínimo combinado antes do teste (1 ponto).
#
# As contas aqui usam só o Python, sem bibliotecas extras.
import csv
import math
from statistics import NormalDist

MINIMO_PP = 1.0  # o time combinou antes: a mudança só paga com pelo menos 1 ponto a mais
Z = NormalDist().inv_cdf(0.975)


def br(x, casas):
    """Número com vírgula decimal, como no texto da aula."""
    return f"{x:.{casas}f}".replace(".", ",")


def olhar(arquivo, nome):
    with open(arquivo, newline="", encoding="utf-8") as f:
        linhas = list(csv.reader(f))[1:]  # a primeira linha é o cabeçalho
    total = len(linhas)
    n_a = sum(1 for linha in linhas if linha[1] == "A")
    n_b = sum(1 for linha in linhas if linha[1] == "B")
    c_a = sum(1 for linha in linhas if linha[1] == "A" and linha[2] == "1")
    c_b = sum(1 for linha in linhas if linha[1] == "B" and linha[2] == "1")
    sem_grupo = total - n_a - n_b

    # Divisão 50/50: qui-quadrado com 1 grau de liberdade; p = erfc(raiz(x/2)).
    esperado = (n_a + n_b) / 2
    qui2 = ((n_a - esperado) ** 2 + (n_b - esperado) ** 2) / esperado
    p_divisao = math.erfc(math.sqrt(qui2 / 2))

    taxa_a, taxa_b = c_a / n_a, c_b / n_b
    dif = taxa_b - taxa_a
    erro = math.sqrt(taxa_a * (1 - taxa_a) / n_a + taxa_b * (1 - taxa_b) / n_b)
    baixo, alto = (dif - Z * erro) * 100, (dif + Z * erro) * 100

    if baixo >= MINIMO_PP:
        leitura = "até o pior caso passa do mínimo, seguir com o B"
    elif alto < MINIMO_PP:
        leitura = "nem o melhor caso chega ao mínimo, não seguir"
    else:
        leitura = "o intervalo cruza o mínimo, os dados ainda não decidem"

    print(f"Teste do {nome} ({arquivo.split('/')[-1]})")
    print(f"1. Divisão: {total} visitas, {n_a} no A, {n_b} no B, {sem_grupo} sem grupo")
    print(f"   A ficou com {br(n_a / (n_a + n_b) * 100, 1)}% das visitas com grupo; teste da divisão 50/50: p = {br(p_divisao, 3)}")
    print(f"2. Conversão: A {br(taxa_a * 100, 2)}% ({c_a} de {n_a}), B {br(taxa_b * 100, 2)}% ({c_b} de {n_b})")
    print(f"3. Diferença B menos A: {br(dif * 100, 2)} ponto; intervalo de 95%: {br(baixo, 2)} a {br(alto, 2)}")
    print(f"4. Contra o mínimo de {br(MINIMO_PP, 0)} ponto: {leitura}")


olhar("../dados/loja/ab_botao.csv", "botão")
print()
olhar("../dados/loja/ab_frete.csv", "frete")
