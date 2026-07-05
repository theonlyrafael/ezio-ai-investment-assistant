import json
import os
import pandas as pd
from openai import OpenAI
from src.config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)


def carregar_base_conhecimento():
    """Lê os arquivos de dados da pasta data/ de forma segura."""
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
    """Estrutura os dados brutos em um texto limpo para o prompt da IA."""
    # Garante que puxamos o perfil do cliente (tratando se for lista ou dict)
    p = perfil[0] if isinstance(perfil, list) and len(perfil) > 0 else perfil
    
    contexto = f"""
    === DADOS DO CLIENTE LOGADO ===
    Nome: {p.get('nome', 'Não identificado')}
    Idade: {p.get('idade', 'Não informado')}
    Perfil de Investidor: {p.get('perfil_investidor', 'Não mapeado')}
    Objetivo Principal: {p.get('objetivo_principal', 'Não informado')}
    Patrimônio Total: R$ {p.get('patrimonio_total', 0.0):,.2f}
    Reserva de Emergência Atual: R$ {p.get('reserva_emergencia_atual', 0.0):,.2f}