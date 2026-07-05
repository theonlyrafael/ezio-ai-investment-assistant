import json
import os
import pandas as pd
from openai import OpenAI
from src.config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)


def carregar_base_conhecimento():
    # lê o arquivo JSON com a base de conhecimento
    try:
        with open("data/perfil_investidor.json", "r", encoding="utf-8") as f:
            perfil = json.load(f)
        with open("data/produtos_financeiros.json", "r", encoding="utf-8") as f:
            produtos = json.load(f)

        # carrega os CSVs se eles existirem e não estiverem vazios
        transacoes = (
            pd.read_csv("data/transacoes.csv", encoding="utf-8").to_dict(
                orient="records"
            )
            if os.path.exists("data/transacoes.csv")
            else []
        )
        historico = (
            pd.read_csv("data/historico_atendimento.csv", encoding="utf-8").to_dict(
                orient="records"
            )
            if os.path.exists("data/historico_atendimento.csv")
            else []
        )

        return perfil, produtos, transacoes, historico
    except Exception as e:
        print(f"Erro ao carregar os arquivos de dados: {e}")
        return {}, [], [], []

def montar_contexto_dinamico(perfil, produtos, transacoes, historico):