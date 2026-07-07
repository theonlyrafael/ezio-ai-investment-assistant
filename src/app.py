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

# 5. Barra de entrada de texto para o usuário digitar sua dúvida financeira
# se o usuário digitar algo e confirmar com Enter, o bloco abaixo eh executado
if prompt := st.chat_input("Digite sua dúvida financeira aqui..."):

    # A. Exibe a pergunta do usuário na tela e salva na memória
    st.chat_message("user", avatar="👤").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # B. Mostra um indicador visual de carregamento enquanto o Ezio pensa na resposta
    with st.spinner("Analisando seu perfil e o mercado..."):

        # C. Chama a nossa função do agente.py, passando a pergunta e o histórico
        # feito o filtro das mensagens de boas-vindas do Streamlit para focar só na conversa
        historico_para_api = [
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages[:-1]
        ]
        resposta_ezio = responder_com_ezio(
            pergunta_usuario=prompt, historico_conversa_streamlit=historico_para_api
        )

    # D. Exibe a resposta do Ezio na tela e salva na memória
    with st.chat_message("assistant", avatar="🏦"):
        # substitui "R$" por "R\$" para não bugar o markdown do streamlit
        resposta_formatada = resposta_ezio.replace("R$", "R\\$")
        st.markdown(resposta_formatada)

    st.session_state.messages.append({"role": "assistant", "content": resposta_formatada})
