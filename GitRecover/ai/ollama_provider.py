import json
from ollama import chat

#TODO: Determine if llama.cpp is better to use than ollama

def provide_feedback(user_payload_json: dict) -> str:
    payload_str = json.dumps(user_payload_json)
    messages = [
        {
            "role": "system",
            "content": f"""
            You are an expert Git recovery diagnostic engine.
            You will receive a JSON payload containing repository state, git history (reflogs, dangling commits, etc), and the user context (prompt message).
            Analyze the user's problem in the context of this data and output ONLY the exact terminal commands required to fix it.
            Do not include markdown formatting, explanations, or conversational text.
            """
            #TODO Determine what LLM should output (JSON, pure bash commands, etc) ?
        },
        {
            "role": "user",
            "content": f"{payload_str}"
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