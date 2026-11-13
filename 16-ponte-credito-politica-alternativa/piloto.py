"""Contas do piloto de uma regra de crédito nova, no papel.

Uso, na pasta dessa aula do kit:

    python3 piloto.py        mostra as contas do piloto da faixa D da aula

No Python aberto nessa pasta:

    from piloto import *

Só usa a biblioteca padrão (Python 3.9 ou mais novo). Nenhuma conta aqui concede crédito:
ela diz quanto um piloto pode perder, quantos contratos ele junta, quando a resposta fica
pronta e qual a chance de a resposta sair clara.

As hipóteses de cada conta estão na função. As principais:
- a exposição de um contrato é o valor emprestado inteiro (exagera um pouco, porque o saldo
  cai a cada parcela paga);
- a perda de um contrato mau é a LGD vezes a exposição; a margem já desconta funding,
  comissão, operação e cobrança, antes da perda;
- mau é alguma parcela chegar a 90 dias de atraso; a primeira parcela vence um mês depois
  do Pix;
- os contratos de um piloto são independentes, com a mesma chance de virar mau.
"""
import calendar
import datetime as dt
import math
from statistics import NormalDist

Z95 = NormalDist().inv_cdf(0.975)


def _entre_0_e_1(nome, x, inclui_zero=False):
    if not isinstance(x, (int, float)) or isinstance(x, bool) or math.isnan(x):
        raise ValueError(f'{nome} precisa ser um número')
    if not ((0 <= x <= 1) if inclui_zero else (0 < x <= 1)):
        faixa = 'entre 0 e 1' if inclui_zero else 'maior que 0 e no máximo 1'
        raise ValueError(f'{nome} precisa ser {faixa} (veio {x}); use 0.35 para 35%')


def _positivo(nome, x):
    if not isinstance(x, (int, float)) or isinstance(x, bool) or math.isnan(x) or x <= 0:
        raise ValueError(f'{nome} precisa ser um número maior que zero (veio {x})')


def parcela(valor, parcelas, taxa_mes):
    """Parcela fixa (tabela Price) de um empréstimo."""
    _positivo('valor', valor)
    _positivo('parcelas', parcelas)
    _entre_0_e_1('taxa_mes', taxa_mes, inclui_zero=True)
    if taxa_mes == 0:
        return valor / parcelas
    return valor * taxa_mes / (1 - (1 + taxa_mes) ** -parcelas)


def pd_empate(margem, lgd, valor):
    """Chance de mau em que a margem paga exatamente a perda esperada: margem = PD × LGD × valor."""
    _positivo('margem', margem)
    _entre_0_e_1('lgd', lgd)
    _positivo('valor', valor)
    empate = margem / (lgd * valor)
    if empate >= 1:
        raise ValueError('com essa margem o contrato paga a perda mesmo se todos virarem maus')
    return empate


def resultado_por_contrato(margem, pd, lgd, valor):
    """Resultado esperado de um contrato: margem menos PD × LGD × valor."""
    _entre_0_e_1('pd', pd, inclui_zero=True)
    _entre_0_e_1('lgd', lgd)
    _positivo('valor', valor)
    return margem - pd * lgd * valor


def teto_contratos(perda_maxima, pd_pessimista, lgd, valor):
    """Quantos contratos cabem se a perda no pior caso não pode passar de perda_maxima."""
    _positivo('perda_maxima', perda_maxima)
    _entre_0_e_1('pd_pessimista', pd_pessimista)
    _entre_0_e_1('lgd', lgd)
    _positivo('valor', valor)
    n = math.floor(perda_maxima / (pd_pessimista * lgd * valor) + 1e-9)
    if n < 1:
        raise ValueError('a perda máxima não cobre nem um contrato no pior caso')
    return n


def contratos_esperados(elegiveis_mes, parte, aceite, meses):
    """Contratos que o piloto junta: elegíveis por mês × parte sorteada × aceite × meses."""
    _positivo('elegiveis_mes', elegiveis_mes)
    _entre_0_e_1('parte', parte)
    _entre_0_e_1('aceite', aceite)
    _positivo('meses', meses)
    return elegiveis_mes * parte * aceite * meses


def chance_de_bater_o_teto(media, teto):
    """Chance de o piloto juntar teto contratos ou mais antes do fim da contratação.

    Supõe que as propostas chegam soltas, uma sem relação com a outra (Poisson com essa média).
    """
    _positivo('media', media)
    if not isinstance(teto, int) or teto < 1:
        raise ValueError('teto precisa ser um inteiro maior que zero')
    abaixo = sum(math.exp(k * math.log(media) - media - math.lgamma(k + 1)) for k in range(teto))
    return max(0.0, 1 - abaixo)


def wilson(k, n, z=Z95):
    """Intervalo de Wilson para k maus em n contratos (aula «Intervalo para proporção»)."""
    if not isinstance(n, int) or n < 1:
        raise ValueError('n precisa ser um inteiro maior que zero')
    if not isinstance(k, int) or not 0 <= k <= n:
        raise ValueError('k precisa ser um inteiro entre 0 e n')
    p = k / n
    centro = (p + z * z / (2 * n)) / (1 + z * z / n)
    meia = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return centro - meia, centro + meia


def leitura(k, n, empate):
    """A regra de decisão escrita antes: o intervalo inteiro abaixo do empate, acima ou cruzando."""
    baixo, alto = wilson(k, n)
    if alto < empate:
        return 'vira política'
    if baixo > empate:
        return 'para'
    return 'reformula'


def cortes(n, empate):
    """Maior número de maus que ainda dá «vira política» e menor que já dá «para», em n contratos."""
    vira = [k for k in range(n + 1) if leitura(k, n, empate) == 'vira política']
    para = [k for k in range(n + 1) if leitura(k, n, empate) == 'para']
    return (max(vira) if vira else None), (min(para) if para else None)


def chance_de_decidir(n, pd_real, empate):
    """Chance de cada leitura se a PD real for pd_real, somando a binomial de 0 a n maus."""
    _entre_0_e_1('pd_real', pd_real, inclui_zero=True)
    _entre_0_e_1('empate', empate)
    chances = {'vira política': 0.0, 'reformula': 0.0, 'para': 0.0}
    for k in range(n + 1):
        chances[leitura(k, n, empate)] += math.comb(n, k) * pd_real ** k * (1 - pd_real) ** (n - k)
    return chances


def chance_de_alarme(n, taxa_real, limite):
    """Chance de a taxa lida em n contratos passar do limite, se a taxa real for taxa_real."""
    if not isinstance(n, int) or n < 1:
        raise ValueError('n precisa ser um inteiro maior que zero')
    _entre_0_e_1('taxa_real', taxa_real, inclui_zero=True)
    _entre_0_e_1('limite', limite)
    return sum(math.comb(n, k) * taxa_real ** k * (1 - taxa_real) ** (n - k)
               for k in range(n + 1) if k / n > limite)


def somar_meses(data, meses):
    """Mesma data, meses depois; se o dia não existe no mês, fica o último dia do mês."""
    ano, mes = divmod(data.month - 1 + meses, 12)
    ano, mes = data.year + ano, mes + 1
    return dt.date(ano, mes, min(data.day, calendar.monthrange(ano, mes)[1]))


def janela_do_mau(parcelas):
    """Meses depois do Pix até a última parcela poder chegar a 90 dias de atraso."""
    _positivo('parcelas', parcelas)
    return parcelas + 3


def primeiro_mau_possivel(pix):
    """O primeiro dia em que um contrato pode virar mau: 1ª parcela (1 mês depois) + 90 dias."""
    return somar_meses(pix, 1) + dt.timedelta(days=90)


def safra_madura(ultimo_pix, parcelas, dias_registro=7):
    """Dia em que a safra fecha: janela do mau depois do último Pix, mais os dias de registro."""
    return somar_meses(ultimo_pix, janela_do_mau(parcelas)) + dt.timedelta(days=dias_registro)


def comite_seguinte(data):
    """Primeira segunda-feira de mês que cai no dia ou depois da data (o comitê da Marta)."""
    d = dt.date(data.year, data.month, 1)
    while True:
        segunda = d + dt.timedelta(days=(0 - d.weekday()) % 7)
        if segunda >= data:
            return segunda
        d = somar_meses(d, 1)


def fim_do_mes(ano, mes):
    return dt.date(ano, mes, calendar.monthrange(ano, mes)[1])


def br(x, casas=1):
    """Número no jeito brasileiro: 1.234,5."""
    s = f'{x:,.{casas}f}'
    return s.replace(',', '_').replace('.', ',').replace('_', '.')


def dia(d):
    return d.strftime('%d/%m/%Y')


if __name__ == '__main__':
    # O piloto da faixa D da aula: hipóteses do briefing.md
    VALOR, PARCELAS, TAXA = 1000, 6, 0.065
    MARGEM, LGD = 140, 0.70
    PERDA_MAXIMA, PD_PESSIMISTA = 40000, 0.35
    ELEGIVEIS, PARTE, ACEITE, MESES = 58, 0.6, 0.70, 6
    INICIO, ULTIMO_PIX = dt.date(2030, 3, 1), fim_do_mes(2030, 8)

    emp = pd_empate(MARGEM, LGD, VALOR)
    teto = teto_contratos(PERDA_MAXIMA, PD_PESSIMISTA, LGD, VALOR)
    esperado = contratos_esperados(ELEGIVEIS, PARTE, ACEITE, MESES)
    n = math.floor(esperado)
    print(f'parcela: R$ {br(parcela(VALOR, PARCELAS, TAXA), 2)}')
    print(f'PD de empate: {br(100 * emp)}%')
    print(f'teto: {teto} contratos, R$ {br(teto * VALOR, 0)} emprestados')
    print(f'contratos esperados: {br(esperado)} ({MESES} meses, {br(100 * PARTE, 0)}% dos elegíveis sorteados)')
    vira, para = cortes(n, emp)
    print(f'com {n} contratos: vira política com até {vira} maus; para com {para} maus ou mais')
    for pd_real in (0.10, 0.12, 0.15, 0.18, 0.20, 0.25, 0.30):
        c = chance_de_decidir(n, pd_real, emp)
        print(f'PD real {br(100 * pd_real, 0)}%: resultado R$ {br(resultado_por_contrato(MARGEM, pd_real, LGD, VALOR), 0)}'
              f' por contrato | vira política {br(100 * c["vira política"], 0)}%'
              f' | reformula {br(100 * c["reformula"], 0)}% | para {br(100 * c["para"], 0)}%')
    print(f'primeiro mau possível de quem pegou no dia {dia(INICIO)}: {dia(primeiro_mau_possivel(INICIO))}')
    print(f'safra de agosto madura em {dia(safra_madura(ULTIMO_PIX, PARCELAS))}; '
          f'comitê de {dia(comite_seguinte(safra_madura(ULTIMO_PIX, PARCELAS)))}')
