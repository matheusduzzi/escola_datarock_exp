# Kit do curso Experimentação e teste A/B

Os arquivos que você usa nas aulas: o diagnóstico, a revisão rápida de estatística e os dois testes A/B da Loja Exemplo. Cada aula traz a sua pasta com os dados e programas dela.

## Como o kit está organizado

| Pasta | O que tem |
|---|---|
| `00-apresentacao/` | O [diagnóstico](00-apresentacao/diagnostico.md), a [revisão rápida de estatística](00-apresentacao/preparacao-estatistica.md), os dados e o programa da tarefa 2, a [folha de respostas](00-apresentacao/minhas-respostas.md), a [folha da ordem de estudo](00-apresentacao/minha-ordem.md) e a `primeira_olhada.py`, que mostra os testes do botão e do frete. |
| `dados/loja/` | Os testes do botão e do frete da Loja Exemplo, 12.000 visitas cada. Ver [dados/loja/LEIA-ME.md](dados/loja/LEIA-ME.md). |
| `NN-titulo/` | Uma pasta por aula, com o número e o título da aula. Elas entram no kit junto com as aulas. |

Os comandos das aulas rodam de dentro da pasta da aula. Quando uma aula usa os testes da loja, ela diz o caminho, por exemplo `../dados/loja/ab_botao.csv`.

## Do que você precisa

- Python 3.9 ou mais novo, com o pandas. É o ambiente de Primeiros passos em dados: SQL e Python para quem está migrando; se você ainda não preparou o seu, a aula 03. Preparar o ambiente, de lá, mostra como.
- Um editor de código e um terminal.

O NumPy vem junto com o pandas. O SciPy e a biblioteca de gráficos entram nas aulas que usam cada um, com a versão e o comando de instalação. As aulas mostram o código pronto e explicam o que cada parte calcula.

Na pasta do kit, instale o que o diagnóstico usa:

```bash
python3 -m pip install -r requirements.txt
```

E veja se funcionou:

```bash
cd 00-apresentacao
python3 tarefa2.py
```

A saída mostra as cinco primeiras visitas do teste do cupom, com as colunas `id_visita`, `grupo` e `converteu`. Uma delas aparece com `NaN` no grupo: é uma das visitas sem grupo da tarefa 2. Se aparecer `No module named 'pandas'`, o `pip` instalou em outro Python. Rode `python3 -m pip install pandas` com o mesmo `python3` que você usa para rodar o programa. No Windows, troque `python3` por `py`.

Para gerar de novo os testes da loja:

```bash
cd ../dados/loja
python3 gerar.py
```

A saída é `ab_botao=12000 ab_frete=12000 visitas_sem_grupo_por_teste=7`. O gerador só usa a biblioteca padrão e sai igual toda vez.

## Se precisar de ajuda

Deixe um comentário na aula. Conte o objetivo, o comando que você rodou, a saída que apareceu e o que já tentou, sem dados pessoais.

## Licença

A licença de uso e redistribuição do kit ainda vai ser definida pela Escola Datarock. Até lá, use os arquivos para estudar o curso. Os dados da Loja Exemplo são inventados e foram gerados pelos programas do próprio kit.

## Aulas com arquivos neste kit

| Pasta | Aula |
|---|---|
| [00-apresentacao/](00-apresentacao/) | Apresentação |
| [01-pergunta-causal-e-alternativas/](01-pergunta-causal-e-alternativas/) | Pergunta causal e alternativas |
| [02-cliente-sessao-e-loja/](02-cliente-sessao-e-loja/) | Unidade e alocação |
| [03-randomizar-e-conferir-grupos/](03-randomizar-e-conferir-grupos/) | Randomizar e conferir grupos |
| [04-metricas-de-sucesso-e-protecao/](04-metricas-de-sucesso-e-protecao/) | Métricas e guardrails |
| [05-efeito-minimo-detectavel-amostra-e-duracao/](05-efeito-minimo-detectavel-amostra-e-duracao/) | MDE, amostra e duração |
| [06-planejar-medias-e-proporcoes/](06-planejar-medias-e-proporcoes/) | Planejar médias e proporções |
| [07-instrumentar-e-testar-a-a/](07-instrumentar-e-testar-a-a/) | Instrumentar e testar A/A |
| [08-desvio-da-proporcao-de-alocacao/](08-desvio-da-proporcao-de-alocacao/) | Desvio da proporção de alocação |
| [09-parada-e-observacoes-repetidas/](09-parada-e-observacoes-repetidas/) | Parada e observações repetidas |
| [10-novidade-selecao-e-contaminacao/](10-novidade-selecao-e-contaminacao/) | Novidade, seleção e contaminação |
| [11-analisar-o-a-b-da-loja-exemplo/](11-analisar-o-a-b-da-loja-exemplo/) | Analisar o A/B da Loja Exemplo |
| [12-multiplas-metricas-e-variantes/](12-multiplas-metricas-e-variantes/) | Múltiplas métricas e variantes |
| [13-segmentos-e-paradoxo-de-simpson/](13-segmentos-e-paradoxo-de-simpson/) | Segmentos e paradoxo de Simpson |
| [14-experimento-na-loja-de-roupas/](14-experimento-na-loja-de-roupas/) | Experimento na loja de roupas |
| [15-intencao-de-tratar-e-adesao/](15-intencao-de-tratar-e-adesao/) | Intenção de tratar e adesão |
| [16-ponte-credito-politica-alternativa/](16-ponte-credito-politica-alternativa/) | Ponte Crédito: política alternativa |
| [17-comite-de-decisao/](17-comite-de-decisao/) | Comitê de decisão |
