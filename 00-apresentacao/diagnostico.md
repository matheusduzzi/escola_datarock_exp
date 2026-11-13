# Diagnóstico: por onde começar em Experimentação e teste A/B

A Lia é do time de produto da Loja Exemplo. Numa segunda-feira ela me mandou quatro frases sobre testes da loja: "o botão novo converte 0,6% a mais", "no teste do cupom o B ganhou com folga", "o teste do frete deu empate, então tanto faz" e "olhei 20 métricas e o tempo na página melhorou com p = 0,03". Cada frase tinha uma conta certa por trás e uma leitura errada na frente. Antes de responder, eu refiz as contas. As cinco tarefas abaixo são essas contas.

Elas usam o que o curso pede de entrada: diferença entre taxas, um CSV lido e agrupado no pandas, intervalo de confiança, tamanho de amostra e o cuidado com muitas comparações. O diagnóstico não é prova e não tem nota. Ele mostra por onde você começa. Anote na [folha de respostas](minhas-respostas.md) a conta que fez, o comando que rodou e a saída que apareceu. Só depois compare com as respostas comentadas.

As tarefas 1, 3, 4 e 5 são de lápis e papel ou calculadora. A tarefa 2 roda de dentro da pasta `00-apresentacao/`:

```bash
cd 00-apresentacao
python3 tarefa2.py
```

No Windows, troque `python3` por `py`. Se uma conta travar, a [revisão rápida de estatística](preparacao-estatistica.md) tem um exemplo curto de cada ideia.

## Tarefa 1. Diferença entre duas taxas

No teste do botão, o grupo A teve 200 compras em 5.000 visitas. O grupo B teve 230 compras em 5.000 visitas.

1. Qual a taxa de conversão de cada grupo, em porcentagem?
2. Quanto o B ficou acima do A, em pontos percentuais?
3. Quanto o B ficou acima do A em relação ao A, em porcentagem?
4. A Lia escreveu "o botão novo converte 0,6% a mais". O que está errado nessa frase e como você escreveria?

## Tarefa 2. Visitas por grupo no pandas

`dados/visitas_cupom.csv` tem 30 visitas de um teste de cupom. Uma linha é uma visita. A coluna `grupo` diz se a visita viu a versão A ou a B; em 4 visitas o grupo não foi gravado e a célula ficou vazia. A coluna `converteu` vale 1 quando a visita terminou em compra.

Em `tarefa2.py`, monte uma tabela com uma linha por grupo e estas colunas:

| Coluna | O que é |
|---|---|
| `grupo` | A ou B |
| `visitas` | quantas visitas o grupo teve |
| `compras` | quantas dessas visitas compraram |
| `taxa_pct` | compras divididas por visitas do próprio grupo, em porcentagem, com uma casa decimal |

As visitas sem grupo ficam fora da tabela. Guarde a tabela final na variável `resultado` e mostre com `print(resultado)`. Mostre também quantas visitas ficaram sem grupo. Anote na folha:

1. A saída de `print(resultado)` e o número de visitas sem grupo.
2. O que aconteceria com a taxa do A se as visitas sem grupo fossem contadas como A.
3. O que aconteceria com as duas taxas se você dividisse as compras pelas 30 visitas.
4. A Lia disse "o B ganhou com folga". Com essas visitas, o que você responderia a ela?

## Tarefa 3. Intervalo da diferença e mínimo que paga a mudança

O time combinou antes do teste que trocar a página só paga se a conversão subir pelo menos 1 ponto percentual. Quatro testes terminaram com estes intervalos de 95% para a diferença B menos A, em pontos percentuais:

| Teste | Intervalo da diferença |
|---|---|
| a | de 1,2 a 2,8 |
| b | de 0,2 a 2,4 |
| c | de −1,3 a 0,9 |
| d | de −0,4 a 3,1 |

1. Em quais testes a diferença é estatisticamente diferente de zero, a 5%?
2. Para cada teste, qual a decisão: seguir com o B, não seguir ou "com esses dados não dá para saber"?
3. O teste c é o do frete, que a Lia chamou de empate. "Tanto faz" é a leitura certa? O que o intervalo diz?

## Tarefa 4. Amostra, margem e poder

Num teste com 6.000 visitas por grupo e conversão perto de 10%, a margem de erro da diferença saiu cerca de 1,1 ponto percentual para cada lado.

1. Quantas visitas por grupo seriam precisas para a margem cair para cerca de 0,55 ponto?
2. E qual seria a margem com 1.500 visitas por grupo?
3. O plano de um teste diz "poder de 80% para um efeito de 1 ponto". Se o efeito real for mesmo de 1 ponto e o time rodar esse teste 10 vezes, em cerca de quantas o resultado sai significativo? Como se chama o erro nas outras?

## Tarefa 5. Muitas comparações e o p-valor

A Lia olhou 20 métricas no mesmo teste, cada uma comparada a 5%. Suponha que o B não muda nenhuma delas e que as comparações são independentes.

1. Quantas métricas você espera ver "significativas" só por acaso?
2. Qual a chance de pelo menos uma sair significativa?
3. Se o time quisesse manter em 5% a chance de qualquer falso alarme nas 20, qual limite cada comparação teria de usar pelo jeito mais simples de corrigir?
4. A métrica de tempo na página saiu com p = 0,03. Qual destas leituras está certa?
   - (a) Há 3% de chance de o B não mudar o tempo na página.
   - (b) Se o B não mudasse nada, uma diferença desse tamanho ou maior apareceria em cerca de 3% dos testes.
   - (c) O B aumenta bastante o tempo na página.

## Depois de responder

Compare com as respostas comentadas que vêm na apresentação do curso, tarefa por tarefa. A tabela "Antes de começar" da apresentação diz o que estudar em cada tarefa em que você travou.
