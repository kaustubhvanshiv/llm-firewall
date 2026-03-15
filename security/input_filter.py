def sanitize_prompt(prompt: str) -> str:
    prompt = prompt.strip()

    # remove excessive newlines
    while "\n\n\n" in prompt:
        prompt = prompt.replace("\n\n\n", "\n")

    return prompt