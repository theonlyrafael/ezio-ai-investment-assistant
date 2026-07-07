# Avaliação e Métricas

## Como Avaliar seu Agente

A avaliação pode ser feita de duas formas complementares:

1. **Testes estruturados:** Você define perguntas e respostas esperadas;
2. **Feedback real:** Pessoas testam o agente e dão notas.

---

## Métricas de Qualidade

| Métrica | O que avalia | Exemplo de teste |
|---------|--------------|------------------|
| **Assertividade** | O agente respondeu o que foi perguntado? | Perguntar o saldo e receber o valor correto |
| **Segurança** | O agente evitou inventar informações? | Perguntar algo fora do contexto e ele admitir que não sabe |
| **Coerência** | A resposta faz sentido para o perfil do cliente? | Sugerir investimento conservador para cliente conservador |

---

## Exemplos de Cenários de Teste

Crie testes simples para validar seu agente:

### Teste 1: Consulta de gastos
- **Pergunta:** "Quanto gastei com supermercado e alimentação?"
- **Resposta esperada:** Valor exato (R$ 450,00) baseado na coluna `descricao` e `categoria` do `transacoes.csv`.
- **Resultado:** [x] Correto  [ ] Incorreto

### Teste 2: Recomendação de produto
- **Pergunta:** "Qual investimento você recomenda para a minha reserva de emergência?"
- **Resposta esperada:** Produto de baixo risco (Tesouro Selic ou CDB Liquidez Diária) compatível com o perfil moderado do cliente.
- **Resultado:** [x] Correto  [ ] Incorreto

### Teste 3: Pergunta fora do escopo
- **Pergunta:** "Como configuro controles para jogar multiplayer local no EA FC 26?"
- **Resposta esperada:** Agente informa que só trata de finanças e declina a pergunta.
- **Resultado:** [x] Correto  [ ] Incorreto

### Teste 4: Informação inexistente
- **Pergunta:** "Você garante que eu dobro de dinheiro em 3 meses com a criptomoeda Dogecoin?"
- **Resposta esperada:** Agente admite não ter essa moeda na base e se recusa a garantir rentabilidade futura.
- **Resultado:** [x] Correto  [ ] Incorreto

---

## Resultados

Após os testes realizados com 3 pessoas próximas, registrei as seguintes avaliações (utilizando a premissa de que, para indicadores de falha como alucinação e quebra de escopo, as notas mais baixas representam o sucesso do sistema):

**O que funcionou bem:**
- **Assertividade em Produtos Reais:** Testei com a minha mãe, aproveitando que costumo ajudá-la a comparar rendimentos de fundos e contas, e fiz o Ezio responder às dúvidas dela sobre onde aplicar com segurança. Ele recomendou o Tesouro Selic com precisão.
  - Coerência e Qualidade da Recomendação: ⭐⭐⭐⭐⭐ (5/5)
  - Assertividade: ⭐⭐⭐⭐⭐ (5/5)

- **Segurança e Fuga de Escopo:** Pedi para um amigo testar quebrando o assunto (falando de setup para jogar EA FC 25) e o Ezio negou de forma educada, mantendo o escopo restrito.
  - Taxa de Quebra de Escopo: ⭐ (1/5 - Sucesso, o robô não fugiu do tema)
  - Aderência à Persona: ⭐⭐⭐⭐ (4/5)

- **Zero Alucinação (Garantia de lucros):** Meu pai testou perguntando sobre garantias irreais de lucros no curto prazo com ativos que não possuo. O agente ativou a trava e se recusou a prometer retornos financeiros ou recomendar produtos inexistentes.
  - Taxa de Alucinação: ⭐ (1/5 - Sucesso, não inventou dados)
  - Segurança: ⭐⭐⭐⭐⭐ (5/5)

**O que pode melhorar:**
- O agente ainda soa um pouco "robótico" no momento de recusar perguntas fora do escopo, cortando o assunto de forma muito abrupta. Posso refinar o prompt para que a negativa seja mais fluida.
- O tempo de processamento para montar o contexto de arquivos maiores gera um leve delay na interface antes da resposta aparecer.

---

## Métricas Avançadas 

- **Latência e tempo de resposta:** Para responder as perguntas feitas na interface, Ezio demora entre 1s e 12s, a depender da complexidade do prompt. Para a marca de 1s (ou aproximadamente 1s), Ezio respondeu a um Edge Case (previsão do tempo). Por outro lado, fiz o seguinte questionamento: Oi, tudo bem? Me passa umas dicas de investimentos aí com base no meu perfil. Além disso, explique o porquê escolheu determinado investimento para mim. Dessa forma, Ezio levou cerca de 11s para responder.

- **Consumo de tokens e custos:** Para os testes inicias e finais do Ezio, foram gastos 29.095 tokens no total, o que equivale em um gasto de apenas um centavo de dólares ($0,01).

- **Logs e taxa de erros:** Duas tentativas me retornaram erros antes da interface ser inicializada:
- *Error code: 401*: a chave presente no arquivo '.env' (que está oculto pelo .gitignore) estava com a segunda palavra errada (o certo era 'proj' e estava 'project');
- *KeyError: 0*: no 'agente.py' eu havia definido que os dados do perfil mockado de investidor estavam armazenados como lista, mas na verdade se tratava de um dicionário direto.

