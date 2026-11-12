# Dossiê do comitê de produto: segunda, 11/05/2026

Três testes da Loja Exemplo esperando decisão. Cada um traz o que foi combinado antes do início, como ele rodou, o resultado, o que custa e o que limita a decisão. As contagens estão em `resultados.csv`, e `python3 comite.py` aplica a regra de cada plano.

Quem senta no comitê: a Lia (produto), o Rui (financeiro), o Caio (dados) e a Bete, gerente da loja física.

## 1. Frete no topo do checkout

| Item | O que tem |
|---|---|
| Plano | Combinado de 13 a 14/08/2025, antes do início em 18/08/2025. Compra na mesma visita, sorteio por visita, 12.000 visitas, um olhar no fim |
| Mínimo e regra | 1 ponto de conversão (conta do Rui com o custo das consultas). Segue se o limite de baixo do intervalo de 95% chega a 1 ponto; não segue se nem o limite de cima chega |
| Execução | 12.000 de 12.000 visitas; 7 sem grupo; divisão A 5.997 e B 5.996, p = 0,993 |
| Resultado | A 607 compras em 5.997 visitas; B 596 em 5.996 |
| Custo | Cada visita do B consulta o sistema de frete, e cada consulta custa R$ 0,30 (fatura do sistema de frete) |
| O que aconteceu depois | O relatório saiu em 26/08/2025. Ninguém desligou o B. Desde 24/08/2025, metade das visitas do checkout continua vendo o frete no topo. O Rui achou na fatura de abril |
| Pedido que chegou | A Bia, do atendimento: "Deu empate, então deixa o B. Os clientes gostam de ver o frete antes" |

## 2. Botão verde no checkout

| Item | O que tem |
|---|---|
| Plano | Escrito pela Lia em 31/07/2025, antes do início em 04/08/2025. Mesma métrica, mesmo tamanho e mesma regra do frete |
| Mínimo e regra | 1 ponto de conversão (conta do financeiro com as duas semanas de desenvolvimento da troca). Mesma regra do pior caso |
| Execução | 12.000 de 12.000 visitas; 7 sem grupo; divisão A 5.999 e B 5.994, p = 0,964 |
| Resultado | A 608 compras em 5.999 visitas; B 685 em 5.994 |
| Custo | A troca definitiva custa duas semanas do time de desenvolvimento. O time tem uma janela livre em junho. O botão verde continua pronto na ferramenta de teste: rodar de novo não custa desenvolvimento |
| O que aconteceu depois | O relatório de agosto disse "os dados ainda não decidem", e ninguém decidiu. O botão de hoje continua no ar |
| Restrição | O checkout recebe 2.100 visitas por dia. Os dados de agosto têm nove meses |
| Pedido que chegou | O Caio: "1,29 passa de 1. Lança" |

## 3. "Retire hoje"

| Item | O que tem |
|---|---|
| Plano | Contrato de métricas de 01/02/2026, antes do início em 02/02/2026. Em 01/02, a Bete escolheu o teste aberto a toda conta que chega ao gatilho, por 12 semanas, até 26/04/2026. Dados fechados em 10/05/2026 |
| Métrica de sucesso | Compra em 7 dias. Lança se o intervalo de 95% de B menos A fica todo acima de zero e a estimativa chega a 2 pontos, com as proteções dentro do limite |
| Proteção do cliente | Reclamação da retirada em 14 dias. B menos A de 1 ponto ou mais, com intervalo todo acima de zero, barra o lançamento |
| Proteções da loja | Retiradas atrasadas: dois dias seguidos acima de 10% baixam o teto de 30 para 15 no dia seguinte; uma semana acima de 6% desliga o "Retire hoje". Vendas do balcão: semana abaixo de R$ 26.000 leva conversa com a Bete |
| Execução | Divisão A 11.250 e B 11.230 contas no gatilho, p = 0,89. Nenhum dia sem registro |
| Resultado | Compra em 7 dias: A 3.645 de 11.250; B 3.930 de 11.230. Reclamação da retirada: A 112 de 11.250; B 258 de 11.230 |
| As proteções da loja | Retiradas atrasadas por semana: de 2,9% a 5,6%, nenhuma semana acima de 6%. Dois dias seguidos acima de 10% aconteceram três vezes, sempre de sábado para domingo, e o teto baixou para 15 nas três segundas. Vendas do balcão: de R$ 27.410 a R$ 33.020 por semana |
| Por que reclamaram | No B, 170 das 258 reclamações têm o motivo "pedido não estava separado quando cheguei". 147 das 258 são de pedidos feitos no sábado. O sábado tem 11% das contas do gatilho |
| Sábado e o resto da semana | Contas do gatilho no sábado: A 1.271, B 1.269. Reclamações da retirada no sábado: A 20, B 147. Nos outros dias: A 92 de 9.979, B 111 de 9.961 |
| Custo | A pessoa a mais nas tardes é uma temporária, com contrato até 31/05/2026. A Bete decide se renova |
| Pedidos que chegaram | O Caio: "São 2,6 pontos de compra contra 1,3 de reclamação. Duas vendas por reclamação, lança". A Lia: "Lança sem o sábado, que o problema é ele" |
