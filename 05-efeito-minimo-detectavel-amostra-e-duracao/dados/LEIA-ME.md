# Dados da aula «Efeito mínimo detectável, amostra e duração»

O histórico de 2025 do gatilho do "Retire hoje" no site da Loja Exemplo, um dia por linha: de segunda, 06/01/2025, a domingo, 04/01/2026, 52 semanas inteiras.

| Arquivo | Uma linha é | Colunas |
|---|---|---|
| `gatilho_por_dia_2025.csv` | um dia | `data`, `contas_no_gatilho` (contas que chegaram, nesse dia, à escolha da entrega com um produto em estoque na loja física), `compraram_7d` (dessas contas, quantas fizeram um pedido do dia até 6 dias depois), `evento` (o nome do feriado ou da data do comércio, vazio nos dias comuns) |

É o site todo, e não só as 9.000 contas do teste. A mesma conta pode aparecer em dias diferentes. Por isso a soma de uma semana é maior que o número de contas diferentes que chegam ao gatilho na semana.

A coluna `evento` só diz o que o calendário marca naquele dia. A temporada de Natal, de 08/12 a 23/12, aparece com o nome `Natal (temporada)`. O `semanas.py` chama de comum a semana, de segunda a domingo, sem nenhum dia com evento.

Os dados de janeiro de 2026, das 9.000 contas, estão na pasta da aula «Métricas de sucesso e proteção», ao lado desta. O `variacao.py` lê de lá.

Datas no formato ano-mês-dia.

## Os outros arquivos da pasta

| Arquivo | O que tem |
|---|---|
| `cenarios-retire.csv` | Os seis cenários do "Retire hoje" que a aula roda |
| `cenarios-caio.csv` | O cenário do Caio, do passo 4 da prática guiada |
| `cenarios-frete.csv` | Só o cabeçalho: os cenários do exercício entram aqui |
| `calendario-2026.csv` | Feriados nacionais e pontos facultativos de 2026, pela Portaria MGI nº 11.460/2025, mais o domingo de Páscoa e o Dia das Mães |
| `cenarios-retire.md` | A nota de cenários que foi para a Lia, preenchida |
| `modelo-cenarios.md` | A mesma nota em branco, para o exercício |
| `pedido-frete.md` | O pedido do exercício |

## Gerar de novo

```bash
python3 gerar_historico.py
```

A saída é `dias=364 contas=99800 compraram=32006`. O gerador só usa a biblioteca padrão e sai igual toda vez. O começo dele conta como os dados nascem: abra depois de fazer as contas da aula.
