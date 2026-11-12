# Listas de contas da aula «Randomizar e conferir grupos»

Uma linha é uma conta da Loja Exemplo. Os números são inventados. Não edite os arquivos à mão: os programas da aula leem estes arquivos como estão.

## clientes_retire.csv

A lista que a Lia mandou para o teste do "Retire hoje". É o export do cadastro tirado no domingo, 01/02/2026, véspera do início. Ele sai ordenado do jeito que o sistema exporta: mais pedidos primeiro. São 9.400 linhas.

| Coluna | O que é | Quando foi medida |
|---|---|---|
| `id_cliente` | O id da conta, como `C10542` | no cadastro |
| `status` | `ativa`, `encerrada` ou `bloqueada` | em 01/02/2026 |
| `tipo` | `cliente`, `funcionario` ou `teste` (conta que o time usa para testar o site) | em 01/02/2026 |
| `cadastro` | Data em que a conta foi criada | no cadastro |
| `ultimo_acesso` | Última vez que a conta entrou no site | até 01/02/2026 |
| `pedidos_90d` | Pedidos nos 90 dias antes de 01/02/2026 | até 01/02/2026 |
| `mora_perto` | `sim` se o endereço do cadastro fica a até 15 km da loja física | em 01/02/2026 |
| `usou_retirada` | `sim` se a conta já usou a retirada na loja em dois dias | até 01/02/2026 |

Para gerar de novo: `python3 gerar_clientes.py`, de dentro da pasta da aula. A saída é `clientes_retire.csv: 9400 linhas`, e o arquivo sai igual toda vez.

## clientes_pontos.csv

A lista do exercício, que a Marta mandou para o teste dos pontos em dobro. O cadastro foi tirado na sexta, 03/04/2026. O teste começou na segunda, 06/04. No dia 20/04, o analista da Marta colou na planilha a última coluna. São 6.303 linhas.

| Coluna | O que é | Quando foi medida |
|---|---|---|
| `id_cliente` | O id da conta, como `P20417` | no cadastro |
| `status` | `ativa`, `encerrada`, `bloqueada` ou `mesclada` (conta juntada em outra conta da mesma pessoa) | em 03/04/2026 |
| `tipo` | `cliente`, `funcionario` ou `teste` | em 03/04/2026 |
| `cadastro` | Data em que a conta foi criada | no cadastro |
| `compras_12m` | Compras com o cadastro informado nos 12 meses antes de 03/04/2026 | até 03/04/2026 |
| `gasto_12m` | Gasto dessas compras, em reais, com ponto no decimal | até 03/04/2026 |
| `usa_app` | `sim` se a conta entrou pelo aplicativo nos 12 meses antes | até 03/04/2026 |
| `compras_desde_inicio` | Compras com cadastro de 06/04 a 19/04 | colada em 20/04/2026 |
