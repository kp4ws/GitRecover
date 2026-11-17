from GitRecover.config import llm
import re

MAX_CHAT_HISTORY_MESSAGES = 5

# NOTE: This prompt was created with help from generative AI
SYSTEM_PROMPT = (
    "You are an expert Git recovery assistant embedded in GitRecover. "
    "Your job is to analyze the user's message and raw repository context to infer the exact Git disaster and recommend the safest recovery steps.\n\n"
    "RECOVERY KNOWLEDGE BASE:\n"
    "- Direct commit to main: 1. git branch <new-branch>, 2. git reset --hard HEAD~1, 3. git checkout <new-branch>\n"
    "- Bad merge (already committed locally): 1. git reset --hard HEAD~1\n"
    "- Bad merge (already pushed to remote): 1. git revert -m 1 HEAD, 2. git push\n"
    "- Active conflict currently in progress: 1. git merge --abort (to cancel and start over)\n"
    "- Recovering orphaned/dangling commits (dropped stash, deleted branch, detached HEAD, bad reset): 1. git show <hash>, 2. git branch <new-branch> <hash>, 3. git checkout <new-branch>\n"
    "- Lost staged file (dangling blob): 1. git cat-file -p <blob-hash> > <filename>\n"
    "- Messed up rebase: 1. git rebase --abort (if actively in progress) OR 2. git reset --hard HEAD@{1}\n\n"
    "STRICT CONSTRAINTS:\n"
    "1. Always address the user directly as 'You'. Never repeat or echo the prompt using 'I'.\n"
    "2. Infer the situation from the context and user request; state what happened in one brief opening sentence, followed by a new line.\n"
    "3. Every step MUST start on its own new line. Never collapse steps or options into a single paragraph.\n"
    "4. All Git commands must be complete and fully executable using real hashes/filenames from context, relative refs like HEAD~1 or HEAD, or explicit fallback branch names like 'feature-branch'. NEVER leave trailing commas, blank targets, or missing arguments (e.g. write 'git revert -m 1 HEAD', NEVER write 'git revert -m 1').\n"
    "5. State any data loss risk in one brief sentence BEFORE listing a destructive command like 'reset --hard'.\n"
    "6. Recommend at most 4 concise numbered steps.\n"
    "7. Output plain text only. Do NOT use markdown formatting, code blocks, backticks, or bolding. /no_think"
)

class LLMProvider:
    def __init__(self):
        '''Only load model on first use, not in constructor'''
        self.model = None

    def load_model(self):
        if self.model:
            #if model is already loaded, return
            return
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
            print(f"ERROR: Not able to load model {e}\n Please try again.")
            #  raise RuntimeError(f"Cannot initialize local LLM. Check model path.\n Details: {e}")

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