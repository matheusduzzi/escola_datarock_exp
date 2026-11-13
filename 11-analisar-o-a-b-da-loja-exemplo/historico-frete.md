# Mensagens do teste do frete no topo

O grupo do time de produto, copiado na ordem em que as mensagens chegaram. O arquivo do teste é `../dados/loja/ab_frete.csv`, com uma linha por visita e as colunas `id_visita`, `grupo` e `converteu`.

**Quarta, 13/08/2025, 09:10. Lia (produto):**
> O próximo teste é o frete no topo. No B, o valor do frete para o CEP da visita aparece no topo da página do checkout, junto do total. O A fica como hoje, com o frete só no fim. Começa na segunda, 18/08. Mesmo formato do botão: sorteio por visita, as primeiras 12.000 visitas do checkout, a métrica é a compra na mesma visita, e ninguém olha a conversão antes das 12.000.

**Quarta, 13/08/2025, 11:30. Rui (financeiro):**
> O frete no topo chama o sistema de frete em toda visita do checkout, e cada consulta custa. Pela minha conta, só paga com 1 ponto a mais de conversão.

**Quarta, 13/08/2025, 15:00. Caio (dados):**
> Para a parte de antes do efeito, sugiro as linhas do botão: até 1% de visitas sem grupo e p da divisão acima de 0,001.

**Quinta, 14/08/2025, 10:00. Lia:**
> Fechado com as linhas do Caio. A regra também é a do botão: intervalo de 95% da diferença B menos A, e só segue se o limite de baixo chegar ao mínimo do Rui.

**Sexta, 15/08/2025, 17:45. Caio:**
> E se na quarta o B estiver muito na frente? Dá para parar e já ligar.

**Sexta, 15/08/2025, 18:02. Lia:**
> Não. Olha uma vez, nas 12.000, como está combinado.

**Sábado, 23/08/2025, 16:20. Caio:**
> Chegou nas 12.000 visitas. O sorteio já parou.

**Segunda, 25/08/2025, 09:20. Caio:**
> Deu -0,18 ponto, p = 0,74. Empate. Aposto que no celular o frete no topo ganha. Dá para separar por celular?

**Segunda, 25/08/2025, 10:05. Bia (design):**
> Se é empate, deixa o B. A página fica mais clara e não perde venda.

**Segunda, 25/08/2025, 10:40. Lia:**
> Rui, e se o mínimo fosse meio ponto? Aí talvez dê para ficar com o B.

**Segunda, 25/08/2025, 11:00. Lia:**
> Para o comitê eu preciso do relatório do frete, do jeito do botão: o plano, a execução, o efeito com o intervalo e a decisão, e que qualquer um consiga refazer. E me diz o que responder para a Bia e para o Caio.
