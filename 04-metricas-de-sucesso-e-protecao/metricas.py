"""As métricas do contrato do "Retire hoje", em código. Usado por ensaio.py e janelas.py.

Uma linha por cliente que passou pelo gatilho: é a mesma linha do sorteio (a conta).
Toda janela conta a partir do dia do primeiro gatilho, inclusive: janela de 7 dias é o dia
do gatilho e os 6 seguintes.
"""
from pathlib import Path

import pandas as pd

AQUI = Path(__file__).resolve().parent
DADOS = AQUI / 'dados'


def ler(pasta=DADOS):
    """Lê as cinco tabelas. Ids ficam como texto; datas viram data."""
    t = {
        'alocacao': pd.read_csv(pasta / 'alocacao_retire.csv', dtype=str),
        'gatilhos': pd.read_csv(pasta / 'gatilhos_antes.csv', dtype=str),
        'pedidos': pd.read_csv(pasta / 'pedidos_antes.csv', dtype={'id_pedido': str, 'id_cliente': str}),
        'atendimento': pd.read_csv(pasta / 'atendimento_antes.csv', dtype=str),
        'loja': pd.read_csv(pasta / 'loja_dias_antes.csv'),
    }
    for nome in ('gatilhos', 'pedidos', 'atendimento', 'loja'):
        if t[nome]['data'].isna().any():
            raise ValueError(f'{nome}: há linha sem data; o contrato não sabe em que janela ela cai')
        t[nome]['data'] = pd.to_datetime(t[nome]['data'], format='%Y-%m-%d')
    aloc = t['alocacao']
    if aloc['id_cliente'].duplicated().any():
        raise ValueError('alocação: a mesma conta aparece duas vezes')
    if not aloc['grupo'].isin(['A', 'B']).all():
        raise ValueError('alocação: grupo diferente de A e B')
    return t


def por_cliente(t, primeiro_de, primeiro_ate, janela=7, janela_reclamacao=14, fim_dos_dados=None):
    """Monta a tabela por cliente exposto.

    Entra a conta da alocação com o primeiro gatilho entre primeiro_de e primeiro_ate.
    Conta pedidos e receita na janela de compra e reclamação de retirada na janela dela.
    Se uma janela passa do fim dos dados, para com erro: o cliente ficaria com menos dias.
    janela=None conta até o fim dos dados, sem prazo fixo (só para comparar em janelas.py).
    """
    primeiro_de, primeiro_ate = pd.Timestamp(primeiro_de), pd.Timestamp(primeiro_ate)
    fim = pd.Timestamp(fim_dos_dados) if fim_dos_dados else t['loja']['data'].max()
    maior = max(janela or 1, janela_reclamacao)
    if primeiro_ate + pd.Timedelta(days=maior - 1) > fim:
        raise ValueError(f'a janela de {maior} dias de quem entra em {primeiro_ate:%d/%m} passa do fim dos dados '
                         f'({fim:%d/%m}); entre com o gatilho até {fim - pd.Timedelta(days=maior - 1):%d/%m}')
    g = t['gatilhos'].merge(t['alocacao'][['id_cliente', 'grupo']], on='id_cliente', how='inner')
    prim = g.groupby(['id_cliente', 'grupo'], as_index=False)['data'].min().rename(columns={'data': 'gatilho'})
    prim = prim[(prim['gatilho'] >= primeiro_de) & (prim['gatilho'] <= primeiro_ate)]

    def na_janela(eventos, dias):
        e = eventos.merge(prim[['id_cliente', 'gatilho']], on='id_cliente', how='inner')
        ultimo = fim if dias is None else e['gatilho'] + pd.Timedelta(days=dias - 1)
        dentro = (e['data'] >= e['gatilho']) & (e['data'] <= ultimo)
        return e[dentro]

    ped = na_janela(t['pedidos'], janela).groupby('id_cliente').agg(pedidos=('id_pedido', 'count'),
                                                                     receita=('valor', 'sum'))
    rec = na_janela(t['atendimento'][t['atendimento']['assunto'] == 'retirada'], janela_reclamacao)
    tab = prim.set_index('id_cliente').join(ped, how='left')
    tab['pedidos'] = tab['pedidos'].astype(float).fillna(0).astype(int)
    tab['receita'] = tab['receita'].astype(float).fillna(0.0)
    tab['comprou'] = (tab['pedidos'] > 0).astype(int)
    tab['reclamou'] = tab.index.isin(rec['id_cliente']).astype(int)
    return tab.reset_index()


def resumo(tab):
    """Uma linha por grupo: numeradores, denominadores e as métricas do contrato."""
    s = tab.groupby('grupo').agg(clientes=('id_cliente', 'count'), compraram=('comprou', 'sum'),
                                 pedidos=('pedidos', 'sum'), receita=('receita', 'sum'),
                                 reclamaram=('reclamou', 'sum'))
    s['compra_7d'] = s['compraram'] / s['clientes']
    s['receita_por_cliente'] = s['receita'] / s['clientes']
    s['ticket_por_pedido'] = s['receita'] / s['pedidos']
    s['reclamacao_14d'] = s['reclamaram'] / s['clientes']
    return s


def loja_por_dia(t):
    """Proteção da loja: a parte das retiradas que atrasou em cada dia e as vendas do balcão."""
    loja = t['loja'].copy()
    loja['atraso'] = loja['retiradas_atrasadas'] / loja['retiradas']
    return loja


def br(x, casas=1):
    """Número no jeito brasileiro: ponto no milhar, vírgula no decimal."""
    return f'{x:,.{casas}f}'.replace(',', '_').replace('.', ',').replace('_', '.')
