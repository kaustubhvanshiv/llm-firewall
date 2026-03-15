SUSPICIOUS_PATTERNS = [
    "ignore previous instructions",
    "reveal system prompt",
    "show system prompt",
    "print system prompt",
    "developer mode",
    "debug mode",
    "pretend you are",
    "act as",
    "bypass safety",
    "ignore safety rules"
]


def detect_prompt_injection(prompt: str):

    lower_prompt = prompt.lower()

    for pattern in SUSPICIOUS_PATTERNS:
        if pattern in lower_prompt:
            return True

    return False