# Segmentos e paradoxo de Simpson

Os arquivos da aula 13. Rode os comandos de dentro dessa pasta. Precisa do Python 3.9 ou mais novo, com o pandas (o NumPy vem junto).

| Arquivo | O que tem |
|---|---|
| `segmentos.py` | As funções da aula: `ler`, `taxas`, `composicao`, `divisao`, `estratificado`, `cortes`, `interacao` e `sorteio_sem_efeito` |
| `plano-checkout.md` | O plano do teste do checkout em uma página, com data, divisão por canal e cortes previstos |
| `visitas_checkout.csv` | As 30.000 visitas do teste do checkout, uma por linha |
| `plano-frete.md` | O plano do teste da calculadora de frete, para o exercício |
| `visitas_frete.csv` | As 40.000 visitas do teste da calculadora de frete |
| `diagnostico-modelo.md` | A folha do diagnóstico, para copiar e preencher no exercício |
| `gerar_dados.py` | O programa que gera os dois CSV |

Em `visitas_checkout.csv`, cada linha é uma visita: `id_visita`, `canal` (site ou app), `grupo` (A ou B), `regiao`, `cliente` (novo ou recorrente), `origem`, `periodo`, `dia`, `chegou_pagamento` (0 ou 1) e `comprou` (0 ou 1).

Em `visitas_frete.csv`: `id_visita`, `semana` (1 ou 2), `grupo`, `cliente`, `regiao`, `categoria`, `dispositivo`, `usou_calculadora` e `comprou`. A coluna `usou_calculadora` fica vazia no A, porque a página do A não tem calculadora.

As taxas saem como parte das visitas: 0,0773 é 7,73%. A diferença é sempre B menos A.

Para gerar os dois CSV de novo:

```bash
python3 gerar_dados.py
```

A saída é `visitas_checkout=30000 visitas_frete=40000`. Os arquivos saem iguais toda vez que você roda.

O `sorteio_sem_efeito` embaralha os grupos com o NumPy. Com outra versão do NumPy, o resultado pode mudar na terceira casa.

No exercício, preencha a parte 1 da `diagnostico-modelo.md` só com o `plano-frete.md`, antes de abrir o `visitas_frete.csv`.
