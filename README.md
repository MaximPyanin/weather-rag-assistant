# RAG-Weather-Assistant

**This project is a RAG micro-service designed to provide real-time weather information using advanced AI techniques, including Azure OpenAI models,Langchain orchestration  and Weaviate vector storage.**

## 📖 Overview

<p align="center">
  <!-- Python -->
  <a href="#">
    <img src="https://img.shields.io/badge/Python-3.11-blue?logo=python" alt="Python 3.11">
  </a>
  <!-- LangChain -->
  <a href="#">
    <img src="https://img.shields.io/badge/LangChain-0.3.x-346CA5?logo=langchain" alt="LangChain">
  </a>
  <!-- Weaviate (Vector DB) -->
  <a href="https://weaviate.io/" target="_blank">
    <img src="https://img.shields.io/badge/Vector DB-Weaviate-FF6F00?logo=weaviate&logoColor=white" alt="Weaviate Vector DB">
  </a>
  <!-- ChatGPT / OpenAI -->
  <a href="https://openai.com/" target="_blank">
    <img src="https://img.shields.io/badge/ChatGPT-74aa9c?logo=openai&logoColor=white" alt="ChatGPT (OpenAI)">
  </a>
  <!-- Microsoft Azure -->
  <a href="https://azure.microsoft.com/" target="_blank">
    <img src="https://custom-icon-badges.demolab.com/badge/Microsoft%20Azure-0089D6?logo=msazure&logoColor=white" alt="Microsoft Azure">
  </a>
  <!-- Flask -->
  <a href="https://flask.palletsprojects.com/" target="_blank">
    <img src="https://img.shields.io/badge/Framework-Flask%203.1-orange?logo=flask" alt="Flask 3.1">
  </a>
</p>


---

## ✨ Features

- Openai GPT model for generative responses
- Openai embedding model for vector embeddings
- Clean architecture with typed LangChain layers
- 🏗️ Integration with Azure OpenAI model deployment and Weaviate vector database
- 🐍 Flask-based backend with Swagger UI
- Docker and Docker Compose for infrastructure management

---

## 📁 Project Hierarchy
The project structure follows a clean, modular approach:
```plaintext
├── src/
│   ├── api/                # RESTful API and Swagger documentation
│   ├── adapters/           # Integration layer with external services (e.g., Weaviate)
│   ├── controllers/        # Orchestration layer, managing request handling and response
│   ├── embeddings_providers/ # Language models and embeddings services (Azure-based)
│   ├── llm_providers/      # Language model wrappers for seamless integration
│   ├── services/           # Core business logic, including data indexing and QA systems
│   ├── config/             # Configuration management for runtime settings
│   └── prompts/            # Predefined prompt templates for consistent LLM interactions
├── Dockerfile              # Docker configuration for containerized deployment
├── docker-compose.yml      # Local development environment setup (API + Weaviate)
```

---

## 🚀 Quick Start 

```bash
# 1 – clone
git clone https://github.com/MaximPyanin/rag-weather-assistant.git
cd rag-weather-assistant

# 2 – create .env (fill Azure creds)
cp .env.sample .env
# AZURE_OPENAI_ENDPOINT=https://<resource>.openai.azure.com/
# AZURE_OPENAI_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
# AZURE_OPENAI_EMBEDDING_ENDPOINT=https://<resource>.openai.azure.com/

# 3 – build & run
docker compose up -d --build

# 4 – open docs
open http://localhost:5000/swagger/

# 5 – sample request
curl -X POST http://localhost:5000/api/v1/ask \
     -H "Content-Type: application/json" \
     -d '{"query": "What is the temperature in Madrid?"}'
```

---

## 🔧 Configuration
You can configure the application using environment variables. The following variables are required:
```plaintext
AZURE_OPENAI_ENDPOINT -	Base URL of your Azure OpenAI resource
AZURE_OPENAI_KEY - Secret key or leave empty ↠ Managed Identity token
AZURE_OPENAI_LLM_DEPLOYMENT - GPT deployment (default gpt-35-turbo)
AZURE_OPENAI_EMBEDDING_ENDPOINT - Same resource or separate embeddings endpoint
AZURE_OPENAI_EMBEDDING_DEPLOYMENT - Embedding deployment (default text-embedding-ada-002)
```
***Any value in AppConfig can be overridden via .env***

## 📜 LICENSE
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.