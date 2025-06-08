import requests

print("Type your prompt and press Enter. Leave blank and press Enter to exit.")
while True:
    prompt = input("You: ")
    if not prompt.strip():
        break
    try:
        resp = requests.post(
            "http://localhost:5000/chat",
            json={"prompt": prompt, "top_k": 3}
        )
        data = resp.json()
        print("Llama3:", data.get("response", "(no response)"))
        if data.get("similar"):
            print("Similar past entries:")
            for s in data["similar"]:
                print("-", s)
    except Exception as e:
        print("Error:", e)
