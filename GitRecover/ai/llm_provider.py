from llama_cpp import Llama

# llm = Llama(
#     model_path="./models" #TODO,
#     #TODO other params
# )

# llm.create_chat_completion(
#     messages = [
#         {
#             "role": "system", 
#             "content": f"""
#             You are an expert Git recovery diagnostic engine.
#             You will receive a JSON payload containing repository state, git history (reflogs, dangling commits, etc), and the user context (prompt message).
#             Analyze the user's problem in the context of this data and output ONLY the exact terminal commands required to fix it.
#             Do not include markdown formatting, explanations, or conversational text.
#             """},
#         {
#             "role": "user",
#             "content": ""
#         }
#     ]
# )