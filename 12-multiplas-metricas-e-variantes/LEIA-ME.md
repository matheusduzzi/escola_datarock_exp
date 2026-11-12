# Múltiplas métricas e variantes

Os arquivos da aula 12. Rode os comandos de dentro dessa pasta. Só usa a biblioteca padrão do Python 3.9 ou mais novo.

| Arquivo | O que tem |
|---|---|
| `familias.py` | As regras `bonferroni`, `holm` e `bh`, a leitura `ler` e o sorteio `simular` |
| `plano-pagina.md` | O plano do teste da página do produto, com data e o papel de cada métrica |
| `resultados_pagina.csv` | Os 16 testes da página: B e C contra A, em oito métricas |
| `plano-lembrete.md` | O plano do teste do lembrete de carrinho, para o exercício |
| `resultados_lembrete.csv` | Os 21 testes do lembrete: B, C e D contra A, em sete métricas |
| `politica-modelo.md` | A folha da política, para copiar e preencher no exercício |
| `gerar_dados.py` | O programa que gera os dois CSV |

Cada linha dos CSV é um teste. Ela traz a versão, a métrica e as contas de cada lado. Traz também a taxa na A e na versão, a diferença (versão menos A), o erro padrão e o p-valor de dois lados. As taxas são a parte das contas: 0,0761 é 7,61%.

Para gerar os dois CSV de novo:

```bash
python3 gerar_dados.py
```

A saída é `resultados_pagina=16 resultados_lembrete=21`. Os arquivos saem iguais toda vez que você roda.

No exercício, preencha a parte de cima da `politica-modelo.md` antes de abrir o `resultados_lembrete.csv`.
