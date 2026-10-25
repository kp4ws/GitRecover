from pathlib import Path
import shlex
import subprocess

def run_cmd(cmd: str, git_repo: str | Path | None = None) -> str:
    args = shlex.split(cmd)
    result = ""
    try:
        cmd = subprocess.run(args, cwd=git_repo, capture_output=True, text=True, check=True)
        result = cmd.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Command failed with exit code {e.returncode}")

    return result