import requests

print("Type your text and press Enter. Leave blank and press Enter to exit.")
while True:
    prompt = input("You: ")
    if not prompt.strip():
        break
    #problem wwith ports 
    try:
        resp = requests.post(
            "http://localhost:5000/embed",
            json={"text": prompt}
        )
        data = resp.json()
        print("Embedding:", data.get("embedding", "(no response)"))
    except Exception as e:
        print("❌ Error:", e)
