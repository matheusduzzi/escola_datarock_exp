# Plano do teste: calculadora de frete na página do produto

Escrito pela Lia na quinta, 11/06, antes do início do teste.

## A pergunta

A calculadora de frete na página do produto (B) aumenta a compra na visita, comparada com a página de hoje, que só mostra o frete no carrinho (A)?

## Quem entra e como o sorteio divide

Toda visita a uma página de produto, no site. O sorteio é por visita.

| Semana | Datas | Parte no B | Por quê |
|---|---|---|---|
| 1 | 15/06 a 21/06 | 10% | A calculadora chama o serviço das transportadoras, e ninguém sabe se ele aguenta muita gente |
| 2 | 22/06 a 28/06 | 50% | O serviço aguentou a semana 1 |

A semana 2 é a do aniversário da loja, com desconto em todo o site. Ela costuma vender bem mais que uma semana comum.

## A métrica que decide

Compra na visita: a coluna `comprou` do arquivo de visitas.

## A regra

Lança o B se o efeito na compra tiver o intervalo de 95% acima de zero. Manter a calculadora custa uma mensalidade ao serviço das transportadoras.

## Cortes previstos

| Corte | Por quê | O que entra no relatório |
|---|---|---|
| Semana | A parte no B muda de uma semana para a outra | O efeito em cada semana |
| Cliente novo e recorrente | Quem nunca comprou não sabe quanto custa o frete da loja, e a calculadora responde isso antes do carrinho | O efeito em cada um e a diferença entre os dois. Uma diferença com p até 0,05 vira um teste só com clientes novos. O corte não muda a regra |

Qualquer outro corte fica fora do plano.
