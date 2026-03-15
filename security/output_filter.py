SENSITIVE_PATTERNS = [
    "system prompt",
    "api key",
    "internal instruction"
]


def filter_output(response):

    lower = response.lower()

    for pattern in SENSITIVE_PATTERNS:
        if pattern in lower:
            return "Response blocked due to sensitive content"

    return response