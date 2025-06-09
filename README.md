# BT_v2: Conversational LLM with Vector Memory

This project provides a conversational interface to an LLM (Ollama/Llama3) with vector-based memory using Weaviate and sentence-transformers. It supports storing, retrieving, and recalling past conversations for context-aware responses.

## Features
- Embeds user and assistant messages with sentence-transformers
- Stores messages, roles, and timestamps in Weaviate
- Retrieves similar past messages for context
- Uses Ollama (Llama3) for LLM responses
- Simple CLI chat interface

## Prerequisites
- [Docker](https://www.docker.com/products/docker-desktop)
- [Python 3.11+](https://www.python.org/downloads/)
- (Optional) [pipenv](https://pipenv.pypa.io/en/latest/) or `venv` for local Python

## Quickstart

### 1. Clone the repository
```sh
git clone <your-repo-url>
cd BT_v2
```

### 2. Build and start all services
```sh
docker-compose up --build -d
```
This will start:
- Weaviate (vector database)
- Ollama (LLM server)
- App (FastAPI server with embedding, chat, and memory)
- Init-schema (sets up Weaviate schema)

### 3. Download the Llama3 model for Ollama
```sh
docker exec -it ollama ollama pull llama3
```
Wait for the model to finish downloading before chatting.

### 4. (Optional) Create and activate a Python virtual environment
```sh
python -m venv venv
.\venv\Scripts\activate  # On Windows
# or
source venv/bin/activate  # On Linux/Mac
pip install -r requirements-extra.txt
```

### 5. Start chatting!
```sh
python chat.py
```
Type your message and press Enter. Leave blank and press Enter to exit.

## How it works
- `chat.py` sends your prompt to `/embed` and `/chat` endpoints on the app server.
- The app server embeds and stores messages in Weaviate, retrieves similar past messages, and gets a response from Llama3 via Ollama.
- Both user and assistant messages are stored with roles and timestamps for rich conversational memory.

## Troubleshooting
- **LLM Response: (LLM error) or (no response)**
  - Make sure the Llama3 model is downloaded in Ollama (`docker exec -it ollama ollama pull llama3`).
  - Check that all containers are running: `docker ps`
  - Check logs: `docker-compose logs app` or `docker-compose logs ollama`
- **Port conflicts**: Ensure nothing else is using ports 5000, 8080, or 11434.

## Customization
- To use a different LLM, update the model name in `app.py` and pull the model in Ollama.
- To extend memory, adjust the Weaviate schema and retrieval logic.

## File Overview
- `app.py` — FastAPI app with /embed and /chat endpoints
- `chat.py` — CLI chat client
- `init_weaviate_schema.py` — Sets up Weaviate schema
- `docker-compose.yml` — Orchestrates all services
- `Dockerfile.*` — Docker build files for each service

## License
MIT
