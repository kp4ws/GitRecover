import subprocess

def run_cmd(*args, cwd: str = ".", capture_output=True, text=True, check=False, timeout=30, env=None, return_str=True) -> str | subprocess.CompletedProcess:
    result = ""
    try:
        cmd = subprocess.run(args, cwd=cwd, capture_output=capture_output, text=text, check=check, timeout=timeout, env=env)
        
        if return_str:
            result = cmd.stdout.strip()
        else:
            result = cmd

    except subprocess.CalledProcessError as e:
        print(f"Command failed: {' '.join(args)}")
        print(e.stderr)
    except subprocess.TimeoutExpired as e:
        print(f"Git {args[0]} timed out after 30 seconds.")
        print(e.stderr)
    except OSError as error:
        print(f"Unable to run Git: {error}")

    return result