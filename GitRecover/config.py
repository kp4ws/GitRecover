#TODO: Should config.toml be in package directory or root directory?

import tomllib
from pathlib import Path

PACKAGE_DIR = Path(__file__).resolve().parent
DEFAULT_MODEL_PATH = PACKAGE_DIR / "models" / "Qwen3-4B-Q4_K_M.gguf"
CONFIG_PATH = Path(__file__).parent / "config.toml"

#Assumes config.toml exists, no current error handling if missing
with open(CONFIG_PATH, "rb") as f:
    config = tomllib.load(f)

llm = config.get("llm", {})
model_path = Path(llm.get("model_path", DEFAULT_MODEL_PATH))

if not model_path.exists():
    model_path = DEFAULT_MODEL_PATH

llm["model_path"] = str(model_path)