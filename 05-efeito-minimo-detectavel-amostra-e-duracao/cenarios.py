"""Cenários de viabilidade de um teste A/B: o menor efeito que ele vê, quanto tempo leva e quando a decisão sai.

Uso:
    python3 cenarios.py cenarios-retire.csv
    python3 cenarios.py cenarios-retire.csv --decidir-ate 2026-03-16

Cada linha do CSV é um cenário. O que vai em cada coluna está em COLUNAS, logo abaixo.
As contas são as da aula «Poder e planejamento de amostra», do curso Estatística para decisão:
linha do teste de 5 em 100, dos dois lados, e poder de 80%, com sorteio meio a meio.
Só usa a biblioteca padrão do Python.
"""
import csv
import math
import sys
from datetime import date, timedelta
from pathlib import Path
from statistics import NormalDist

AQUI = Path(__file__).resolve().parent
CALENDARIO = AQUI / 'calendario-2026.csv'
Z = NormalDist()
ALFA, PODER = 0.05, 0.80

COLUNAS = {
    'cenario': 'nome curto do cenário',
    'metrica': 'proporcao (uma taxa, como a compra em 7 dias) ou media (um valor por conta, como a receita)',
    'base': 'como a métrica está hoje: 0.32 para 32%, ou 54.60 para R$ 54,60',
    'desvio': 'desvio padrão da métrica por conta, só para media; na proporção ele sai da própria taxa',
    'minimo': 'o menor efeito que paga a mudança: 0.02 para 2 pontos, ou 1.50 para R$ 1,50',
    'contas_por_semana': 'contas novas que chegam ao gatilho por semana, os dois grupos juntos',
    'teto_contas': 'quantas contas existem no máximo para o teste; vazio se não há teto',
    'semanas': 'semanas inteiras de teste',
    'inicio': 'primeiro dia do teste, no formato ano-mês-dia',
    'dias_depois': 'dias depois do último dia do teste até o último dado da janela mais longa',
}


def _checar_alfa_poder(alfa, poder):
    if not 0 < alfa < 1 or not 0 < poder < 1:
        raise ValueError('alfa e poder ficam entre 0 e 1')


def n_proporcao(base, efeito, alfa=ALFA, poder=PODER):
    """Contas por grupo para ver uma taxa passar de base para base + efeito.

    Linha do teste com a taxa média dos dois grupos e poder com a taxa de cada grupo,
    a mesma conta do power.prop.test do R. Arredonda para cima.
    """
    return math.ceil(_n_proporcao(base, efeito, alfa, poder))


def _n_proporcao(base, efeito, alfa, poder):
    _checar_alfa_poder(alfa, poder)
    outra = base + efeito
    if not (0 < base < 1 and 0 < outra < 1):
        raise ValueError(f'taxa fora de 0 a 1: base {base}, base + efeito {outra}')
    if efeito == 0:
        raise ValueError('efeito zero: não há diferença para ver')
    za, zb = Z.inv_cdf(1 - alfa / 2), Z.inv_cdf(poder)
    media = (base + outra) / 2
    linha = za * math.sqrt(2 * media * (1 - media))
    folga = zb * math.sqrt(base * (1 - base) + outra * (1 - outra))
    return ((linha + folga) / efeito) ** 2


def mde_proporcao(n, base, alfa=ALFA, poder=PODER):
    """O menor aumento que um teste com n contas por grupo vê com o poder pedido.

    É a conta de n_proporcao ao contrário: procura o efeito em que ela dá exatamente n.
    """
    if n <= 0:
        raise ValueError('n precisa ser maior que zero')
    baixo, alto = 1e-9, 1 - base - 1e-9
    if _n_proporcao(base, alto, alfa, poder) > n:
        raise ValueError(f'com {n} contas por grupo nenhum aumento cabe abaixo de 100%')
    for _ in range(200):
        meio = (baixo + alto) / 2
        if _n_proporcao(base, meio, alfa, poder) > n:
            baixo = meio
        else:
            alto = meio
    return alto


def poder_proporcao(n, base, efeito, alfa=ALFA):
    """A chance de o teste com n contas por grupo acusar um efeito desse tamanho, se ele existir."""
    za = Z.inv_cdf(1 - alfa / 2)
    outra = base + efeito
    media = (base + outra) / 2
    linha = za * math.sqrt(2 * media * (1 - media) / n)
    erro = math.sqrt((base * (1 - base) + outra * (1 - outra)) / n)
    return Z.cdf((abs(efeito) - linha) / erro)


def n_media(efeito, desvio, alfa=ALFA, poder=PODER):
    """Contas por grupo para ver uma média subir efeito, com o desvio por conta dado."""
    _checar_alfa_poder(alfa, poder)
    if efeito == 0 or desvio <= 0:
        raise ValueError('efeito precisa ser diferente de zero e desvio maior que zero')
    za, zb = Z.inv_cdf(1 - alfa / 2), Z.inv_cdf(poder)
    return math.ceil(2 * ((za + zb) * desvio / efeito) ** 2)


def mde_media(n, desvio, alfa=ALFA, poder=PODER):
    """O menor aumento da média que um teste com n contas por grupo vê com o poder pedido."""
    _checar_alfa_poder(alfa, poder)
    if n <= 0 or desvio <= 0:
        raise ValueError('n e desvio precisam ser maiores que zero')
    za, zb = Z.inv_cdf(1 - alfa / 2), Z.inv_cdf(poder)
    return (za + zb) * desvio * math.sqrt(2 / n)


def poder_media(n, desvio, efeito, alfa=ALFA):
    za = Z.inv_cdf(1 - alfa / 2)
    return Z.cdf(abs(efeito) / (desvio * math.sqrt(2 / n)) - za)


def contas_no_teste(contas_por_semana, semanas, teto=None):
    """Contas que chegam ao gatilho em tantas semanas, os dois grupos juntos, sem passar do teto."""
    total = contas_por_semana * semanas
    return min(total, teto) if teto else total


def semanas_para(minimo, metrica, base, desvio, contas_por_semana, teto=None):
    """Semanas inteiras até o teste ver o mínimo. None se o teto de contas não deixa."""
    n = n_proporcao(base, minimo) if metrica == 'proporcao' else n_media(minimo, desvio)
    if teto and 2 * n > teto:
        return None
    return math.ceil(2 * n / contas_por_semana)


def datas(inicio, semanas, dias_depois):
    """Último dia do teste e último dia de dados."""
    ultimo = inicio + timedelta(days=7 * semanas - 1)
    return ultimo, ultimo + timedelta(days=dias_depois)


def ler_calendario(caminho=CALENDARIO):
    with open(caminho, encoding='utf-8', newline='') as f:
        return [(date.fromisoformat(l['data']), l['evento']) for l in csv.DictReader(f)]


def _numero(linha, campo, obrigatorio=True):
    texto = (linha.get(campo) or '').strip()
    if not texto:
        if obrigatorio:
            raise ValueError(f'cenário "{linha.get("cenario", "?")}": coluna {campo} vazia ({COLUNAS[campo]})')
        return None
    if ',' in texto:
        raise ValueError(f'cenário "{linha["cenario"]}": {campo} = {texto}; no CSV o decimal é com ponto ({texto.replace(",", ".")})')
    return float(texto)


def ler_cenario(linha):
    """Lê e valida uma linha do CSV. Para com erro em vez de calcular com um número sem sentido."""
    faltam = [c for c in COLUNAS if c not in linha]
    if faltam:
        raise ValueError(f'faltam colunas no CSV: {", ".join(faltam)}')
    nome = linha['cenario'].strip()
    metrica = linha['metrica'].strip()
    if metrica not in ('proporcao', 'media'):
        raise ValueError(f'cenário "{nome}": metrica = {metrica}; use proporcao ou media')
    c = {'cenario': nome, 'metrica': metrica, 'base': _numero(linha, 'base'), 'minimo': _numero(linha, 'minimo'),
         'desvio': _numero(linha, 'desvio', metrica == 'media'),
         'contas_por_semana': _numero(linha, 'contas_por_semana'), 'teto_contas': _numero(linha, 'teto_contas', False)}
    if metrica == 'proporcao' and not 0 < c['base'] < 1:
        raise ValueError(f'cenário "{nome}": base = {linha["base"]} fora de 0 a 1; 32% se escreve 0.32')
    if metrica == 'proporcao' and not 0 < c['minimo'] < 1 - c['base']:
        raise ValueError(f'cenário "{nome}": minimo = {linha["minimo"]}; 2 pontos se escreve 0.02')
    if c['minimo'] <= 0 or c['contas_por_semana'] <= 0:
        raise ValueError(f'cenário "{nome}": minimo e contas_por_semana precisam ser maiores que zero')
    semanas = linha['semanas'].strip()
    if not semanas.isdigit() or int(semanas) < 1:
        raise ValueError(f'cenário "{nome}": semanas = {semanas}; o teste roda semanas inteiras (1, 2, 3...)')
    c['semanas'] = int(semanas)
    c['inicio'] = date.fromisoformat(linha['inicio'].strip())
    dd = linha['dias_depois'].strip()
    if not dd.isdigit():
        raise ValueError(f'cenário "{nome}": dias_depois = {dd}; um número inteiro de dias')
    c['dias_depois'] = int(dd)
    return c


def avaliar(c):
    total = contas_no_teste(c['contas_por_semana'], c['semanas'], c['teto_contas'])
    n = math.floor(total / 2)
    if c['metrica'] == 'proporcao':
        mde, poder = mde_proporcao(n, c['base']), poder_proporcao(n, c['base'], c['minimo'])
    else:
        mde, poder = mde_media(n, c['desvio']), poder_media(n, c['desvio'], c['minimo'])
    ultimo, fecha = datas(c['inicio'], c['semanas'], c['dias_depois'])
    precisa = semanas_para(c['minimo'], c['metrica'], c['base'], c['desvio'], c['contas_por_semana'],
                           c['teto_contas'])
    return {**c, 'contas': total, 'por_grupo': n, 'mde': mde, 'poder': poder, 'ultimo': ultimo, 'fecha': fecha,
            'precisa': precisa, 'teto_bateu': bool(c['teto_contas']) and total >= c['teto_contas']}


def no_calendario(calendario, de, ate):
    """Os eventos do calendário entre duas datas, com dias seguidos do mesmo evento juntos."""
    grupos = []
    for d, e in calendario:
        if de <= d <= ate:
            if grupos and grupos[-1][0] == e and (d - grupos[-1][-1]).days == 1:
                grupos[-1].append(d)
            else:
                grupos.append([e, d])
    if not grupos:
        return 'nada no calendário'
    return '; '.join(f'{g[0]} {" e ".join(dm(d) for d in g[1:])}' for g in grupos)


def quebrar(texto, largura=62):
    """Quebra a lista do calendário entre um evento e outro, sem cortar o nome de um evento."""
    linhas = ['']
    for item in texto.split('; '):
        juntar = f'{linhas[-1]}; {item}' if linhas[-1] else item
        if len(juntar) <= largura or not linhas[-1]:
            linhas[-1] = juntar
        else:
            linhas[-1] += ';'
            linhas.append(item)
    return linhas


def br(x, casas=0):
    return f'{x:,.{casas}f}'.replace(',', '_').replace('.', ',').replace('_', '.')


def efeito_br(x, metrica):
    return f'{br(100 * x, 1)} pontos' if metrica == 'proporcao' else f'R$ {br(x, 2)}'


def dm(d):
    return d.strftime('%d/%m')


def main(args):
    if not args or args[0].startswith('-'):
        print(__doc__.strip())
        return 2
    prazo = None
    if '--decidir-ate' in args:
        prazo = date.fromisoformat(args[args.index('--decidir-ate') + 1])
    with open(AQUI / args[0], encoding='utf-8', newline='') as f:
        linhas = list(csv.DictReader(f))
    if not linhas:
        raise ValueError(f'{args[0]} não tem nenhum cenário: preencha uma linha por cenário abaixo do cabeçalho')
    cenarios = [avaliar(ler_cenario(l)) for l in linhas]
    calendario = ler_calendario()

    primeiro = cenarios[0]
    print(f'Mínimo que importa: {efeito_br(primeiro["minimo"], primeiro["metrica"])}. '
          f'Linha do teste 5 em 100, poder 80%, meio a meio.')
    print()
    print(f'{"cenário":<22}{"contas":>7}{"por grupo":>11}{"vê a partir de":>16}{"poder":>7}{"precisa":>10}')
    for c in cenarios:
        teto = '*' if c['teto_bateu'] else ' '
        precisa = 'não cabe' if c['precisa'] is None else f'{c["precisa"]} sem.'
        print(f'{c["cenario"]:<22}{br(c["contas"]):>6}{teto}{br(c["por_grupo"]):>11}'
              f'{efeito_br(c["mde"], c["metrica"]):>16}{br(100 * c["poder"]) + "%":>7}{precisa:>10}')
    print('poder: chance de o teste acusar o mínimo, se ele existir')
    print('precisa: semanas até ver o mínimo com o tráfego do cenário')
    if any(c['teto_bateu'] for c in cenarios):
        print('* bateu no teto de contas do teste')
    print()
    cab = f'{"cenário":<22}{"último dia":>11}{"dados até":>11}'
    print(cab + (f'{"decide até " + dm(prazo):>17}' if prazo else ''))
    for c in cenarios:
        linha = f'{c["cenario"]:<22}{dm(c["ultimo"]):>11}{dm(c["fecha"]):>11}'
        if prazo:
            linha += f'{("sim" if c["fecha"] < prazo else "não"):>17}'
        print(linha)
        for trecho in quebrar(no_calendario(calendario, c['inicio'], c['fecha'])):
            print(f'  {trecho}')
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main(sys.argv[1:]))
    except (ValueError, FileNotFoundError) as erro:
        print(f'Erro: {erro}')
        sys.exit(1)
