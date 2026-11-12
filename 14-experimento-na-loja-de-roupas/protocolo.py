"""Contas do protocolo do teste do look pronto na rede Trama.

Uso, no Python aberto na pasta dessa aula do kit:
    from protocolo import *

Rodar `python3 protocolo.py` mostra as contas principais do protocolo da aula.
Só usa a biblioteca padrão. Os dados ficam em dados/ (lojas.csv e semanas.csv).

Todas as partes e taxas são frações: 0.04 quer dizer 4%.
"""
import csv
import functools
import datetime as dt
import hashlib
import itertools
import math
import random
import statistics
from pathlib import Path

AQUI = Path(__file__).resolve().parent

# As janelas do protocolo (sempre a segunda-feira que abre a semana)
ANTES = ('2026-05-04', 12)      # as 12 últimas semanas com a devolução fechada
TESTE = ('2026-09-14', 8)       # o teste: de 14/09 a 08/11/2026
# O ensaio no histórico repete a mesma distância: 12 semanas, 7 de intervalo, 8 de "teste"
ENSAIO_ANTES = ('2026-01-19', 12)
ENSAIO_TESTE = ('2026-06-01', 8)


# ---------- leitura ----------

def ler_lojas(caminho=AQUI / 'dados' / 'lojas.csv'):
    with open(caminho, encoding='utf-8') as f:
        return list(csv.DictReader(f))


def ler_semanas(caminho=AQUI / 'dados' / 'semanas.csv'):
    with open(caminho, encoding='utf-8') as f:
        linhas = list(csv.DictReader(f))
    for x in linhas:
        for c in ('entradas', 'falta_tamanho'):
            x[c] = int(x[c])
        for c in ('vendas', 'devolvido_7d', 'devolvido_30d'):
            x[c] = float(x[c])
    return linhas


def _fracao(valor, nome):
    if not 0 <= valor < 1:
        raise ValueError(f'{nome} é uma fração entre 0 e 1: escreva 0.04 para 4%, e não 4.')
    return valor


def semanas_da_janela(janela):
    """As segundas-feiras de uma janela (início, número de semanas)."""
    inicio, n = janela
    if n < 1:
        raise ValueError('a janela precisa de pelo menos 1 semana')
    d = dt.date.fromisoformat(inicio)
    if d.weekday() != 0:
        raise ValueError(f'{inicio} não é segunda-feira: a semana da rede começa na segunda')
    return [(d + dt.timedelta(weeks=i)).isoformat() for i in range(n)]


def fim_da_janela(janela):
    """O domingo que fecha a última semana da janela."""
    return dt.date.fromisoformat(semanas_da_janela(janela)[-1]) + dt.timedelta(days=6)


# ---------- unidades, pares e sorteio ----------

def unidade_de(lojas, por='loja'):
    """Dicionário loja -> unidade do sorteio ('loja' ou 'cidade')."""
    if por not in ('loja', 'cidade'):
        raise ValueError("a unidade é 'loja' ou 'cidade'")
    return {x['loja']: x[por] for x in lojas}


def venda_liquida(semanas, mapa, janela):
    """Venda líquida média por semana de cada unidade: vendas menos o que voltou em 30 dias."""
    dias = set(semanas_da_janela(janela))
    soma = {}
    for x in semanas:
        if x['semana'] in dias and x['loja'] in mapa:
            u = mapa[x['loja']]
            soma[u] = soma.get(u, 0.0) + x['vendas'] - x['devolvido_30d']
    achadas = {x['semana'] for x in semanas if x['semana'] in dias}
    if achadas != dias:
        raise ValueError(f'faltam semanas nos dados: {sorted(dias - achadas)}')
    return {u: v / len(dias) for u, v in soma.items()}


def formar_pares(medias):
    """Ordena as unidades da maior para a menor e junta de duas em duas.
    Se o número for ímpar, a menor fica de fora e volta como sobra."""
    ordem = sorted(medias, key=lambda u: (-medias[u], u))
    pares = [tuple(ordem[i:i + 2]) for i in range(0, len(ordem) - 1, 2)]
    sobra = ordem[-1] if len(ordem) % 2 else None
    return pares, sobra


def sortear(pares, nome_teste):
    """Em cada par, o hash do nome do teste com o par decide quem fica com o look pronto (B)."""
    grupos = {}
    for a, b in pares:
        bit = hashlib.sha256(f'{nome_teste}:{a}-{b}'.encode('utf-8')).digest()[0] % 2
        grupos[a], grupos[b] = ('B', 'A') if bit else ('A', 'B')
    return grupos


# ---------- a conta da leitura ----------

def crescimento(semanas, mapa, antes, teste, efeito=0.0, grupos=None):
    """Quanto a venda líquida de cada unidade mudou do 'antes' para o 'teste'.
    `efeito` soma um efeito de mentira às unidades do B, para ensaiar o teste no histórico."""
    a = venda_liquida(semanas, mapa, antes)
    t = venda_liquida(semanas, mapa, teste)
    fator = {u: (1 + efeito) if grupos and grupos.get(u) == 'B' else 1.0 for u in a}
    return {u: t[u] * fator[u] / a[u] - 1 for u in a}


def nivel(semanas, mapa, teste, efeito=0.0, grupos=None):
    """Venda líquida de cada unidade no 'teste', relativa à média de todas: sem olhar o antes."""
    t = venda_liquida(semanas, mapa, teste)
    fator = {u: (1 + efeito) if grupos and grupos.get(u) == 'B' else 1.0 for u in t}
    t = {u: t[u] * fator[u] for u in t}
    m = statistics.mean(t.values())
    return {u: v / m - 1 for u, v in t.items()}


@functools.lru_cache(maxsize=None)
def t_critico(gl, confianca=0.95):
    """A régua do intervalo com poucas unidades (distribuição t de Student), sem SciPy."""
    if gl < 1:
        raise ValueError('com menos de 2 pares não existe intervalo')
    c = math.lgamma((gl + 1) / 2) - math.lgamma(gl / 2) - 0.5 * math.log(gl * math.pi)

    def acumulada(x, passos=4000):  # de 0 a x, regra de Simpson
        h = x / passos
        f = [math.exp(c - (gl + 1) / 2 * math.log(1 + (h * i) ** 2 / gl)) for i in range(passos + 1)]
        return h / 3 * (f[0] + f[-1] + 4 * sum(f[1:-1:2]) + 2 * sum(f[2:-1:2]))

    alvo, lo, hi = confianca / 2, 0.0, 50.0
    for _ in range(60):
        meio = (lo + hi) / 2
        lo, hi = (meio, hi) if acumulada(meio) < alvo else (lo, meio)
    return (lo + hi) / 2


def efeito_pareado(valores, pares, grupos, confianca=0.95):
    """Média das diferenças B menos A dentro dos pares, com o intervalo pela régua t."""
    d = [valores[b] - valores[a] if grupos[b] == 'B' else valores[a] - valores[b] for a, b in pares]
    k = len(d)
    media = statistics.mean(d)
    ep = statistics.stdev(d) / math.sqrt(k)
    t = t_critico(k - 1, confianca)
    return {'efeito': media, 'ep': ep, 'ic': (media - t * ep, media + t * ep)}


def efeito_sem_pares(valores, grupos, confianca=0.95):
    """Diferença das médias B menos A, sem pares, com o intervalo pela régua t."""
    b = [v for u, v in valores.items() if grupos[u] == 'B']
    a = [v for u, v in valores.items() if grupos[u] == 'A']
    media = statistics.mean(b) - statistics.mean(a)
    ep = math.sqrt(statistics.variance(b) / len(b) + statistics.variance(a) / len(a))
    t = t_critico(len(a) + len(b) - 2, confianca)
    return {'efeito': media, 'ep': ep, 'ic': (media - t * ep, media + t * ep)}


# ---------- o ensaio no histórico ----------

def _sorteios_pareados(pares):
    for bits in itertools.product((0, 1), repeat=len(pares)):
        g = {}
        for (a, b), bit in zip(pares, bits):
            g[a], g[b] = ('B', 'A') if bit else ('A', 'B')
        yield g


def _sorteios_livres(unidades, quantos=4096, numero=14):
    rng = random.Random(numero)
    unidades = sorted(unidades)
    for _ in range(quantos):
        b = set(rng.sample(unidades, len(unidades) // 2))
        yield {u: 'B' if u in b else 'A' for u in unidades}


def ensaio(semanas, lojas, por='loja', pareado=True, com_antes=True, efeito=0.0,
           antes=ENSAIO_ANTES, teste=ENSAIO_TESTE, tirar=(), minimo=None):
    """Roda o teste no histórico, onde ninguém teve o look pronto, em todos os sorteios possíveis
    dos pares (ou em 4.096 sorteios sem pares). Com `efeito`, as unidades do B ganham esse efeito
    de mentira. `tirar` remove lojas, como uma loja que fecha no meio do teste.

    Retorna o desvio das estimativas, a parte dos sorteios em que o intervalo fica todo acima de
    zero (o poder, se houver efeito) e a parte em que o intervalo não passa pelo zero. Com
    `minimo`, retorna também a parte em que a regra lança: intervalo acima de zero e estimativa
    pelo menos igual ao mínimo."""
    if minimo is not None:
        _fracao(minimo, 'o mínimo')
    mapa = unidade_de(lojas, por)
    pares, sobra = formar_pares(venda_liquida(semanas, mapa, antes))
    # Os pares são os do plano. Se uma loja sai, o par dela sai inteiro: o outro lado não troca de par.
    fora = {mapa[k] for k in tirar} | ({sobra} if sobra else set())
    pares = [p for p in pares if not set(p) & fora]
    ficam = {u for p in pares for u in p}
    mapa = {k: v for k, v in mapa.items() if v in ficam and k not in tirar}
    if len(pares) < 2:
        raise ValueError('sobrou menos de 2 pares: não existe intervalo')
    sorteios = list(_sorteios_pareados(pares) if pareado else _sorteios_livres({u for p in pares for u in p}))
    base = crescimento(semanas, mapa, antes, teste) if com_antes else venda_liquida(semanas, mapa, teste)
    estimativas, acima, fora, lanca = [], 0, 0, 0
    for g in sorteios:
        if com_antes:
            v = {u: (1 + x) * (1 + efeito) - 1 if g[u] == 'B' else x for u, x in base.items()}
        else:
            bruto = {u: x * (1 + efeito) if g[u] == 'B' else x for u, x in base.items()}
            m = statistics.mean(bruto.values())
            v = {u: x / m - 1 for u, x in bruto.items()}
        r = efeito_pareado(v, pares, g) if pareado else efeito_sem_pares(v, g)
        estimativas.append(r['efeito'])
        acima += r['ic'][0] > 0
        fora += r['ic'][0] > 0 or r['ic'][1] < 0
        lanca += minimo is not None and r['ic'][0] > 0 and r['efeito'] >= minimo
    n = len(sorteios)
    saida = {'unidades': 2 * len(pares), 'sorteios': n, 'desvio': statistics.pstdev(estimativas),
             'acima_de_zero': acima / n, 'fora_do_zero': fora / n}
    if minimo is not None:
        saida['lanca'] = lanca / n
    return saida


def efeito_minimo_detectavel(semanas, lojas, poder=0.80, **opcoes):
    """O menor efeito que o desenho enxerga com o poder pedido: o intervalo todo acima de zero
    em pelo menos 80% dos sorteios. Procura por bisseção até 0,05 ponto percentual e arredonda
    para cima em 0,1 ponto. Cada passo roda todos os sorteios: leva alguns segundos."""
    _fracao(poder, 'o poder')

    def chance(e):
        return ensaio(semanas, lojas, efeito=e, **opcoes)['acima_de_zero']

    lo, hi = 0.0, 0.02
    while chance(hi) < poder:
        lo, hi = hi, hi * 2
        if hi > 2:
            raise ValueError('nem um efeito de 200% fica acima de zero: o desenho não enxerga nada')
    while hi - lo > 0.0005:
        meio = (lo + hi) / 2
        lo, hi = (meio, hi) if chance(meio) < poder else (lo, meio)
    return math.ceil(hi * 1000) / 1000


# ---------- métricas de proteção ----------

def taxa_semanal(semanas, lojas_do_grupo, janela, metrica):
    """Uma taxa do grupo em cada semana. metrica: 'devolucao_7d' (% das vendas que voltou em
    7 dias) ou 'falta_tamanho' (faltas por 1.000 entradas)."""
    dias = semanas_da_janela(janela)
    num = {d: 0.0 for d in dias}
    den = {d: 0.0 for d in dias}
    for x in semanas:
        if x['semana'] in num and x['loja'] in lojas_do_grupo:
            if metrica == 'devolucao_7d':
                num[x['semana']] += x['devolvido_7d']
                den[x['semana']] += x['vendas']
            elif metrica == 'falta_tamanho':
                num[x['semana']] += x['falta_tamanho']
                den[x['semana']] += x['entradas'] / 1000
            else:
                raise ValueError("metrica é 'devolucao_7d' ou 'falta_tamanho'")
    return [num[d] / den[d] for d in dias]


def chance_de_alarme(semanas, lojas, limite, metrica, seguidas=2, por='loja',
                     janela=ENSAIO_TESTE, antes=ENSAIO_ANTES):
    """No histórico, sem mudança nenhuma: em que parte dos sorteios dos pares a taxa do B passa a
    do A por mais que `limite` em `seguidas` semanas seguidas. É a chance de alarme falso da regra.
    O limite é uma fração da taxa: 0.01 é 1 ponto de devolução; para a falta de tamanho, é o número
    de faltas por 1.000 entradas."""
    if limite < 0 or seguidas < 1:
        raise ValueError('o limite não pode ser negativo e a regra pede pelo menos 1 semana')
    if metrica == 'devolucao_7d':
        _fracao(limite, 'o limite de devolução')
    mapa = unidade_de(lojas, por)
    pares, sobra = formar_pares(venda_liquida(semanas, mapa, antes))
    alarmes, n = 0, 0
    for g in _sorteios_pareados(pares):
        b = {k for k, u in mapa.items() if g.get(u) == 'B'}
        a = {k for k, u in mapa.items() if g.get(u) == 'A'}
        dif = [tb - ta for tb, ta in zip(taxa_semanal(semanas, b, janela, metrica),
                                         taxa_semanal(semanas, a, janela, metrica))]
        seq, disparou = 0, False
        for x in dif:
            seq = seq + 1 if x > limite else 0
            disparou = disparou or seq >= seguidas
        alarmes += disparou
        n += 1
    return alarmes / n


# ---------- o mínimo que paga ----------

def minimo_que_paga(custo_semana, margem, venda_semana):
    """Quanto a venda líquida de uma loja precisa subir, em fração, para a margem pagar o custo."""
    _fracao(margem, 'a margem')
    if margem == 0 or venda_semana <= 0 or custo_semana < 0:
        raise ValueError('margem e venda precisam ser positivas, e o custo não pode ser negativo')
    return custo_semana / margem / venda_semana


# ---------- calendário ----------

def data_da_leitura(janela=TESTE, devolucao=30, registro=7):
    """O dia em que a última venda do teste já teve todo o prazo de devolução e o registro."""
    return fim_da_janela(janela) + dt.timedelta(days=devolucao + registro)


def ultima_semana_fechada(hoje, devolucao=30, registro=7):
    """A segunda-feira da última semana cuja devolução já fechou em `hoje`."""
    d = dt.date.fromisoformat(hoje) - dt.timedelta(days=devolucao + registro)
    domingo = d - dt.timedelta(days=(d.weekday() + 1) % 7)
    return (domingo - dt.timedelta(days=6)).isoformat()


if __name__ == '__main__':
    semanas, lojas = ler_semanas(), ler_lojas()
    mapa = unidade_de(lojas)
    pares, _ = formar_pares(venda_liquida(semanas, mapa, ANTES))
    grupos = sortear(pares, 'look-pronto-2026')
    print('pares:', len(pares), 'lojas no B:', sorted(u for u, g in grupos.items() if g == 'B'))
    print('mínimo que o desenho enxerga, 8 semanas:', efeito_minimo_detectavel(semanas, lojas))
    print('leitura:', data_da_leitura())
