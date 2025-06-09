import time
import requests

WEAVIATE_URL = "http://weaviate:8080/v1"
SCHEMA = {
    "class": "Message",
    "description": "A message with text, embedding, role, and timestamp",
    "vectorizer": "none",
    "vectorIndexType": "hnsw",
    "properties": [
        {"name": "text", "dataType": ["text"]},
        {
            "name": "embedding",
            "dataType": ["number"],
            "description": "Vector embedding"
        },
        {"name": "role", "dataType": ["text"]},
        {"name": "timestamp", "dataType": ["date"]}
    ]
}

def wait_for_weaviate():
    for _ in range(30):
        try:
            r = requests.get(f"{WEAVIATE_URL}/.well-known/ready")
            if r.status_code == 200:
                return True
        except Exception:
            pass
        time.sleep(2)
    return False

def create_schema():
    payload = {"classes": [SCHEMA]}
    r = requests.post(f"{WEAVIATE_URL}/schema", json=payload)
    if r.status_code in (200, 409, 422):
        print("Schema created or already exists.")
    else:
        print(f"Failed to create schema: {r.status_code} {r.text}")

        
if __name__ == "__main__":
    if wait_for_weaviate():
        create_schema()
    else:
        print("Weaviate did not become ready in time.")
