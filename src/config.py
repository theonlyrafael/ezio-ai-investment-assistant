import os
from dotenv import load_dotenv

# carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# resgata a chave da API
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# aviso caso a chave da API não esteja definida
if not OPENAI_API_KEY:
    raise ValueError("A chave da API do OpenAI não está definida. Por favor, verifique se a variável de ambiente OPENAI_API_KEY existe no arquivo .env.")