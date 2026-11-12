"""O plano do teste do "Retire hoje": a lista, o nome do teste e quem pode entrar.

Tudo aqui foi escrito antes do sorteio e só usa colunas do cadastro tirado em 01/02/2026,
véspera do início. Para outro teste, copie este arquivo com outro nome e mude as quatro partes.
"""
from grupos import Regra

CLIENTES = "dados/clientes_retire.csv"
NOME_TESTE = "retire-hoje"
INICIO = "2026-02-02"


def conta_ativa(status):
    return status == "ativa"


def e_cliente(tipo):
    return tipo == "cliente"


def entrou_no_mes_anterior(ultimo_acesso):
    return "2026-01-03" <= ultimo_acesso <= "2026-02-01"


REGRAS = [
    Regra("encerrada", "status", "Conta encerrada ou bloqueada não consegue comprar durante o teste.",
          conta_ativa),
    Regra("interna", "tipo", "Conta de funcionário ou de teste do time não é cliente da loja.",
          e_cliente),
    Regra("sem-acesso", "ultimo_acesso",
          "Não entrou no site nos 30 dias antes do início; o plano é para quem entrou no mês anterior.",
          entrou_no_mes_anterior),
]

# Colunas de antes do início, para ver se os grupos ficaram parecidos.
EQUILIBRIO = ["pedidos_90d", "mora_perto", "usou_retirada"]
