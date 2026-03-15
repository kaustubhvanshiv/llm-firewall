import requests

OLLAMA_API = "http://localhost:11434/api/generate"
MODEL = "llama3"

def generate_response(prompt: str):

    print("Sending prompt to Ollama...")

    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(OLLAMA_API, json=payload)

    print("Response received")

    if response.status_code == 200:
        return response.json()["response"]

    return "Error contacting model"