from pathlib import Path
import subprocess

def run_cmd(*args, cwd: str = ".") -> str:
    result = ""
    try:
        cmd = subprocess.run(args, cwd=cwd, capture_output=True, text=True, check=True)
        result = cmd.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {' '.join(args)}")
        print(e.stderr)

    return result