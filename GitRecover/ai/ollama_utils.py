from ollama import chat

def provide_feedback(user_message: str) -> str | None:
    messages = [
        {
            "role": "system",
            "content": "You are a helpful git support specialist. Be concise and never use emojis. Your responses should be formatted in JSON. Please provide your certainty level and specific sequence of actions or commands to be run."
        },
        {
            "role": "user",
            "content": f"{user_message}"
        },
    ]

    response = chat(
        model="llama3.2:latest", 
        messages=messages,
        # stream=True,
        )

    return response.message.content

    # for chunk in response:
    #     print(chunk.message.content, end="", flush=True)