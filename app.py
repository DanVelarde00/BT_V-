from fastapi import FastAPI
from pydantic import BaseModel
import requests
from sentence_transformers import SentenceTransformer
import weaviate
from weaviate.util import generate_uuid5
import json
from datetime import datetime

# Constants
LLAMA3_MODEL = "llama3:instruct"
OLLAMA_URL = "http://ollama:11434/api/generate"
import os
WEAVIATE_URL = os.getenv("WEAVIATE_URL", "http://localhost:8080")

# FastAPI App
app = FastAPI()
model = SentenceTransformer("all-MiniLM-L6-v2")

# Weaviate client
client = weaviate.Client(WEAVIATE_URL)

# Request model
class ChatRequest(BaseModel):
    prompt: str
    top_k: int = 3

# Endpoint
@app.post("/chat")
def chat(request: ChatRequest):
    # Embed the prompt
    embedding = model.encode(request.prompt).tolist()
    print("📌 Prompt:", request.prompt)
    print("🔢 Embedding:", embedding[:5], "...")  # Show only first 5 for brevity

    # Store in Weaviate
    client.data_object.create(
        {"text": request.prompt, "embedding": embedding, "timestamp": datetime.utcnow().isoformat(), "role": "user"},
        class_name="Message",
        uuid=generate_uuid5(request.prompt)
    )

    # Search similar
    response = client.query.get("Message", ["text"]) \
        .with_near_vector({"vector": embedding}) \
        .with_limit(request.top_k) \
        .do()

    matches = response.get("data", {}).get("Get", {}).get("Message", [])
    context = "\n".join([m["text"] for m in matches])
    print("📚 Retrieved context:", context)

    # Ask LLM
    payload = {
        "model": LLAMA3_MODEL,
        "prompt": f"{context}\n\n{request.prompt}",
        "stream": False  # ✅ Required
    }

    try:
        r = requests.post(OLLAMA_URL, json=payload)
        if r.ok:
            print("🧠 Raw LLM JSON:", r.json())
            response_text = r.json().get("response", "(empty response field)")
        else:
            response_text = f"(LLM HTTP Error {r.status_code})"
    except Exception as e:
        response_text = f"(LLM error: {e})"

    print("🤖 LLM Response:", response_text)
    # Store assistant response
    client.data_object.create(
        {"text": response_text, "embedding": model.encode(response_text).tolist(), "timestamp": datetime.utcnow().isoformat(), "role": "assistant"},
        class_name="Message",
        uuid=generate_uuid5(response_text)
    )
    return {"response": response_text, "context": context}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
