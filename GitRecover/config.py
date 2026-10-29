#TODO: Should config.toml be in package directory or root directory?

import tomllib
from pathlib import Path

PACKAGE_DIR = Path(__file__).resolve().parent
DEFAULT_MODEL_PATH = PACKAGE_DIR / "models" / "Llama-3.2-1B-Instruct-Q4_K_M.gguf" #TODO Update this with default model filename
CONFIG_PATH = Path(__file__).parent / "config.toml"

#Assumes config.toml exists, no current error handling if missing
with open(CONFIG_PATH, "rb") as f:
    config = tomllib.load(f)

llm = config.get("llm", {})
#TODO: This has bug, need to implement better way of getting the model's path
model_path = Path(llm.get("model_path", DEFAULT_MODEL_PATH))

if not model_path.exists():
    model_path = DEFAULT_MODEL_PATH

llm["model_path"] = str(model_path)