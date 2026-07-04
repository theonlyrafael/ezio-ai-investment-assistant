# Base de Conhecimento

## Dados Utilizados

| Arquivo | Formato | Utilização no Agente |
|---------|---------|---------------------|
| `historico_atendimento.csv` | CSV | Contextualizar interações anteriores e manter a fluidez da conversa |
| `perfil_investidor.json` | JSON | Personalizar recomendações de acordo com o apetite de risco |
| `produtos_financeiros.json` | JSON | Sugerir produtos adequados ao perfil mapeado do usuário |
| `transacoes.csv` | CSV | Analisar o padrão de fluxo de caixa e capacidade de aporte do cliente |

---

## Adaptações nos Dados

> Você modificou ou expandiu os dados mockados? Descreva aqui.

Optei por não utilizar datasets genéricos do Hugging Face para manter o controle da persona e focar exclusivamente na realidade do mercado brasileiro. Em vez disso, expandi os dados mockados utilizando scripts em Python (com bibliotecas como `Faker` e `Pandas`) para gerar um volume robusto de registros sintéticos. O catálogo de `produtos_financeiros.json` foi enriquecido com ativos reais e práticos, como variações de títulos do Tesouro Direto, contas com rendimento diário atrelado ao CDI, CDBs e algumas opções de renda variável. O `perfil_investidor.json` e os históricos de transações foram escalados para simular múltiplos cenários de clientes com diferentes capacidades de aporte.

---

## Estratégia de Integração

### Como os dados são carregados?
> Descreva como seu agente acessa a base de conhecimento.

Os arquivos JSON e CSV são carregados na memória pelo back-end em Python (utilizando `Pandas` e a biblioteca nativa `json`) logo na inicialização da aplicação no Streamlit, funcionando como um banco de dados em memória local e rápido para a sessão.

### Como os dados são usados no prompt?
> Os dados vão no system prompt? São consultados dinamicamente?

Os dados são consultados dinamicamente para evitar o desperdício de tokens e respeitar a janela de contexto. Quando o usuário faz uma pergunta, o back-end filtra as tabelas e arquivos locais, extrai apenas as linhas pertinentes ao cenário e injeta esse bloco como uma mensagem de contexto (`system` ou `user`) antes de chamar a API de completude.

Abaixo está o exemplo de código que ilustra essa abordagem de integração:

```python
import json
import pandas as pd
from openai import OpenAI

def gerar_resposta_ezio(id_cliente, pergunta_usuario):
    # 1. Carrega os dados locais da base de conhecimento
    with open('data/perfil_investidor.json', 'r') as f:
        perfis = json.load(f)
    with open('data/produtos_financeiros.json', 'r') as f:
        produtos = json.load(f)
        
    # Encontra o perfil do cliente específico
    perfil_cliente = next(p for p in perfis if p["id"] == id_cliente)
    
    # 2. Aplica a regra de negócio: Filtra produtos adequados ao perfil
    risco_permitido = perfil_cliente["perfil_risco"] # Ex: "Moderado"
    produtos_recomendados = [
        p for p in produtos 
        if p["nivel_risco"] == risco_permitido or p["nivel_risco"] == "Baixo"
    ]
    
    # 3. Monta dinamicamente a string de contexto
    contexto_prompt = f"""
    CONTEXTO DO CLIENTE:
    - Nome: {perfil_cliente['nome']}
    - Perfil de Risco: {risco_permitido}
    
    PRODUTOS DISPONÍVEIS PARA RECOMENDAÇÃO:
    {json.dumps(produtos_recomendados, indent=2, ensure_ascii=False)}
    """
    
    # 4. Envia o contexto estruturado para a API da OpenAI
    client = OpenAI(api_key="SUA_API_KEY")
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system", 
                "content": "Você é o Ezio, um assistente virtual de investimentos educativo e consultivo. Responda à dúvida do usuário baseando-se estritamente no contexto fornecido. Se a resposta não puder ser derivada do contexto ou se o cliente não tiver perfil mapeado, informe que não possui os dados e decline educadamente de alucinar."
            },
            {
                "role": "user", 
                "content": f"{contexto_prompt}\n\nPergunta do usuário: {pergunta_usuario}"
            }
        ]
    )
    
    return response.choices[0].message.content
```

---

## Exemplo de Contexto Montado

> Mostre um exemplo de como os dados são formatados para o agente.

```
Dados do Cliente:
- Nome: Donatello
- Perfil: Moderado
- Saldo disponível para investimento: R$ 6.100,00

Produtos pré-selecionados para o perfil:
- Tesouro IPCA+ 2029 (Renda Fixa, Risco Baixo)
- Conta Digital 100% CDI (Renda Fixa, Risco Baixo, Liquidez Diária)
- Fundo Imobiliário XPML11 (Renda Variável, Risco Moderado)

Últimas transações:
- 01/07: Pagamento Fatura - R$ 1.300,00
- 02/07: Aporte Tesouro Direto - R$ 610,00

Último atendimento:
- 10/06: Cliente perguntou sobre a diferença de rentabilidade entre poupança e CDI.
```
