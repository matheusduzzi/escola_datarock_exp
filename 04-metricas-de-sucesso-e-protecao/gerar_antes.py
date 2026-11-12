"""Gera os registros das 4 semanas antes do teste "Retire hoje" (05/01 a 01/02/2026).

Como os dados nascem (abra depois de fazer as contas da aula):

- As 9.000 contas são as da tabela de alocação da aula «Randomizar e conferir grupos»
  (dados/alocacao_retire.csv). O grupo não entra em nenhuma conta deste gerador: antes do
  início ninguém viu o "Retire hoje", e A e B só diferem pelo acaso.
- Perto de 30% das contas chegam à escolha da entrega com um produto em estoque na loja
  (o gatilho) em algum dia das 4 semanas. Algumas voltam ao gatilho mais 1 ou 2 vezes.
- Quem passa pelo gatilho compra nos 7 dias seguintes com chance perto de 32%, quase sempre
  no dia ou no dia seguinte; 15% de quem compra faz um segundo pedido na mesma semana. Depois dos 7 dias, cada dia ainda tem 1% de chance de uma compra.
  Por isso a compra "até o fim dos dados" cresce com o tempo que sobra.
- Há pedidos fora do gatilho: de quem nunca chegou nele e de quem comprou antes dele.
- Reclamação de retirada no atendimento: perto de 8% dos pedidos com retirada, de 1 a 9 dias
  depois do pedido. Há também contatos de outros assuntos.
- A loja tem a sua própria tabela por dia, com todas as retiradas (não só as das 9.000 contas):
  perto de 40 retiradas por dia, 3% delas atrasadas, e as vendas do balcão.

Supõe, e uma loja de verdade não garante: clientes independentes, comportamento igual nas
4 semanas e nenhum feriado. Só usa a biblioteca padrão e Random.random(), cuja sequência o
Python garante entre versões; a saída é igual toda vez.
"""
import csv
import random
from datetime import date, timedelta
from pathlib import Path

AQUI = Path(__file__).resolve().parent
DADOS = AQUI / 'dados'
INICIO = date(2026, 1, 5)
DIAS = 28


def dia(i):
    return (INICIO + timedelta(days=i)).isoformat()


def escolher(r, pesos):
    """Índice sorteado com os pesos dados, usando só r.random()."""
    u, acc = r.random() * sum(pesos), 0.0
    for i, p in enumerate(pesos):
        acc += p
        if u < acc:
            return i
    return len(pesos) - 1


def valor(r):
    return round(60 + 420 * r.random() ** 2, 2)


def main():
    r = random.Random(20260105)
    with open(DADOS / 'alocacao_retire.csv', encoding='utf-8', newline='') as f:
        contas = [linha['id_cliente'] for linha in csv.DictReader(f)]
    gatilhos, pedidos, atendimento = [], [], []

    def pedido(cliente, d, entrega):
        pedidos.append((f'P{len(pedidos) + 1:05d}', cliente, dia(d), f'{valor(r):.2f}', entrega))
        if entrega == 'retirada' and r.random() < 0.08:
            dd = d + 1 + escolher(r, [1] * 9)
            if dd < DIAS:
                atendimento.append((cliente, dia(dd), 'retirada'))

    for c in contas:
        if r.random() < 0.30:
            d0 = escolher(r, [1] * DIAS)
            extras = escolher(r, [6, 3, 1])
            dias_g = {d0} | {d0 + 1 + escolher(r, [1] * 10) for _ in range(extras)}
            for d in sorted(x for x in dias_g if x < DIAS):
                gatilhos.append((c, dia(d)))
            if d0 > 0 and r.random() < 0.08:
                pedido(c, escolher(r, [1] * d0), 'casa')
            if r.random() < 0.32:
                atraso = escolher(r, [50, 22, 9, 7, 5, 4, 3])
                if d0 + atraso < DIAS:
                    pedido(c, d0 + atraso, 'retirada' if r.random() < 0.25 else 'casa')
                    if r.random() < 0.15:
                        d2 = d0 + atraso + 1 + escolher(r, [1] * 5)
                        if d2 < min(d0 + 7, DIAS):
                            pedido(c, d2, 'retirada' if r.random() < 0.25 else 'casa')
            for d in range(d0 + 7, DIAS):
                if r.random() < 0.01:
                    pedido(c, d, 'retirada' if r.random() < 0.25 else 'casa')
        elif r.random() < 0.15:
            pedido(c, escolher(r, [1] * DIAS), 'casa')
        if r.random() < 0.05:
            atendimento.append((c, dia(escolher(r, [1] * DIAS)), 'entrega' if r.random() < 0.6 else 'troca'))

    pedidos.sort(key=lambda p: (p[2], p[0]))
    atendimento.sort(key=lambda a: (a[1], a[0]))
    loja = []
    for i in range(DIAS):
        sabado = (INICIO + timedelta(days=i)).weekday() == 5
        retiradas = 32 + escolher(r, [1] * 17)
        atrasadas = sum(r.random() < 0.03 for _ in range(retiradas))
        balcao = (4200 + 1600 * (r.random() - 0.5) * 2) * (1.4 if sabado else 1.0)
        loja.append((dia(i), retiradas, atrasadas, f'{balcao:.2f}'))

    tabelas = {
        'gatilhos_antes.csv': (('id_cliente', 'data'), gatilhos),
        'pedidos_antes.csv': (('id_pedido', 'id_cliente', 'data', 'valor', 'entrega'), pedidos),
        'atendimento_antes.csv': (('id_cliente', 'data', 'assunto'), atendimento),
        'loja_dias_antes.csv': (('data', 'retiradas', 'retiradas_atrasadas', 'vendas_balcao'), loja),
    }
    for nome, (cab, linhas) in tabelas.items():
        with open(DADOS / nome, 'w', encoding='utf-8', newline='') as f:
            w = csv.writer(f, lineterminator='\n')
            w.writerow(cab)
            w.writerows(linhas)
    print(' '.join(f'{n.replace("_antes.csv", "")}={len(t[1])}' for n, t in tabelas.items()))


if __name__ == '__main__':
    main()
