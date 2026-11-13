# Revisão rápida de estatística

Cinco ideias que o curso usa desde a aula 01, cada uma com um exemplo curto. Os números aqui são outros, para você não ver a resposta do diagnóstico antes de tentar. Quem fez Estatística para decisão já viu tudo isso com mais calma; a aula indicada em cada seção é a de lá.

## 1. Ponto percentual e porcentagem

Uma taxa de abandono de carrinho foi de 20% para 25%. Ela subiu 5 pontos percentuais: 25 menos 20. Em relação ao começo, ela subiu 25%: 5 dividido por 20. As duas frases são verdadeiras e respondem perguntas diferentes. O que não dá é escrever "subiu 5%", porque aí ninguém sabe qual das duas contas você fez.

Em teste A/B, a diferença em pontos percentuais é a que entra no intervalo e no mínimo combinado. A porcentagem relativa ajuda a contar a história, sempre junto com a taxa de partida.

Para estudar mais: aula «Intervalo para proporção» de Estatística para decisão.

## 2. Cada taxa com o seu denominador

Num teste com 40 visitas no A, 10 compras, e 50 visitas no B, 15 compras, a taxa do A é 10 de 40 (25%) e a do B é 15 de 50 (30%). Cada grupo divide pelas suas próprias visitas. Visita que ficou sem grupo não entra em nenhum dos dois: ela não viu a versão A nem a B, pelo menos não que dê para saber.

No pandas, `groupby("grupo")` já deixa de fora a linha com grupo vazio. Por isso vale contar essas linhas à parte, com `isna().sum()`, e dizer quantas foram.

Para estudar mais: aulas «Ler e inspecionar CSV», «Selecionar, filtrar e conferir» e «Agrupar e verificar no pandas» de Primeiros passos em dados.

## 3. Intervalo da diferença, zero e mínimo que paga

Um teste termina com a diferença B menos A entre 0,5 e 1,5 ponto. O intervalo não passa pelo zero, então a diferença é estatisticamente diferente de zero a 5%. Se o time combinou antes que a mudança só paga a partir de 2 pontos, nem o melhor caso do intervalo chega lá. A decisão é não seguir, mesmo com significância.

A regra que o curso usa compara o intervalo inteiro com o mínimo combinado: todo acima, segue; todo abaixo, não segue; cruzando o mínimo, os dados ainda não decidem. Intervalo que passa pelo zero não prova que A e B são iguais. Ele diz que o teste não conseguiu separar os dois.

Para estudar mais: aulas «Intervalo de confiança e cobertura» e «P-valor, erros e relevância» de Estatística para decisão.

## 4. A margem cai com a raiz da amostra

A margem de erro de uma diferença cai com a raiz quadrada do número de visitas. Com 2.000 visitas por grupo e margem de 2 pontos, 8.000 visitas por grupo dão margem de 1 ponto: quatro vezes mais visitas para metade da margem. Dobrar as visitas tira só cerca de 30% da margem.

Poder é a chance de o teste dar significativo quando o efeito é do tamanho planejado. Com poder de 90%, em 10 testes iguais com aquele efeito, cerca de 9 dão significativo e 1 não dá. Esse que não dá é um falso negativo, também chamado de erro tipo II.

Para estudar mais: aulas «Margem de erro e sensibilidade» e «Poder e planejamento de amostra» de Estatística para decisão.

## 5. Muitas comparações e o que o p-valor diz

Se você compara 10 métricas a 5% e o B não muda nenhuma, espera ver meia métrica "significativa" por acaso: 10 vezes 0,05. A chance de pelo menos uma sair significativa é 1 menos 0,95 elevado a 10, cerca de 40%. O jeito mais simples de segurar isso divide o 5% pelo número de comparações: 0,05 dividido por 10 dá 0,005 para cada uma.

O p-valor é calculado supondo que o B não muda nada. Ele diz com que frequência apareceria uma diferença daquele tamanho ou maior, se essa suposição fosse verdadeira. Ele não é a chance de a suposição ser verdadeira e não mede o tamanho do efeito.

Para estudar mais: aulas «P-valor, erros e relevância» e «Famílias de testes e multiplicidade» de Estatística para decisão.
