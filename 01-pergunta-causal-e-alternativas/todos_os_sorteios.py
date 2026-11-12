"""Os seis carrinhos da seção 3 da aula e todos os jeitos de sortear três deles para o e-mail.

Na vida real ninguém vê as duas colunas de um carrinho. Aqui as duas estão na tabela para você
ver o que o sorteio faz com a conta. Só usa a biblioteca padrão.
"""
from fractions import Fraction
from itertools import combinations

# carrinho: (compra se receber o e-mail, compra se não receber)
CARRINHOS = {"A": (1, 1), "B": (1, 0), "C": (0, 0), "D": (1, 0), "E": (0, 0), "F": (1, 1)}


def pontos(fr):
    return f"{float(fr) * 100:+.1f}".replace(".", ",")


efeito_real = Fraction(sum(com - sem for com, sem in CARRINHOS.values()), len(CARRINHOS))
print(f"Efeito médio de verdade (as duas colunas): {pontos(efeito_real)} pontos")

estimativas = []
for com_email in combinations(CARRINHOS, 3):
    sem_email = [c for c in CARRINHOS if c not in com_email]
    taxa_com = Fraction(sum(CARRINHOS[c][0] for c in com_email), 3)
    taxa_sem = Fraction(sum(CARRINHOS[c][1] for c in sem_email), 3)
    estimativas.append(("".join(com_email), taxa_com - taxa_sem))

print(f"Sorteios possíveis: {len(estimativas)}")
contagem = {}
for _, est in estimativas:
    contagem[est] = contagem.get(est, 0) + 1
for est in sorted(contagem):
    print(f"  estimativa {pontos(est):>6} pontos em {contagem[est]:>2} sorteios")
media = sum(e for _, e in estimativas) / len(estimativas)
print(f"Média das estimativas: {pontos(media)} pontos")
print("Exemplo: e-mail para B, C, F ->", pontos(dict(estimativas)["BCF"]), "pontos")
print("Exemplo: e-mail para A, B, F ->", pontos(dict(estimativas)["ABF"]), "pontos")
