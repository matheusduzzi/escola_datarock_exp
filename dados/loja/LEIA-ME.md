# Testes A/B da Loja Exemplo

Dois testes do checkout da Loja Exemplo. Os números são inventados e saem do `gerar.py` desta pasta.

| Arquivo | Linhas | Colunas | O que testou |
|---|---|---|---|
| `ab_botao.csv` | 12.000 visitas | `id_visita`, `grupo` (`A` ou `B`), `converteu` (1 se comprou) | o botão de compra antigo (A) contra um botão verde maior (B) |
| `ab_frete.csv` | 12.000 visitas | as mesmas | a página sem o valor do frete no topo (A) contra a página com o frete no topo (B) |

Uma linha é uma visita. Em cada arquivo, algumas visitas ficaram com o grupo vazio. As aulas dizem quantas e o que fazer com elas.

## Como os dados nascem

O começo do `gerar.py` conta o mecanismo: quantas visitas cada grupo recebe, a taxa de compra de cada grupo e o que se perde no registro. Faça as contas das aulas antes de abrir o gerador. Depois abra e compare o que você estimou com o que foi sorteado. Numa loja de verdade ninguém conhece a taxa sorteada; é por isso que o curso mede a incerteza.

O gerador também diz o que ele supõe e uma loja de verdade não garante: uma visita por pessoa, visitas independentes, taxa que não muda durante o teste e ninguém trocando de grupo. Várias aulas do curso tratam justamente do que acontece quando uma dessas coisas falha.

## Gerar de novo

```bash
python3 gerar.py
```

A saída é `ab_botao=12000 ab_frete=12000 visitas_sem_grupo_por_teste=7`. O gerador só usa a biblioteca padrão do Python e sai igual toda vez. Não edite os CSVs à mão: aula que precisar de outro caso cria os próprios arquivos na pasta dela.
