# 09. Parada e observações repetidas

Os arquivos da aula «Parada e observações repetidas» do curso Experimentação e teste A/B.

## O que tem nessa pasta

| Arquivo | Para quê |
|---|---|
| `dados/parcelamento_diario.csv` | O teste do parcelamento em 6 vezes, do dia 1 ao dia 21. É o teste da aula |
| `dados/guia_tamanhos_diario.csv` | O teste do guia de tamanhos, do dia 1 ao dia 21 de um plano de 28 dias. É o teste do exercício |
| `parada.py` | As contas: ler um teste (`ler_diario`), somar os dias (`acumulado`), o teste de duas proporções (`teste_proporcoes`), a chance de alarme falso e o poder com várias olhadas (`alarme_falso`), as linhas de cada olhada (`linhas_parada`) e as simulações (`simular_aa`, `simular_teste`) |
| `regra-de-parada.md` | A folha do exercício, com as dez linhas da regra e a tabela das olhadas. Salve uma cópia com o seu nome |

Os dois CSVs têm uma linha por dia, com as colunas:

| Coluna | O que é |
|---|---|
| `dia` | o dia do teste, de 1 em 1 |
| `visitas_A`, `visitas_B` | as visitas sorteadas para cada grupo naquele dia |
| `compras_A`, `compras_B` | as visitas de cada grupo que compraram naquele dia |

## Como rodar

Abra o Python dentro dessa pasta:

```bash
python3
```

Cole os blocos da aula na ordem, a partir da seção 3. Os blocos usam as variáveis dos blocos de antes, então pule só o que você já rodou.

Leia os testes sempre com o `ler_diario` do `parada.py`. Ele avisa se faltar coluna, se um dia estiver fora de ordem ou se algum dia tiver mais compras que visitas.

O `parada.py` usa a biblioteca padrão do Python, o NumPy e o pandas. Não precisa do SciPy. O `alarme_falso` faz a conta numa grade fina, sem sortear nada. O `linhas_parada` procura a linha que deixa o alarme falso total na fração que você pedir. As duas levam alguns segundos com 21 ou 28 olhadas. As simulações sorteiam testes, então outro `rng` dá números um pouco diferentes. Se aparecer `No module named 'pandas'`, volte ao README do kit e instale pelo `requirements.txt`. No Windows, troque `python3` por `py`.

As olhadas entram como os dias em que você olha, em ordem e sem repetir, por exemplo `[7, 14, 21]`. A conta supõe visitas parecidas em cada dia. As linhas entram como z: um número só para todas as olhadas ou uma lista com um por olhada. A linha de 0,05 dos dois lados é `1.96`. O alfa entra como fração: 5% é `0.05`.

Se uma função recusar a entrada, leia a mensagem.

Se precisar de ajuda, deixe um comentário na aula. Conte o objetivo, o comando que você rodou, a saída que apareceu e o que já tentou, sem dados pessoais.
