# Contrato de métricas: teste `retire-hoje`

Escrito no domingo, 01/02/2026, antes do início (segunda, 02/02). Lido e aceito pela Lia (produto) e pela gerente da loja física no mesmo dia. Nenhum número do teste existia quando ele foi escrito.

## Quem entra na conta

As 9.000 contas da tabela de alocação. Entra na conta a que passa pelo gatilho: chega à escolha da entrega com um produto em estoque na loja, do primeiro ao último dia do teste. O gatilho é anotado igual nos dois grupos. Uma linha por conta, com o primeiro gatilho. Quem passa pelo gatilho fica na conta, compre ou não, use o "Retire hoje" ou não.

O último dia do teste sai da aula «Efeito mínimo detectável, amostra e duração». Os dados fecham 14 dias depois desse dia, para toda conta ter as janelas inteiras.

## Métrica de sucesso

| Campo | Compra em 7 dias |
|---|---|
| Numerador | Contas do denominador com pelo menos um pedido pago do dia do primeiro gatilho até 6 dias depois |
| Denominador | Contas que passaram pelo gatilho no teste |
| Janela | 7 dias de calendário a partir do dia do primeiro gatilho, contando esse dia; igual para toda conta |
| Como é hoje | 32,6% no A e 31,0% no B, nas duas semanas antes do início (`ensaio.py`) |
| Critério de sucesso | Diferença B - A com intervalo de 95% todo acima de zero e estimativa de pelo menos 2 pontos, com as proteções dentro do limite |

O mínimo de 2 pontos é a conta da Lia: a hora extra da equipe nas tardes do "Retire hoje" só se paga com 2 pontos a mais de compra.

## O que cada resultado decide

| Resultado | Decisão |
|---|---|
| Intervalo todo acima de zero, estimativa de 2 pontos ou mais, proteções dentro | Lança com o teto de 30 por dia e acompanha a fila da loja |
| Intervalo todo acima de zero, estimativa abaixo de 2 pontos | O efeito existe e não paga a equipe. Não lança como está |
| Intervalo pega o zero | Os dados não mostram efeito. Não lança agora. Não quer dizer que o "Retire hoje" não funciona |
| Intervalo todo abaixo de zero | O "Retire hoje" piorou a compra. Não lança |
| Uma proteção passou do limite | Não lança, mesmo com a compra subindo. Primeiro descobre o porquê |

## Métricas de proteção

| Métrica | Numerador | Denominador | Janela | Como é hoje | Limite e o que acontece |
|---|---|---|---|---|---|
| Reclamação da retirada | Contas do denominador com contato de assunto `retirada` no atendimento | Contas que passaram pelo gatilho | 14 dias a partir do primeiro gatilho | 1,1% no A e 0,7% no B | Na decisão: B - A de 1 ponto ou mais, com intervalo todo acima de zero, barra o lançamento |
| Retiradas atrasadas na loja | Retiradas de dois dias que não estavam separadas na hora | Retiradas de dois dias previstas no dia | Cada dia e cada semana do teste, comparados com as 4 semanas antes | 2,8% nas 4 semanas; por semana, de 1,5% a 4,2%; pior dia 10,6% | Durante o teste: dois dias seguidos acima de 10% baixam o teto de 30 para 15 no dia seguinte; uma semana acima de 6% desliga o "Retire hoje" e chama a gerente |
| Vendas do balcão | Soma das vendas do balcão na semana | (total da semana) | Cada semana do teste, comparada com as 4 semanas antes | De R$ 27.847 a R$ 34.135 por semana | Durante o teste: semana abaixo de R$ 26.000 leva a conversa com a gerente antes da semana seguinte |

As duas proteções da loja comparam o teste com as semanas de antes, e não o A com o B: a equipe e o balcão atendem os dois grupos. Por isso elas servem de alarme. Elas não medem o efeito do "Retire hoje".

## Números que acompanham, sem decidir

Sempre com o numerador e o denominador ao lado.

| Número | Por que não decide |
|---|---|
| Receita por conta em 7 dias (receita na janela / contas que passaram pelo gatilho, com zero para quem não comprou) | Mostra se a compra a mais é de pedido pequeno. É o candidato a sucesso de um próximo teste |
| Pedidos por conta em 7 dias | Explica a receita e o tíquete |
| Tíquete por pedido (receita / pedidos) | O denominador é o pedido, e o "Retire hoje" pode mudar quantos pedidos existem |
| Compra por visita (pedidos / visitas) | O denominador é a visita, e o "Retire hoje" pode mudar quantas visitas o cliente faz antes de comprar |
| Uso do "Retire hoje" no B | Só existe no B. Não tem com o que comparar no A |

## O que o contrato não muda depois do início

A métrica de sucesso, o mínimo de 2 pontos, as janelas, quem entra na conta e os limites de proteção. Se algo precisar mudar, a mudança é escrita com a data e o motivo, antes de qualquer análise, e a análise mostra as duas versões.
