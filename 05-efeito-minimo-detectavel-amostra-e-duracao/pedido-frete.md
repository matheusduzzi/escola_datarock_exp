# O pedido do exercício: cenários do frete no carrinho

A Lia escreveu na sexta, 27/02/2026, depois de receber o contrato do frete no carrinho:

> O contrato está aceito. Agora o financeiro quer saber quando sai a resposta. O contrato com o sistema de frete vence em 30/06, e eles precisam decidir até a sexta, 26/06, se renovam por um ano. O teste liga na segunda, 02/03. Quantas semanas ele fica no ar? O Caio diz que 8 semanas sobram.

O que já está no contrato:

- A métrica de sucesso é a receita por conta que abre o carrinho, em 7 dias, com zero para quem não compra. Hoje é R$ 54,60. O mínimo do financeiro é R$ 1,50 a mais por conta.
- A compra em 7 dias é uma métrica de proteção. Hoje é 28%. A Lia não aceita perder mais de 1 ponto, e o teste precisa conseguir ver uma perda desse tamanho.
- O sorteio divide a conta, meio a meio, pelo nome `frete-carrinho`. Toda conta que abre o carrinho durante o teste entra no sorteio, sem teto.
- Intervalo de 95%, dos dois lados. Poder de 80%.
- Os dados fecham 36 dias depois do último dia do teste: 6 dias da janela de compra de quem abre o carrinho no último dia, mais 30 de prazo de devolução.

Os números que o Caio mandou, das 4 semanas de fevereiro:

| Número | Fevereiro |
|---|---|
| Contas diferentes que abriram o carrinho | 50.400, perto de 12.600 por semana |
| Desvio da receita por conta em 7 dias | R$ 96 |

E o Caio:

> 8 semanas dá 100 mil contas. Para ver R$ 1,50 isso sobra. E se no fim faltar um pouco, a gente estica uma semana.
