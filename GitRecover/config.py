"""
Author: Kent Pawson
config.py loads the application settings and resolves the local model path.
"""

import tomllib
import sys
from pathlib import Path

PACKAGE_DIR = Path(__file__).resolve().parent
APPLICATION_ROOT = (
    Path(sys._MEIPASS)
    if hasattr(sys, "_MEIPASS")
    else PACKAGE_DIR.parent
)
DEFAULT_MODEL_PATH = APPLICATION_ROOT / "GitRecover" / "models" / "Qwen3-4B-Q4_K_M.gguf"
CONFIG_PATH = APPLICATION_ROOT / "GitRecover" / "config.toml"

with open(CONFIG_PATH, "rb") as f:
    config = tomllib.load(f)

llm = config.get("llm", {})
configured_model_path = Path(llm.get("model_path", DEFAULT_MODEL_PATH))
if configured_model_path.is_absolute():
    model_path = configured_model_path
else:
    model_path = APPLICATION_ROOT / configured_model_path

if not model_path.exists():
    model_path = DEFAULT_MODEL_PATH

llm["model_path"] = str(model_path)

if not getattr(sys, "frozen", False):
    print("Current model: ", llm["model_path"])