# Três desenhos para o "Retire hoje"

A mesma mudança, sorteada de três jeitos. É a seção 3 da aula «Cliente, sessão e loja».

A mudança: mostrar "Retire hoje" na escolha da entrega, para compras no site até as 16h, com retirada na loja física no mesmo dia. Hoje a retirada leva dois dias úteis.

Os fatos do caso:

- Quem comprou no site em outubro fez, em média, 3,4 visitas nos 7 dias antes da compra.
- 35% das visitas são de quem não entrou na conta. O site só reconhece essa pessoa pelo cookie do navegador.
- O "Retire hoje" aparece na escolha da entrega, e para chegar ali o cliente já entrou na conta.
- A loja física tem uma equipe só. Ela atende o balcão e separa os pedidos de retirada, uns 40 por dia. O estoque da loja também é um só.

| | Por sessão | Por cliente | Por loja |
|---|---|---|---|
| Quem cai em cada grupo | Cada visita, sorteada de novo | Cada conta, uma vez, até o fim | A loja inteira |
| O que vaza | A mesma pessoa vê as duas versões; o que viu numa visita pesa na compra da outra | A equipe e o estoque da loja atendem os dois grupos | Quase nada: a loja inteira muda junto |
| Como segurar | Não dá: a pessoa leva a lembrança de uma visita para a outra | Teto de 30 pedidos de "Retire hoje" por dia; proteção: atraso das retiradas de dois dias e vendas do balcão | Precisa de muitas lojas para sortear |
| A linha da conta | A visita | O cliente, com visitas e compras somadas | A loja |
| Serve para o "Retire hoje"? | Não | Sim, com o teto | Não: a Loja Exemplo tem uma loja física |

Com quatro visitas sorteadas uma a uma, a chance de todas caírem no mesmo grupo é de 1 em 8 (2 × 0,5 × 0,5 × 0,5 × 0,5).

Para ver o que a conta errada faz, rode `python3 sorteio_e_conta.py` nessa pasta.
