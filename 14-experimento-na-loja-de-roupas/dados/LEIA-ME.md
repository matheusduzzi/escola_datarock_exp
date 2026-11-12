# Dados da rede Trama

Duas tabelas, geradas por `gerar_dados.py` nesta pasta. O programa só usa a biblioteca padrão e sai igual toda vez:

```bash
python3 gerar_dados.py
```

A saída é `lojas=24 semanas=648 cidades=10`.

## lojas.csv

| Coluna | O que é |
|---|---|
| `loja` | código da loja, de L01 a L24 |
| `cidade` | cidade da loja |
| `area_m2` | área de venda, em metros quadrados |
| `provadores` | número de cabines de provador |

## semanas.csv

Uma linha por loja e semana, de segunda, 19/01/2026, a domingo, 26/07/2026: 27 semanas. Nenhuma dessas semanas teve o look pronto.

| Coluna | O que é |
|---|---|
| `loja` | código da loja |
| `semana` | a segunda-feira que abre a semana |
| `entradas` | pessoas que entraram, pelo sensor da porta |
| `vendas` | venda da semana, em reais |
| `devolvido_7d` | quanto das vendas da semana voltou em até 7 dias, em reais |
| `devolvido_30d` | quanto das vendas da semana voltou em até 30 dias, em reais |
| `falta_tamanho` | vezes que o botão "tamanho em falta" foi apertado no caixa |

A tabela para em 26/07 porque, no dia do plano (04/09/2026), essa é a última semana em que o prazo de 30 dias da devolução e os 7 dias do sistema já passaram.
