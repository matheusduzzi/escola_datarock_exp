# Pedido: o contrato do teste do frete no carrinho

A Lia escreveu na quarta, 25/02/2026:

> Quero refazer o teste do frete com a página nova. Agora o valor do frete aparece já no carrinho, calculado pelo CEP da conta, e o carrinho mostra quanto falta para o frete grátis, que vale para pedidos acima de R$ 199. Da outra vez só olhamos a conversão, e cada um leu o resultado de um jeito. O Caio quer decidir pelo tíquete médio, que "com certeza sobe". O financeiro quer saber das devoluções. E o time do site tem medo de o carrinho ficar lento, porque o cálculo do frete chama outro sistema. O teste liga na segunda, 02/03. Me manda o contrato antes.

O plano, já fechado:

- O sorteio divide a conta, pelo nome de teste `frete-carrinho`. O grupo A vê o carrinho de hoje, com o frete só no fim da compra. O grupo B vê o frete no carrinho e quanto falta para o frete grátis.
- O gatilho é a conta abrir o carrinho com pelo menos um produto. O servidor anota cada abertura nos dois grupos, antes de a página carregar.
- O último dia do teste ainda vai ser calculado.

Os números de hoje, que o Caio tirou das 4 semanas antes:

| Número | Hoje |
|---|---|
| Contas que abrem o carrinho e compram em 7 dias | 28% |
| Receita por conta que abre o carrinho, em 7 dias: valor dos produtos, sem o frete, com zero para quem não compra | R$ 54,60 |
| Tíquete por pedido, sem o frete | R$ 182,00 |
| Pedidos devolvidos | 6 de cada 100 pedidos; o cliente pode pedir a devolução até 30 dias depois do pedido |
| Aberturas do carrinho por conta, em 7 dias | 2,6 em média |
| Tempo até o carrinho carregar | 1,1 s na mediana; 9 de cada 10 em até 2,4 s |
| Aberturas do carrinho que fecham antes de carregar | 2 de cada 100 |

O que cada um disse:

- **Financeiro:** "O cálculo no carrinho custa uma taxa por consulta ao sistema de frete. A página nova só se paga se a receita por conta que abre o carrinho subir pelo menos R$ 1,50 em 7 dias. E cada pedido devolvido custa R$ 22 de frete de volta: se o B tiver 1 pedido devolvido a mais a cada 100 contas, a conta não fecha."
- **Lia:** "Não aceito perder mais de 1 ponto de compra, mesmo que a receita suba."
- **Time do site:** "Mais de 300 ms a mais na mediana do carregamento é problema. E a saída antes de carregar não pode subir."
- **Caio:** "Com o frete grátis à vista, o pessoal põe mais coisa no carrinho. O tíquete sobe, pode apostar. Decide por ele."

O arquivo do teste antigo do frete é `../dados/loja/ab_frete.csv`. Ele tem uma linha por visita e três colunas: `id_visita`, `grupo` e `converteu`.
