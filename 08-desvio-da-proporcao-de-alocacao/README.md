# 08. Desvio da proporção de alocação

Os arquivos da aula «Desvio da proporção de alocação» do curso Experimentação e teste A/B.

## O que tem nessa pasta

| Arquivo | Para quê |
|---|---|
| `dados/teste_selo.csv` | O teste do selo de troca grátis, de 6 a 19 de abril. É o primeiro teste da aula |
| `dados/teste_pagamento.csv` | O teste da página de pagamento nova, de 20 de abril a 3 de maio. É o segundo teste da aula |
| `dados/teste_video.csv` | O teste do vídeo do produto, de 4 a 17 de maio. É o teste do exercício |
| `srm.py` | As contas: ler um teste, o qui-quadrado da divisão (`teste_srm`), a divisão por dia ou navegador (`divisao_por`) e a conversão com intervalo (`conversao`) |
| `roteiro-srm.md` | A folha do exercício, com as sete perguntas do roteiro. Salve uma cópia com o seu nome |

Os três CSVs têm uma linha por visita sorteada, com 29.400 visitas cada um (14 dias, 2.100 por dia). As colunas:

| Coluna | De onde vem | O que é |
|---|---|---|
| `id_visita` | serviço de sorteio | o código da visita |
| `dia` | serviço de sorteio | o dia da visita |
| `navegador` | serviço de sorteio | Chrome, Safari, Edge, Firefox ou o app da loja |
| `grupo` | serviço de sorteio | `A` ou `B`, o grupo em que a visita caiu |
| `exposicao` | navegador | 1 se o evento de exposição chegou ao registro; é o que o painel do teste conta |
| `comprou` | sistema de pedidos | 1 se a visita fez um pedido |

Os três testes têm a divisão do painel torta, cada um por um motivo. Achar qual é o trabalho da aula e do exercício.

## Como rodar

A aula usa também o teste do botão da loja, o `ab_botao.csv`, que fica na pasta `dados/loja` da raiz do kit, uma pasta acima dessa. Abra o Python dentro dessa pasta:

```bash
python3
```

Cole os blocos da aula na ordem, a partir da seção 3. Os blocos usam as variáveis dos blocos de antes, então pule só o que você já rodou.

Leia os testes sempre com o `ler_visitas` do `srm.py`. Ele lê os ids como texto e avisa se faltar alguma coluna.

O `srm.py` faz as contas com a biblioteca padrão do Python e usa o pandas para ler e agrupar. Não precisa do SciPy. Se você já usa o SciPy, o `teste_srm(contagens, proporcoes)` dá o mesmo resultado de `scipy.stats.chisquare(contagens, f_exp=...)`, com `f_exp` igual ao total vezes cada proporção. Se aparecer `No module named 'pandas'`, volte ao README do kit e instale pelo `requirements.txt`. No Windows, troque `python3` por `py`.

Se uma função recusar a entrada, leia a mensagem. As contagens entram como números inteiros e as proporções como fração que soma 1 (meio a meio é `[0.5, 0.5]`, 90% e 10% é `[0.9, 0.1]`). Sem a proporção, o `teste_srm` compara com partes iguais.

Se precisar de ajuda, deixe um comentário na aula. Conte o objetivo, o comando que você rodou, a saída que apareceu e o que já tentou, sem dados pessoais.
