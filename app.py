from fastapi import FastAPI
from weaviate import Client
from sentence_transformers import SentenceTransformer
from pydantic import BaseModel
from typing import List

app = FastAPI()

weaviate_client = Client("http://weaviate:8080")
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

class EmbedRequest(BaseModel):
    text: str

class StoreRequest(BaseModel):
    content: str
    embedding: List[float]

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
