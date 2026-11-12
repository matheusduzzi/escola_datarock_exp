# Briefing: o piloto da faixa D chega ao comitê de crédito

Comitê de crédito da Ponte Crédito, segunda, 07/07/2031. Quem decide é a Marta, diretora de crédito. A Helena, gerente de risco, leva o resultado. Nenhum número aqui é de um cliente real.

## O que a proposta aprovada em 04/02/2030 dizia

| Linha | O que ficou combinado |
|---|---|
| Pergunta | Aprovar a faixa D com R$ 1.000 em 6 parcelas, a 6,5% ao mês, para quem passa nos critérios, dá resultado positivo? |
| Sorteio | Por cliente; 60% dos elegíveis vão para a regra nova, 40% recebem a recusa de hoje |
| Teto | R$ 40 mil de perda no pior caso (35% de maus, LGD de 70%): 163 contratos, R$ 163 mil |
| Mau | Alguma parcela com 90 dias de atraso, até 9 meses depois do Pix |
| Empate | 20% de maus: margem de R$ 140 por contrato, antes da perda, ÷ R$ 700 de perda por mau (70% × R$ 1.000) |
| Regra de decisão | Intervalo de Wilson de 95% da taxa de maus, com as seis safras maduras. Inteiro abaixo do empate: vira política. Inteiro acima: para. Cruzando: reformula |
| Se a margem mudar | O empate muda junto, e a regra usa o empate novo. Vale a margem que a controladoria mandar por escrito antes da data da leitura |
| Regras de parada | Teto automático; 1ª parcela atrasada 30 dias acima de 12%, a partir de 40 contratos; contrato fora dos critérios |
| Data da leitura | Safra de agosto madura em 07/06/2031; comitê de 07/07/2031 |

## O que o piloto juntou

| Item | Número |
|---|---|
| Pix | De 01/03/2030 a 31/08/2030 |
| Elegíveis sorteados para a regra nova | 211 |
| Contratos assinados | 149 (R$ 149 mil). O teto não foi atingido |
| Maus nas seis safras maduras | 19 |
| Por canal | App: 5 maus em 64 contratos. Lojas parceiras: 14 maus em 85 |
| 1ª parcela atrasada 30 dias | 6 de 149 (4,0%), abaixo da linha de 12%. A regra nunca parou o piloto |
| Contratos fora dos critérios | Nenhum |

## Mensagens que chegaram antes do comitê

**Lúcia, controladoria, segunda, 02/06/2031, por e-mail à Helena e à Marta:**

> O custo do fundo subiu em abril. A margem do produto da faixa D, antes da perda, caiu de R$ 140 para R$ 112 por contrato. A LGD continua em 70%. Se a taxa subir para 7,5% ao mês, a margem volta a R$ 140.

**Tiago, comercial, quarta, 02/07/2031, no grupo:**

> No app deu 7,8% de maus. Libera a faixa D no app já e deixa as lojas para depois.

**Helena, quinta, 03/07/2031:**

> Seja qual for a leitura, quero sair do comitê com o próximo passo e o nome de quem cuida. Se houver crédito novo para a faixa D, a Marta aceita no máximo R$ 30 mil de perda no pior caso.

## O que você tem para as contas

O `comite.py` dessa pasta tem `wilson`, `empate` e `leitura_credito`. No Python aberto nessa pasta:

```python
from comite import *
```
