# Plano do teste da página do produto

Escrito pela Lia na quinta, 26/02/2026, antes do início. Mandado ao grupo do time no mesmo dia.

## O que muda

| Versão | Página do produto |
|---|---|
| A | A página de hoje |
| B | Fotos grandes, que abrem em tela cheia |
| C | As avaliações dos clientes no topo, antes da descrição |

## Quem entra e como sorteia

Toda conta que abre uma página de produto entre a segunda, 02/03, e o domingo, 15/03. Cada conta é sorteada uma vez para A, B ou C, com a mesma chance, e fica na mesma versão o teste todo.

## As métricas

Todas contadas por conta: contas que fizeram a coisa sobre contas sorteadas para a versão.

| Métrica | O que conta | Papel |
|---|---|---|
| `comprou_7d` | Comprou em até 7 dias da primeira visita à página | Decide |
| `devolveu_30d` | Devolveu um pedido em até 30 dias | Proteção |
| `chamou_atendimento_7d` | Abriu chamado no atendimento em até 7 dias | Proteção |
| `pos_no_carrinho` | Pôs algum produto no carrinho | Acompanha |
| `abriu_fotos` | Abriu pelo menos uma foto | Acompanha |
| `leu_avaliacoes` | Rolou a página até as avaliações | Acompanha |
| `voltou_7d` | Voltou ao site em até 7 dias | Acompanha |
| `favoritou` | Salvou um produto nos favoritos | Acompanha |

## Regra

- As duas versões custam o mesmo para manter. Qualquer ganho na compra paga a troca.
- Lança a versão que ganhar na compra em 7 dias, se nenhuma proteção piorar.
- As métricas que acompanham vão no relatório. Elas não decidem.

## Antes do efeito

A divisão entre as três versões é checada antes de olhar qualquer métrica, como na aula «Desvio da proporção de alocação».
