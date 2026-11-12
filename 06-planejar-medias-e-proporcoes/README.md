# 06. Planejar médias e proporções

Os arquivos da aula «Planejar médias e proporções» do curso Experimentação e teste A/B.

## O que tem nessa pasta

| Arquivo | Para quê |
|---|---|
| `amostra.py` | As contas da aula: visitas para uma proporção, pedidos para uma média, pedidos em visitas, poder de um tamanho escolhido e os sorteios que conferem a conta |
| `plano-amostra.md` | A folha do exercício, com as tabelas das hipóteses, da sensibilidade e as sete linhas do plano. Salve uma cópia com o seu nome |

A aula não tem dados próprios. A conversão de hoje sai dos testes da loja, em `../dados/loja/` (o `ab_botao.csv` na aula e o `ab_frete.csv` no exercício). O resto são as hipóteses escritas no texto.

## Como rodar

Abra o Python dentro dessa pasta:

```bash
python3
```

Cole os blocos da aula na ordem, a partir da seção 2. Cada bloco importa do `amostra.py` as funções que usa. Os sorteios da seção 5 levam um ou dois segundos.

Os sorteios saem iguais toda vez que você roda o bloco inteiro, desde a linha do `np.random.default_rng`. Se você rodar só uma parte, o sorteio continua de onde parou e os números mudam um pouco.

As contas usam só a biblioteca padrão do Python. A leitura do CSV usa o pandas, e os sorteios, o NumPy, que vem com ele. Se aparecer `No module named 'pandas'`, volte ao README do kit e instale pelo `requirements.txt`. No Windows, troque `python3` por `py`.

Se uma função recusar a entrada, leia a mensagem. As taxas entram como fração: 10% é `0.10`, e não `10`.

Se precisar de ajuda, deixe um comentário na aula. Conte o objetivo, o comando que você rodou, a saída que apareceu e o que já tentou, sem dados pessoais.
