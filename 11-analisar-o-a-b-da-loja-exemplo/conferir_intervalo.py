"""Confere o intervalo do relatório por outro caminho: o bootstrap.

    python3 conferir_intervalo.py plano-botao.md

Reamostra as visitas de cada grupo 5.000 vezes, com reposição, e pega os percentis 2,5 e 97,5 da
diferença B menos A. O relatório decide pela aproximação normal, que é o método do plano; este
programa só mostra se os dois caminhos contam a mesma história. Sorteios com
numpy.random.default_rng(42): rodar de novo dá os mesmos números.
"""
import sys

import numpy as np

from analise_ab import ErroPlano, ParadaExecucao, efeito, ler_plano, ler_visitas

REPETICOES = 5000


def bootstrap(a, b, repeticoes=REPETICOES, semente=42):
    rng = np.random.default_rng(semente)
    difs = [rng.choice(b, len(b)).mean() - rng.choice(a, len(a)).mean() for _ in range(repeticoes)]
    return np.percentile(difs, [2.5, 97.5])


def br(x):
    return f'{100 * x:.2f}'.replace('.', ',')


def main(argv):
    if len(argv) != 1:
        print('uso: python3 conferir_intervalo.py <plano>')
        return 2
    try:
        plano = ler_plano(argv[0])
        visitas = ler_visitas(plano['dados'], plano['metrica'])
    except (ErroPlano, ParadaExecucao, FileNotFoundError) as e:
        print(f'Erro: {e}')
        return 1
    v = visitas.dropna(subset=['grupo'])
    a = v.loc[v['grupo'] == 'A', plano['metrica']].to_numpy()
    b = v.loc[v['grupo'] == 'B', plano['metrica']].to_numpy()
    e = efeito(visitas, plano)
    inf, sup = bootstrap(a, b)
    print(f'{plano["dados"].name}: diferença B menos A de {br(e["diferenca"])} ponto')
    print(f'  aproximação normal (o plano): {br(e["inferior"])} a {br(e["superior"])} ponto')
    print(f'  bootstrap, {REPETICOES} reamostragens: {br(inf)} a {br(sup)} ponto')
    print(f'  maior distância entre os limites: {br(max(abs(inf - e["inferior"]), abs(sup - e["superior"])))} ponto')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
