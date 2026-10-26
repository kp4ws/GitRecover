import json
from llama_cpp import Llama
from GitRecover.config import llm
import re

class LLMProvider:
    def __init__(self):
        '''Only load model on first use, not in constructor'''
        self.model = None

    def _load_model(self):
        try:
            self.model = Llama(
                model_path=llm.get("model_path"),
                n_ctx=llm.get("n_ctx"),
                n_threads=llm.get("n_threads"),
                n_batch=llm.get("n_batch"),
                verbose=False,
            )
        except Exception as e:
             raise RuntimeError(f"Cannot initialize local LLM. Check model path.\n Details: {e}")

    def generate_response(self, chat_history: list[dict], payload: dict = None) -> str:
        if self.model is None:
            '''This will be true on first use, where model is first loaded'''
            self._load_model()

        #System Prompt
        messages = [
            {
                "role": "system", 
                "content": """
                You are an expert Git recovery diagnostic engine.
                You will receive a JSON payload containing repository state, git history (reflogs, dangling commits, etc), and the user context (prompt message).
                Analyze the user's problem in the context of this data and output ONLY the exact terminal commands required to fix it.
                Do not include markdown formatting, explanations, or conversational text.
                """
            }
        ]

        #Recovery Payload
        if payload:
            raw_json = json.dumps(payload)
            json_text = re.sub(r'[{}[\]",]', '', raw_json)

            messages.append(
                {
                    "role": "user",
                    "content": f"""
                    Analyze this Git recovery request:
                    {json_text}
                    """
                }
            )

        #Extend chat history
        messages.extend(chat_history)
        
        #Generate response
        response = self.model.create_chat_completion(
            messages=messages,
            temperature=0.2,
        )

        unfiltered_response = response["choices"][0]["message"]["content"] or ""

        #Remove "thinking" from the response
        filtered_response = re.sub(r'<think>.*?</think>', '', unfiltered_response, flags=re.DOTALL)
        return filtered_response.strip()