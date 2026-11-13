# Tarefa 2 do diagnóstico: visitas do teste do cupom por grupo.
# Rode de dentro da pasta 00-apresentacao:  python3 tarefa2.py
import pandas as pd

visitas = pd.read_csv("dados/visitas_cupom.csv")
print(visitas.head())

# Monte aqui a tabela com uma linha por grupo e as colunas
# grupo, visitas, compras e taxa_pct, sem as visitas que ficaram sem grupo.
# Guarde a tabela final na variável resultado e mostre com print(resultado).
# Mostre também quantas visitas ficaram sem grupo.
