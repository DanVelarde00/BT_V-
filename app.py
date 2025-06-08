from fastapi import FastAPI
from weaviate import Client
from sentence_transformers import SentenceTransformer
from pydantic import BaseModel
from typing import List
import requests

app = FastAPI()

weaviate_client = Client("http://weaviate:8080")
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
OLLAMA_URL = "http://ollama:11434/api/generate"
LLAMA3_MODEL = "llama3"

class EmbedRequest(BaseModel):
    text: str

class StoreRequest(BaseModel):
    content: str
    embedding: List[float]

class ChatRequest(BaseModel):
    prompt: str
    top_k: int = 3  # Number of similar past prompts to recall

class ChatResponse(BaseModel):
    response: str
    similar: List[str]

@app.post("/embed")
def embed_text(request: EmbedRequest):
    embedding = embedding_model.encode(request.text).tolist()
    return {"embedding": embedding}

@app.post("/store")
def store_document(request: StoreRequest):
    weaviate_client.data_object.create(
        {
            "content": request.content,
            "embedding": request.embedding
        },
        "Document"
    )
    return {"status": "success"}

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    # 1. Embed the prompt
    prompt_embedding = embedding_model.encode(request.prompt).tolist()

    # 2. Recall similar past prompts/responses from Weaviate
    similar = []
    try:
        result = weaviate_client.query.get("Document", ["content"]).with_near_vector({"vector": prompt_embedding, "certainty": 0.7}).with_limit(request.top_k).do()
        if result and "data" in result and "Get" in result["data"] and "Document" in result["data"]["Get"]:
            similar = [doc["content"] for doc in result["data"]["Get"]["Document"]]
    except Exception:
        pass

    # 3. Send prompt to Llama 3 via Ollama
    payload = {"model": LLAMA3_MODEL, "prompt": request.prompt}
    r = requests.post(OLLAMA_URL, json=payload)
    response_text = r.json().get("response", "") if r.ok else "(LLM error)"

    # 4. Embed and store prompt/response in Weaviate
    try:
        weaviate_client.data_object.create(
            {"content": f"Prompt: {request.prompt}\nResponse: {response_text}", "embedding": embedding_model.encode(request.prompt + response_text).tolist()},
            "Document"
        )
    except Exception:
        pass

    return ChatResponse(response=response_text, similar=similar)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
