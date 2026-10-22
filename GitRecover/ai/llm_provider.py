import json
from llama_cpp import Llama
from GitRecover.config import llm

#TODO: Figure out which model is best to use. Write down notes and submit them in VIULearn

class LLMProvider:
    def __init__(self):
        self.model = None

        try:
            self.model = Llama(
                model_path=llm.get("model_path"),
                n_ctx=llm.get("n_ctx"),
                n_threads=llm.get("n_threads"),
                verbose=False,
            )
        except Exception as e:
            print(e)
            print("**ERROR:** Cannot initialize local LLM. Ensure a model is provided prior to running the app and try again.")
            exit(1)

    def generate_response(self, payload: dict[str, object]) -> str:
        if not self.model:
            return

        print("test")
        
        response = self.model.create_chat_completion(
            messages = [
                {
                    "role": "system", 
                    "content": """
                    You are an expert Git recovery diagnostic engine.
                    You will receive a JSON payload containing repository state, git history (reflogs, dangling commits, etc), and the user context (prompt message).
                    Analyze the user's problem in the context of this data and output ONLY the exact terminal commands required to fix it.
                    Do not include markdown formatting, explanations, or conversational text.
                    """
                },
                {
                    "role": "user",
                    "content": f"""
                    Analyze this Git recovery request:
                    {json.dumps(payload, indent=2)}
                    """
                },
            ],
            temperature=0.2,
        )

        return response["choices"][0]["message"]["content"] or ""