import json
from datetime import datetime

LOG_FILE = "logs/attack_logs.json"


def log_attack(prompt, attack_type):
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "attack_type": attack_type,
        "prompt": prompt,
        "action": "blocked"
    }

    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")
        
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

def detect_prompt_injection(prompt):

    lower_prompt = prompt.lower()

    for pattern in SUSPICIOUS_PATTERNS:
        if pattern in lower_prompt:
            log_attack(prompt, "prompt_injection")
            return True

    return False