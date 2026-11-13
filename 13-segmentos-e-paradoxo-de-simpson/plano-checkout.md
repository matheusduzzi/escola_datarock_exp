# Plano do teste: checkout em uma página

Escrito pela Lia na quinta, 14/05, antes do início do teste.

## A pergunta

O checkout em uma página (B) aumenta a compra na visita, comparado com o checkout de hoje, em três telas (A)?

## Quem entra e como o sorteio divide

Toda visita à loja, no site e no app. O sorteio é por visita.

| Canal | Parte no B | Por quê |
|---|---|---|
| Site | 50% | Se o B der problema, a gente desliga na hora |
| App | 20% | Uma versão ruim do app leva dias para ser trocada, porque depende da loja de aplicativos |

A divisão fica fixa do primeiro ao último dia.

## Período

De segunda, 18/05, a domingo, 07/06. Três semanas.

## A métrica que decide

Compra na visita: a coluna `comprou` do arquivo de visitas.

## A regra

Lança o B se o efeito na compra tiver o intervalo de 95% acima de zero. O checkout novo já está pronto, e o custo de ligar é pequeno.

## Cortes previstos

| Corte | Por quê | O que entra no relatório |
|---|---|---|
| Canal (site e app) | A divisão é diferente em cada canal, e o app compra muito mais que o site | O efeito em cada canal |
| Cliente novo e recorrente | Quem não tem cartão salvo pode ganhar mais com uma tela só | O efeito em cada um e a diferença entre os dois. Uma diferença com p até 0,05 vira um teste próprio. O corte não muda a regra |

Qualquer outro corte fica fora do plano.
