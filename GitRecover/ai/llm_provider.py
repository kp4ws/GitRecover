from GitRecover.config import llm
import re

MAX_CHAT_HISTORY_MESSAGES = 5
SYSTEM_PROMPT = (
    "You are a cautious, expert Git recovery assistant. "
    "Use the supplied repository state; never assume a commit was pushed or shared. "
    "Recommend the smallest safe fix using at most 4 concise, numbered steps. "
    "If unsure about recommendation, ask user follow-up question."
    "Rules for Git commands:\n"
    "1. Every command must be complete and fully executable. NEVER leave commands incomplete or missing arguments (e.g., write 'git reset --hard HEAD~1', never leave empty targets like 'git cherry-pick').\n"
    "2. Use exact commit hashes from context or valid relative refs like HEAD~1 or HEAD@{1}. NEVER use pseudo-code or placeholders like {commit} or <hash>.\n"
    "3. For commits accidentally made to main, use the canonical 3-step sequence: git branch <new-branch>, git reset --hard HEAD~1, git checkout <new-branch>.\n"
    "4. Before recommending destructive commands (reset --hard, rebase, clean), state the risk briefly.\n"
    "Do not use markdown, code blocks, or backticks in your output. Plain text only. /no_think"
)

class LLMProvider:
    def __init__(self):
        '''Only load model on first use, not in constructor'''
        self.model = None

    def load_model(self):
        try:
            from llama_cpp import Llama

            self.model = Llama(
                model_path=llm.get("model_path"),
                n_ctx=llm.get("n_ctx"),
                n_threads=llm.get("n_threads"),
                n_batch=llm.get("n_batch"),
                verbose=False,
            )
        except Exception as e:
             raise RuntimeError(f"Cannot initialize local LLM. Check model path.\n Details: {e}")

    def generate_response(self, chat_history: list[dict], context: str) -> str:
        if self.model is None:
            '''This will be true on first use, where model is first loaded'''
            self.load_model()

        #System Prompt combined with repository context
        messages = [
            {
                "role": "system", 
                "content": f"{SYSTEM_PROMPT}\n\nCURRENT REPOSITORY CONTEXT:\n{context}"
            }
        ]

        # Use last 5 history entries
        messages.extend(chat_history[-MAX_CHAT_HISTORY_MESSAGES:])
        
        #Generate response
        #TODO Determine if params should be added/changed to speed up model response time
        response = self.model.create_chat_completion(
            messages=messages,
            temperature=llm["temperature"],
            max_tokens=llm["max_tokens"],
            frequency_penalty=llm["frequency_penalty"],
            presence_penalty=llm["presence_penalty"],
        )

        unfiltered_response = response["choices"][0]["message"]["content"] or ""

        filtered_response = self._filter_response(unfiltered_response)
        return filtered_response.strip()

    def _filter_response(self, unfiltered_response: str):
        #Remove reasoning tags from response
        filtered_text = re.sub(
            r"<think>.*?(?:</think>|$)",
            "",
            unfiltered_response,
            flags=re.DOTALL,
        )

        #Enforce plain text (remove ticks, etc)
        filtered_text = re.sub(r"```[a-zA-Z]*", "", filtered_text)  # remove ```bash or ```
        filtered_text = filtered_text.replace("```", "").replace("`", "")
        filtered_text = re.sub(r"\*\*(.*?)\*\*", r"\1", filtered_text) # convert **bold** to plain text

        return filtered_text