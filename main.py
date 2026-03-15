from fastapi import FastAPI
from pydantic import BaseModel
from llm.llm_client import generate_response

# imports from project
from security.input_filter import sanitize_prompt
from security.prompt_detector import detect_prompt_injection

app = FastAPI()


class ChatRequest(BaseModel):
    message: str


@app.get("/")
def home():
    return {"status": "LLM Firewall Running"}


@app.post("/chat")
def chat(req: ChatRequest):

    # Step 1: sanitize input
    user_prompt = sanitize_prompt(req.message)

    print("Prompt received:", user_prompt)

    # Step 2: detect prompt injection BEFORE calling model
    if detect_prompt_injection(user_prompt):
        return {
            "error": "Prompt injection attempt detected"
        }

    # Step 3: call LLM
    response = generate_response(user_prompt)

    return {
        "user": user_prompt,
        "response": response
        }
    
