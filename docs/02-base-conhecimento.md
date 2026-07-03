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

[Sua descrição aqui]

---

## Exemplo de Contexto Montado

> Mostre um exemplo de como os dados são formatados para o agente.

```
Dados do Cliente:
- Nome: João Silva
- Perfil: Moderado
- Saldo disponível: R$ 5.000

Últimas transações:
- 01/11: Supermercado - R$ 450
- 03/11: Streaming - R$ 55
...
```
