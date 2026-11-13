"""Testes A/A: sorteia por cliente ou por loja e faz a conta de duas formas.

Nenhuma das versões muda nada: os dois grupos recebem a mesma coisa. Uma conta honesta
acusa diferença (p < 0,05) em cerca de 5% dos testes. O programa mostra quantas vezes cada
conta acusa diferença quando a conta trata as visitas como se fossem soltas.

Só usa a biblioteca padrão. Sai igual toda vez (a semente fica fixa abaixo).

Como os dados nascem (o que o programa supõe):
- Sorteio por cliente: 1.000 clientes por teste, metade em cada grupo. Cada cliente faz
  1 visita ou mais (5 em média). Depois de cada visita, a chance de voltar mais uma vez é
  CHANCE_DE_VOLTAR, logo abaixo (0.8 dá 5 visitas em média; 0.0 dá uma visita só).
  Cada cliente tem a sua chance de comprar em cada visita, 10% em média, mas uns
  compram muito mais que outros.
- Sorteio por loja: 12 lojas por teste, 6 em cada grupo, 1.500 visitas por loja. Cada loja
  tem a sua taxa de compra, entre 8% e 14%, por causa do bairro e do movimento.
- 1.000 testes de cada tipo.
"""
import math
import random

SEMENTE = 20261111
TESTES = 1000
CHANCE_DE_VOLTAR = 0.8   # 0.8: 5 visitas por cliente em média; 0.0: uma visita só
Z = 1.96          # 95%, normal
T_10 = 2.228      # 95%, t de Student com 10 graus de liberdade (6 + 6 lojas - 2)


def num(x, casas=1):
    return f'{x:.{casas}f}'.replace('.', ',')


def milhar(n):
    return f'{n:,}'.replace(',', '.')


def z_proporcoes(c_a, n_a, c_b, n_b):
    """Conta por visita: cada visita é uma linha solta."""
    pa, pb = c_a / n_a, c_b / n_b
    p = (c_a + c_b) / (n_a + n_b)
    ep = math.sqrt(p * (1 - p) * (1 / n_a + 1 / n_b))
    return (pb - pa) / ep, ep


def var_razao(linhas):
    """Variância da taxa (compras / visitas) com o cliente como linha (método delta)."""
    k = len(linhas)
    s = [c for c, _ in linhas]
    n = [v for _, v in linhas]
    ms, mn = sum(s) / k, sum(n) / k
    vs = sum((x - ms) ** 2 for x in s) / (k - 1)
    vn = sum((x - mn) ** 2 for x in n) / (k - 1)
    cov = sum((a - ms) * (b - mn) for a, b in zip(s, n)) / (k - 1)
    r = ms / mn
    return (vs - 2 * r * cov + r * r * vn) / (k * mn * mn)


def teste_por_cliente(rng):
    grupos = {'A': [], 'B': []}
    clientes = list(range(1000))
    rng.shuffle(clientes)
    for i, _ in enumerate(clientes):
        grupo = 'A' if i < 500 else 'B'
        visitas = 1
        while rng.random() < CHANCE_DE_VOLTAR:   # geométrica: 1 / (1 - chance) visitas em média
            visitas += 1
        chance = rng.betavariate(0.5, 4.5)  # 10% em média, muito desigual
        compras = sum(rng.random() < chance for _ in range(visitas))
        grupos[grupo].append((compras, visitas))
    ca, na = (sum(x) for x in zip(*grupos['A']))
    cb, nb = (sum(x) for x in zip(*grupos['B']))
    z_visita, ep_visita = z_proporcoes(ca, na, cb, nb)
    ep_cliente = math.sqrt(var_razao(grupos['A']) + var_razao(grupos['B']))
    z_cliente = (cb / nb - ca / na) / ep_cliente
    return abs(z_visita) > Z, abs(z_cliente) > Z, ep_cliente / ep_visita, na + nb


def teste_por_loja(rng):
    lojas = []
    for _ in range(12):
        taxa = rng.uniform(0.08, 0.14)
        compras = sum(rng.random() < taxa for _ in range(1500))
        lojas.append((compras, 1500))
    rng.shuffle(lojas)
    a, b = lojas[:6], lojas[6:]
    ca, na = sum(c for c, _ in a), sum(v for _, v in a)
    cb, nb = sum(c for c, _ in b), sum(v for _, v in b)
    z_visita, ep_visita = z_proporcoes(ca, na, cb, nb)
    ta = [c / v for c, v in a]
    tb = [c / v for c, v in b]
    ma, mb = sum(ta) / 6, sum(tb) / 6
    sp = (sum((x - ma) ** 2 for x in ta) + sum((x - mb) ** 2 for x in tb)) / 10
    ep_loja = math.sqrt(sp * (1 / 6 + 1 / 6))
    t = (mb - ma) / ep_loja
    return abs(z_visita) > Z, abs(t) > T_10, ep_loja / ep_visita


def main():
    rng = random.Random(SEMENTE)
    r = [teste_por_cliente(rng) for _ in range(TESTES)]
    visitas_media = sum(x[3] for x in r) / TESTES
    print(f'Sorteio por cliente: {milhar(TESTES)} testes A/A, 1.000 clientes e {num(visitas_media / 1000)} visitas por cliente em média')
    print(f'  conta por visita acusou diferença em {num(100 * sum(x[0] for x in r) / TESTES)}% dos testes')
    print(f'  conta por cliente acusou diferença em {num(100 * sum(x[1] for x in r) / TESTES)}% dos testes')
    print(f'  a margem certa é {num(sum(x[2] for x in r) / TESTES, 2)} vezes a margem da conta por visita')
    s = [teste_por_loja(rng) for _ in range(TESTES)]
    print(f'Sorteio por loja: {milhar(TESTES)} testes A/A, 12 lojas e 18.000 visitas por teste')
    print(f'  conta por visita acusou diferença em {num(100 * sum(x[0] for x in s) / TESTES)}% dos testes')
    print(f'  conta por loja acusou diferença em {num(100 * sum(x[1] for x in s) / TESTES)}% dos testes')
    print(f'  a margem certa é {num(sum(x[2] for x in s) / TESTES, 2)} vezes a margem da conta por visita')


if __name__ == '__main__':
    main()
