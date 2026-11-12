# Plano do teste do lembrete de carrinho

Escrito pela Lia na quinta, 02/04/2026, antes do início. Mandado ao grupo do time no mesmo dia.

## O que muda

Quem deixa produto no carrinho e sai do site sem comprar recebe, ou não, um e-mail de lembrete.

| Versão | Lembrete |
|---|---|
| A | Nenhum lembrete, como hoje |
| B | Lembrete 1 hora depois |
| C | Lembrete 24 horas depois |
| D | Lembrete 24 horas depois, com cupom de 10% |

## Quem entra e como sorteia

Toda conta que deixa o carrinho entre a segunda, 06/04, e o domingo, 03/05. Cada conta é sorteada uma vez para A, B, C ou D, com a mesma chance, e fica na mesma versão o teste todo.

## As métricas

Todas contadas por conta: contas que fizeram a coisa sobre contas sorteadas para a versão.

| Métrica | O que conta | Papel |
|---|---|---|
| `comprou_7d` | Comprou em até 7 dias depois de deixar o carrinho | Decide |
| `saiu_da_lista_30d` | Pediu para sair da lista de e-mails da loja em até 30 dias | Proteção |
| `cancelou_7d` | Cancelou um pedido em até 7 dias | Proteção |
| `voltou_2d` | Voltou ao site em até 2 dias | Acompanha |
| `comprou_outro_item` | Comprou um produto que não estava no carrinho | Acompanha |
| `recomprou_30d` | Fez uma segunda compra em até 30 dias | Acompanha |
| `avaliou_produto` | Deixou avaliação de um produto comprado | Acompanha |

## Regra

- O financeiro fez a conta em 01/04: qualquer ganho na compra paga o lembrete, com ou sem cupom.
- O cupom custa 10% de cada pedido que o usa. Por isso a ordem de preferência é: primeiro uma versão sem cupom (B ou C); o D só se nenhuma sem cupom servir.
- Uma versão só lança se ganhar na compra em 7 dias e nenhuma proteção dela piorar.
- As métricas que acompanham vão no relatório. Elas não decidem.

## Antes do efeito

A divisão entre as quatro versões é checada antes de olhar qualquer métrica, como na aula «Desvio da proporção de alocação».
