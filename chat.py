import requests

print("Type your text and press Enter. Leave blank and press Enter to exit.")
while True:
    prompt = input("You: ")
    if not prompt.strip():
        break
    try:
        # Get LLM response and context from app (correct port 5001)
        chat_resp = requests.post(
            "http://localhost:5001/chat",
            json={"prompt": prompt, "top_k": 3}
        )
        chat_data = chat_resp.json()
        print("LLM Response:", chat_data.get("response", "(no response)"))
        if chat_data.get("context"):
            print("Context:")
            print(chat_data["context"])
    except Exception as e:
        print("❌ Error:", e)
