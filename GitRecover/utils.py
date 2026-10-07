import subprocess
import shlex
from pathlib import Path

def run_cmd(cmd: str, cwd: str | Path | None = None) -> str:
    args = shlex.split(cmd)
    result = ""
    try:
        cmd = subprocess.run(args, cwd=cwd, capture_output=True, text=True, check=True)
        result = cmd.stdout
    except subprocess.CalledProcessError as e:
        print(f"Command failed with exit code {e.returncode}")

    return result