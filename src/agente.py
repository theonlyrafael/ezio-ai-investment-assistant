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
    # garante que o perfil do cliente eh puxado (tratando se for lista ou dict)
    p = perfil[0] if isinstance(perfil, list) and len(perfil) > 0 else perfil

    contexto = f"""
    === DADOS DO CLIENTE LOGADO ===
    Nome: {p.get('nome', 'Não identificado')}
    Idade: {p.get('idade', 'Não informado')}
    Perfil de Investidor: {p.get('perfil_investidor', 'Não mapeado')}
    Objetivo Principal: {p.get('objetivo_principal', 'Não informado')}
    Patrimônio Total: R$ {p.get('patrimonio_total', 0.0):,.2f}
    Reserva de Emergência Atual: R$ {p.get('reserva_emergencia_atual', 0.0):,.2f}
    
    === PRODUTOS FINANCEIROS DISPONÍVEIS NA BASE ===
    """
    for prod in produtos:
        contexto += f"\n- {prod['nome']} ({prod['categoria'].upper()}): Risco {prod['risco']}. Rentabilidade: {prod['rentabilidade']}. Indicado para: {prod['indicado_para']}."

    if transacoes:
        contexto += "\n\n=== ÚLTIMAS TRANSAÇÕES DO CLIENTE ==="
        for t in transacoes[:5]:  # pega as últimas 5 para não lotar o prompt
            contexto += f"\n- {t.get('data', 'N/A')}: {t.get('tipo', 'N/A')} de R$ {t.get('valor', 0.0):,.2f} em {t.get('ativo', 'N/A')}"

    if historico:
        contexto += "\n\n=== HISTÓRICO DE ATENDIMENTOS ANTERIORES ==="
        for h in historico[:3]:
            contexto += f"\n- {h.get('data', 'N/A')} | Tema: {h.get('tema', 'N/A')} | Resumo: {h.get('resumo', 'N/A')}"

    return contexto

def responder_com_ezio(pergunta_usuario, historico_conversa_streamlit=[]):
    """Orquestra a consulta dos dados e realiza a chamada à API da OpenAI."""
    # 1. Busca os dados reais das planilhas e arquivos locais
    perfil, produtos, transacoes, historico = carregar_base_conhecimento()
    
    # 2. Transforma esses dados no bloco de texto que o Ezio vai ler
    contexto_injetado = montar_contexto_dinamico(perfil, produtos, transacoes, historico)

    # 3. Trazendo o System Prompt consolidado da Etapa 3
    system_prompt = """
    Você é o Ezio, um agente financeiro inteligente e consultivo focado em investimentos e educação financeira.
    Seu objetivo é analisar o contexto do usuário e fornecer recomendações de Renda Fixa e Variável de forma personalizada e didática, sempre explicando o raciocínio por trás da escolha.

    REGRAS:
    1. Sempre baseie suas respostas ESTRITAMENTE nos dados fornecidos na Base de Conhecimento. Não invente produtos.
    2. Nunca invente informações financeiras ou garanta rentabilidade futura.
    3. NUNCA recomende produtos sem antes verificar o Perfil de Investidor (Conservador, Moderado, Arrojado) no contexto. Se não houver, pergunte.
    4. Mantenha um tom informal, acessível e amigável, explicando termos técnicos com analogias.
    5. Você não é contador. Não forneça conselhos sobre Imposto de Renda ou regras tributárias.
    6. Se não souber algo ou se o produto solicitado não estiver na sua Base de Conhecimento, admita claramente que foge do seu escopo e ofereça as alternativas que você possui disponíveis.
    """