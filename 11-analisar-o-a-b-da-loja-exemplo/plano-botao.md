# Plano do teste do botão verde

Escrito pela Lia na quinta, 31/07/2025, antes do início. Lido pelo Caio e pelo financeiro no mesmo dia.

## A pergunta

O botão de compra verde e maior faz mais visitas comprarem do que o botão de hoje? Trocar o botão custa duas semanas de desenvolvimento.

## O que fica combinado

- **Quem entra:** toda visita que chega ao checkout a partir da segunda, 04/08/2025. O sorteio divide cada visita meio a meio entre A (botão de hoje) e B (botão verde maior).
- **Métrica que decide:** compra na mesma visita. Numerador: visitas que compraram. Denominador: visitas sorteadas com grupo.
- **Mínimo que paga a troca:** 1 ponto de conversão, conta do financeiro com as duas semanas de desenvolvimento.
- **Tamanho e parada:** as primeiras 12.000 visitas, perto de 6 dias de checkout. Ninguém olha a conversão antes de chegar às 12.000.
- **Antes do efeito:** visitas sem grupo até 1% do total e divisão dos grupos com p acima de 0,001. Se uma das duas falhar, a análise para até alguém achar o motivo.
- **Regra de decisão:** intervalo de 95% da diferença B menos A. Segue se o limite de baixo chega a 1 ponto. Não segue se nem o limite de cima chega. Nos outros casos, os dados ainda não decidem.

## O que o relatório lê

```plano
teste: botão verde no checkout
combinado_em: 2025-07-31
inicio: 2025-08-04
dados: ../dados/loja/ab_botao.csv
unidade: visita
metrica: converteu
comparacao: B (botão verde maior) menos A (botão de hoje)
minimo_pontos: 1
visitas_planejadas: 12000
sem_grupo_max_pct: 1
linha_divisao: 0.001
nivel: 95
regra: pior_caso
```
