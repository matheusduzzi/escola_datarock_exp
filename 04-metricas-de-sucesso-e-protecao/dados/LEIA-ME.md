# Dados da aula «Métricas de sucesso e proteção»

As 4 semanas antes do teste "Retire hoje" na Loja Exemplo: de segunda, 05/01/2026, a domingo, 01/02/2026. O teste começa na segunda, 02/02. Nessas semanas ninguém viu o "Retire hoje": a retirada na loja física levava dois dias úteis para todo mundo.

| Arquivo | Uma linha é | Colunas |
|---|---|---|
| `alocacao_retire.csv` | uma conta sorteada | `id_cliente`, `teste`, `grupo` (`A` retirada em dois dias, `B` "Retire hoje") |
| `gatilhos_antes.csv` | uma vez em que a conta chegou à escolha da entrega com um produto em estoque na loja | `id_cliente`, `data` |
| `pedidos_antes.csv` | um pedido pago no site | `id_pedido`, `id_cliente`, `data`, `valor` (em reais, sem o frete), `entrega` (`casa` ou `retirada`) |
| `atendimento_antes.csv` | um contato do cliente com o atendimento | `id_cliente`, `data`, `assunto` (`retirada`, `entrega` ou `troca`) |
| `loja_dias_antes.csv` | um dia da loja física | `data`, `retiradas` (retiradas previstas para o dia), `retiradas_atrasadas` (as que não estavam separadas na hora combinada), `vendas_balcao` (em reais) |

A alocação é a tabela da aula «Randomizar e conferir grupos»: as 9.000 contas, 4.513 no A e 4.487 no B. O grupo já existe antes do início porque o sorteio foi feito no domingo. Nas 4 semanas de antes, ele só serve para ver se a métrica sai parecida nos dois lados.

O gatilho é anotado do mesmo jeito para as contas dos dois grupos. Uma conta pode ter vários gatilhos; o contrato usa o primeiro. Há pedidos de contas que nunca passaram pelo gatilho e pedidos feitos antes do gatilho: eles não entram na conta da métrica.

A tabela da loja conta todas as retiradas da loja, de qualquer cliente, e não só as das 9.000 contas. A loja é uma só e atende os dois grupos.

Datas no formato ano-mês-dia. Valores com ponto decimal, como o programa grava.

## Gerar de novo

```bash
python3 gerar_antes.py
```

A saída é `gatilhos=3708 pedidos=2295 atendimento=428 loja_dias=28`. O gerador só usa a biblioteca padrão e sai igual toda vez. O começo dele conta como os dados nascem: abra depois de fazer as contas da aula.
