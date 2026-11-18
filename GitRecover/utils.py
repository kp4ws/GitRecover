"""
Author: Kent Pawson
utils.py contain helper functions to be used throughout the application.
Speficially, it contains the run_cmd function which can be used to run a terminal command.
"""

import subprocess

def run_cmd(*args, cwd: str = ".", capture_output=True, text=True, check=False, timeout=30, env=None, return_str=True) -> str | subprocess.CompletedProcess:
    """Run a command and return its output or process result.

    Parameters:
        *args: Arguments to execute.
        cwd: The directory to execute the command in.
        capture_output: Determines if standard output and standard error should be captured.
        text: Determine if text mode should be used or not.
        check: Determine if to raise exception on a non-zero exit status.
        timeout: Maximum execution time in seconds.
        env: Environment mapping used for the child process.
        return_str: Determine if return value should be output as string or CompletedProcess.

    Returns:
        The stripped stdout string or CompletedProcess depending on return_str parameter.
    """
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