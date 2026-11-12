# 07. Instrumentar e testar A/A

Os arquivos da aula «Instrumentar e testar A/A» do curso Experimentação e teste A/B.

## O que tem nessa pasta

| Arquivo | Para quê |
|---|---|
| `dados/eventos_semana1.csv` | Os eventos da primeira semana de A/A do checkout, de 2 a 8 de março. É a semana da aula |
| `dados/eventos_semana2.csv` | Os eventos da segunda semana, de 9 a 15 de março. É a semana do exercício |
| `aa.py` | As contas: ler os eventos, o p da divisão, a conversão de A contra B, o sorteio pelo id e a simulação de muitos A/A |
| `checagens.py` | As quatro checagens da aula juntas (`checar`), a tabela de visitas, uma semana sem falha (`semana_sintetica`) e o `plantar`, que planta falhas que você escolhe |
| `folha-aa.md` | A folha do exercício. Salve uma cópia com o seu nome |

Os dois CSVs têm uma linha por evento, com as colunas `momento`, `id_evento`, `id_visita`, `id_sessao`, `evento` (`exposicao` ou `compra`) e `grupo` (só na exposição). As duas semanas têm falhas de registro escondidas de propósito. Achar quais é o trabalho da aula e do exercício.

## Como rodar

Abra o Python dentro dessa pasta:

```bash
python3
```

Cole os blocos da aula na ordem, a partir da seção 3. Os blocos usam as variáveis dos blocos de antes, então pule só o que você já rodou. A simulação da seção 6 leva poucos segundos.

Os sorteios saem iguais toda vez que você roda o bloco inteiro, desde a linha do `np.random.default_rng`. Se você rodar só uma parte, o sorteio continua de onde parou e os números mudam um pouco.

Leia os eventos sempre com o `ler_eventos` do `aa.py`. Ele lê os ids como texto. Com o `pd.read_csv` sem mais nada, um id como `00012345` vira o número 12345 e deixa de bater com o mesmo id em outra linha.

O `aa.py` e o `checagens.py` usam o pandas, e a simulação, o NumPy, que vem com ele. Se aparecer `No module named 'pandas'`, volte ao README do kit e instale pelo `requirements.txt`. No Windows, troque `python3` por `py`.

Se uma função recusar a entrada, leia a mensagem. As taxas entram como fração (10% é `0.10`), e as contagens de visitas e compras, como números inteiros. O `comparar_conversao` recusa mais compras que visitas: quase sempre é uma compra contada duas vezes.

Se precisar de ajuda, deixe um comentário na aula. Conte o objetivo, o comando que você rodou, a saída que apareceu e o que já tentou, sem dados pessoais.
