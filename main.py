from fastapi import FastAPI, Request
from pydantic import BaseModel
from llm.llm_client import generate_response

# imports from project
from security.input_filter import sanitize_prompt
from security.prompt_detector import detect_prompt_injection
from security.rate_limiter import is_rate_limited
from security.output_filter import filter_output

app = FastAPI()


class ChatRequest(BaseModel):
    message: str


@app.get("/")
def home():
    return {"status": "LLM Firewall Running"}


@app.post("/chat")
def chat(req: ChatRequest, request: Request):

    client_ip = request.client.host

    if is_rate_limited(client_ip):
        return {"error": "Rate limit exceeded"}

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

    # Step 4: output filtering
    response = filter_output(response)

    return {
        "user": user_prompt,
        "response": response
    }