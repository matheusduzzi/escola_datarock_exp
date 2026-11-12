# Cenários de viabilidade: teste `retire-hoje`

Escrito no domingo, 01/02/2026, antes do início em segunda, 02/02/2026.
Para: Lia (produto) e a gerente da loja.

## A pergunta

A gerente decide na segunda, 16/03, se contrata de vez a pessoa que separa os pedidos nas tardes. O teste responde até lá se o "Retire hoje" traz os 2 pontos de compra em 7 dias que pagam essa pessoa?

## As hipóteses

| Hipótese | Valor | De onde veio |
|---|---|---|
| Métrica de sucesso | Compra em 7 dias, por conta que passou pelo gatilho | Contrato de métricas de 01/02 |
| Como está hoje | 32% | Ensaio do contrato nas 4 semanas de janeiro: 32,6% no A e 31,0% no B |
| O mínimo que paga | 2 pontos, de 32% para 34% | Conta da Lia com a gerente: a pessoa a mais nas tardes |
| Quanto a métrica varia | Sai da própria taxa: 0,32 × 0,68 | Compra é 0 ou 1 por conta |
| Linha do teste e poder | Intervalo de 95%, dos dois lados; poder de 80% | Contrato de métricas; hábito da loja |
| Divisão | Meio a meio | Sorteio pelo id com o nome `retire-hoje` |
| Contas novas no gatilho por semana, só as 9.000 | 662,5 | 2.650 contas em 4 semanas de janeiro (653, 682, 641 e 674) |
| Teto, só as 9.000 | 9.000 contas | Regra de quem entra: entrou no site nos 30 dias antes do início |
| Contas novas no gatilho por semana, teste aberto | 1.505; e 1.204 (20% a menos) | Time do site: 6.020 contas diferentes no gatilho nas 4 semanas de janeiro. Em janelas longas, parte delas já passou antes, e esse número eu não tenho |
| Fim dos dados | Último dia do teste + 13 dias | Janela de 14 dias da reclamação, contando o dia do gatilho |

## Os cenários

Saída de `python3 cenarios.py cenarios-retire.csv --decidir-ate 2026-03-16`.

| Cenário | Contas por grupo | Vê a partir de | Poder para 2 pontos | Precisa | Último dia | Dados até | Decide até 16/03 |
|---|---|---|---|---|---|---|---|
| 9.000 em 4 semanas | 1.325 | 5,2 pontos | 19% | não cabe | 01/03 | 14/03 | sim |
| 9.000 em 8 semanas | 2.650 | 3,6 pontos | 34% | não cabe | 29/03 | 11/04 | não |
| 9.000 em 14 semanas | 4.500 (teto) | 2,8 pontos | 52% | não cabe | 10/05 | 23/05 | não |
| Aberto em 4 semanas | 3.010 | 3,4 pontos | 38% | 12 semanas | 01/03 | 14/03 | sim |
| Aberto em 12 semanas | 9.030 | 2,0 pontos | 82% | 12 semanas | 26/04 | 09/05 | não |
| Aberto, 20% menos contas, 12 semanas | 7.224 | 2,2 pontos | 72% | 15 semanas | 26/04 | 09/05 | não |

Para ver 2 pontos, o teste precisa de 8.676 contas por grupo, 17.352 no total. As 9.000 contas não chegam lá em nenhum prazo.

## O calendário

- O teste roda semanas inteiras, de segunda a domingo. No histórico de 2025, a segunda tem 317 contas no gatilho por dia e 29,3% de compra; o sábado, 212 e 36,2%.
- Carnaval em 16 e 17/02: a loja abre só de manhã e o "Retire hoje" fica desligado nos dois dias. Num teste de 4 semanas, é um quarto do teste.
- O teste aberto de 12 semanas passa por Carnaval, Paixão de Cristo (03/04), Páscoa, o ponto facultativo de 20/04, Tiradentes e 1º de maio. O Dia das Mães, 10/05, fica fora da janela de compra.

## As opções

1. **Abrir o teste e rodar 12 semanas, de 02/02 a 26/04.** Toda conta que chega ao gatilho entra no sorteio nessa hora, pelo id e pelo nome `retire-hoje`; as 9.000 ficam no grupo em que estão, e as outras regras de quem entra continuam. Vê 2 pontos com 82% de chance. Dados completos em 09/05; decisão na segunda, 11/05. Custo: renovar a temporária de 16/03 a 11/05. Risco: com 20% menos contas por semana, vê 2,2 pontos, e a conta pede 15 semanas.
2. **Rodar até 01/03 e decidir em 16/03.** Aberto, vê a partir de 3,4 pontos; só com as 9.000, a partir de 5,2. Serve se um efeito grande mudaria a decisão. Se o intervalo pegar o zero, isso não quer dizer que o "Retire hoje" não paga, e a gerente decide sem o teste.
3. **Não testar agora** e decidir pela conta da gerente.

Recomendo a opção 1, com a regra nova de entrada escrita hoje, antes de ligar, e testada no A/A antes de comparar os grupos. A escolha é da gerente.

## O que não muda depois do início

- A regra de quem entra e o número de semanas.
- O resultado é olhado uma vez, no fim, com os dados completos. Sem parar no dia em que der significativo.
- Se o tráfego vier menor que o previsto, o teste não ganha semanas depois do início sem uma regra escrita antes.
