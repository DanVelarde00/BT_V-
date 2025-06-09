import requests

print("Type your text and press Enter. Leave blank and press Enter to exit.")
while True:
    prompt = input("You: ")
    if not prompt.strip():
        break
    try:
        # Get embedding from app
        resp = requests.post(
            "http://localhost:5000/embed",
            json={"text": prompt}
        )
        data = resp.json()
        print("Embedding:", data.get("embedding", "(no response)"))
        # Get LLM response from app
        chat_resp = requests.post(
            "http://localhost:5000/chat",
            json={"prompt": prompt, "top_k": 3}
        )
        chat_data = chat_resp.json()
        print("LLM Response:", chat_data.get("response", "(no response)"))
        if chat_data.get("similar"):
            print("Similar past prompts:")
            for s in chat_data["similar"]:
                print("-", s)
    except Exception as e:
        print("❌ Error:", e)
