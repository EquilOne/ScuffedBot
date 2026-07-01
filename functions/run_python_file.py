import os
import subprocess
import sys

from openai.types.responses import FunctionToolParam

from config import SUBPROCESS_TIMEOUT


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_path = (
            os.path.commonpath([working_dir_abs, target]) == working_dir_abs
        )

        if not valid_target_path:
            raise PermissionError(
                f'Cannot execute "{file_path}" as it is outside the permitted working directory'
            )
        if not os.path.isfile(target):
            raise FileNotFoundError(
                f'"{file_path}" does not exist or is not a regular file'
            )
        if not target.endswith(".py"):
            raise ValueError(f'"{file_path}" is not a Python file')

        command = [sys.executable, target]
        if args is not None:
            command.extend(args)

        result = subprocess.run(
            command, capture_output=True, text=True, timeout=SUBPROCESS_TIMEOUT
        )
        output_string = ""

        if result.returncode != 0:
            output_string += f"Process exited with code {result.returncode}\n"
        if not result.stdout and not result.stderr:
            output_string += "No output produced\n"
        output_string += f"STDOUT: {result.stdout}, STDERR: {result.stderr}"
        return output_string

    except PermissionError as e:
        return f"Error: {e}"
    except FileNotFoundError as e:
        return f"Error: {e}"
    except ValueError as e:
        return f"Error: {e}"
    except subprocess.TimeoutExpired:
        return f"Error: Execution timed out after {SUBPROCESS_TIMEOUT} seconds"
    except OSError as e:
        return f"Error: Could not execute file: {e}"


run_python_file_tool: FunctionToolParam = {
    "type": "function",
    "name": "run_python_file",
    "description": "Executes a Python file located inside the working directory and returns stdout and stderr, and any non-zero exit code.",
    "strict": True,
    "parameters": {
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "The path to the Python file to execute, relative to the working directory.",
            },
            "args": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Optional arguments to pass to the Python file.",
            },
        },
        "required": ["file_path"],
        "additionalProperties": False,
    },
}
