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

# 3. Inicialização do Session State para armazenar o histórico de conversas
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": "Olá! Eu sou o Ezio, o melhor assessor de investimentos que você poderia ter. Como posso ajudá-lo hoje?",
        }
    )

# 4. Renderização do histórico de mensagens na tela
for message in st.session_state.messages:
    # aqui defini um avatar diferente para o usuário e para o assistente
    avatar_icon = "👤" if message["role"] == "user" else "🏦"
    with st.chat_message(message["role"], avatar=avatar_icon):
        st.markdown(message["content"])

# 5. Captura da entrada do usuário e processamento da resposta
if prompt := st.chat_input("Digite sua dúvida financeira aqui..."):



        
        
