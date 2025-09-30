# projeto_agente_wpp
Criação de Agentes com CrewAI, LLM, integração com WhatsApp com EvolutionAPI e n8n.

# 🤖 Base para Criação de Agentes Especializados com CrewAI + EvolutionAPI + n8n

> ⚠️ **Atenção:** Todas as informações de `.env` e do `docker-compose.yml` são **apenas para teste** e devem ser **atualizadas** antes de uso em produção.  
> Este projeto serve como **base inicial** para criação de agentes mais especializados e códigos mais estruturados.

---

## 📌 Descrição do Projeto
Este repositório oferece uma arquitetura mínima para:
- Rodar **agentes inteligentes** com [CrewAI]([https://github.com/joaomdmoura/crewAI](https://github.com/crewAIInc/crewAI));
- Utilizar o modelo **Llama 3.1:8B** via [Ollama](https://ollama.ai/);
- Integrar mensagens via **WhatsApp** utilizando [EvolutionAPI](https://github.com/EvolutionAPI);
- Orquestrar fluxos com **n8n** (automação via webhooks e HTTP requests);
- Rodar um **servidor HTTP local** para testes.

---

## ⚙️ Pré-requisitos
Antes de iniciar, certifique-se de ter instalado:

- [Docker & Docker Compose](https://docs.docker.com/get-docker/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (se usar Windows/Mac)
- [Ollama](https://ollama.ai/) rodando localmente
- Git (para clonar este repositório)

---

## 🧩 Configuração do Ambiente

### 1. Rodar o modelo no Ollama
Certifique-se que o modelo **Llama 3.1:8B** já está inicializado:
```bash ollama run llama3.1:8b```

### 2. Configuração da EvolutionAPI

- Atualize os dados do docker-compose.yml da EvolutionAPI.

- Atualize as variáveis do .env da EvolutionAPI.

- Rodar a EvolutionAPI:

- docker compose up -d

- Integração com WhatsApp será feita após a API estar ativa.

### 3. Rodar o Agente CrewAI

- Crie seu agente CrewAI com suporte a WebSocket (porta padrão: 8765).

- Configure o agente para utilizar o modelo llama3.1:8b que já foi inicializado no Ollama.

- Rode o arquivo de conexão do agente para interceptar a rota de mensagens.

### 4. Servidor HTTP para testes

- Suba um servidor HTTP local para receber e enviar mensagens de teste ao agente.
- Este servidor será usado como ponte entre o n8n e o agente.

### 5. Configuração do n8n

- No Docker Desktop, busque a imagem oficial ou rode:

- docker pull docker.n8n.io/n8nio/n8n


- Depois inicie o container configurando o volume:

- Container Path: /home/node/.n8n

- Timezone: GENERIC_TIMEZONE=America/Sao_Paulo

---

## 🔗 Integração com n8n + EvolutionAPI

- Criar um Webhook no n8n

- O webhook receberá as mensagens processadas pelo EvolutionAPI.

- Configurar o servidor HTTP

- O servidor recebe a request, envia ao agente que processa e devolve a resposta.

- Criar um HTTP Request no n8n

- Configure a request para enviar a resposta processada para a EvolutionAPI.

- Ao criar a request, substitua: localhost → host.docker.internal:${port}

- Ativar os Webhooks da EvolutionAPI

- Configure a URL do webhook para apontar ao n8n: http://host.docker.internal:${port}/webhook/...

- Inserir as credenciais do EvolutionAPI no n8n.

---

## 🔄 Fluxo de Funcionamento

- Usuário envia mensagem via WhatsApp.

- EvolutionAPI recebe e dispara para o Webhook do n8n.

- O n8n envia os dados para o Servidor HTTP.

- O Servidor HTTP repassa ao Agente CrewAI.

- O agente processa com Llama 3.1:8B e devolve a resposta.

- O n8n envia a resposta de volta à EvolutionAPI.

- O usuário recebe a resposta no WhatsApp.

---

🚀 Próximos Passos

- Criar agentes especializados (ex: suporte, vendas, atendimento).

- Melhorar segurança das credenciais.

- Automatizar a configuração com scripts.
