import time
import requests

WEAVIATE_URL = "http://weaviate:8080/v1/schema"
SCHEMA = {
    "class": "Document",
    "description": "A document with text and embedding",
    "properties": [
        {"name": "text", "dataType": ["text"]},
        {"name": "embedding", "dataType": ["number"], "description": "Vector embedding", "indexConfig": {"similarityFunction": "cosine"}}
    ]
}

def wait_for_weaviate():
    for _ in range(30):
        try:
            r = requests.get("http://weaviate:8080/v1/.well-known/ready")
            if r.status_code == 200:
                return True
        except Exception:
            pass
        time.sleep(2)
    return False

def create_schema():
    r = requests.post(WEAVIATE_URL, json=SCHEMA)
    if r.status_code == 200 or r.status_code == 422:
        print("Schema created or already exists.")
    else:
        print(f"Failed to create schema: {r.status_code} {r.text}")

if __name__ == "__main__":
    if wait_for_weaviate():
        create_schema()
    else:
        print("Weaviate did not become ready in time.")
