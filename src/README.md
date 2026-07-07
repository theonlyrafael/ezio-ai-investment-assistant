# Passo a Passo de Execução

## Setup da OpenAI

Para a inteligência do agente (Ezio), optei por utilizar a API oficial da OpenAI em vez de um modelo local (Ollama). Isso garante maior agilidade e consistência nas respostas.

1. Crie ou acesse sua conta em [platform.openai.com](https://platform.openai.com/).
2. Gere uma nova **API Key**.
3. Na raiz do repositório, crie um arquivo chamado `.env` e insira a sua chave no seguinte formato:
   ```text
   OPENAI_API_KEY=sua-chave-aqui
   ```
*(Nota de segurança: o arquivo `.env` deve estar mapeado no seu `.gitignore` para não vazar publicamente).*

## Estrutura do Código

Para seguir as melhores práticas de Engenharia de Software (Separação de Responsabilidades), o código não é monolítico. Ele foi modularizado e todo o código-fonte está dentro da pasta `src/`:

* `src/app.py`: Interface gráfica (Front-end) desenvolvida com Streamlit.
* `src/agente.py`: O "cérebro" do projeto (Back-end), responsável por processar os CSVs/JSONs e orquestrar as chamadas para a OpenAI.
* `src/config.py`: Módulo responsável pelo carregamento seguro das variáveis de ambiente.
* `src/requirements.txt`: Lista exata das bibliotecas necessárias para o projeto funcionar.

## Como Rodar

Abra o seu terminal na raiz do projeto e execute os comandos abaixo:

```bash
# 1. Instalar todas as dependências do projeto
pip install -r src/requirements.txt

# 2. Iniciar o servidor da interface do agente
streamlit run src/app.py
```

## Evidência de Execução

<img width="1920" height="1107" alt="Interface do Ezio rodando com sucesso" src="https://github.com/user-attachments/assets/b5af743b-f940-46a8-97eb-87dcdf89d499" />
