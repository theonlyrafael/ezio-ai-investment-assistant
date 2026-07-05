import streamlit as st
from agente import responder_com_ezio

# 1. Configuração inicial da página: aba do navegador e layout
st.set_page_config(
    page_title="Ezio - Seu Assessor de Investimentos", page_icon="🏦", layout="centered"
)

# 2. Título e cabeçalho da interface
st.title("🏦 Ezio AI")
st.markdown(
    "Seu assessor financeiro inteligente. Pergunte sobre investimentos, rentabilidade ou dicas para sua carteira!"
)
st.divider()
