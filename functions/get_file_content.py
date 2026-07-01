import os

from openai.types.responses import FunctionToolParam

from config import MAX_CHARS


def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_file = (
            os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        )

        if not valid_target_file:
            raise PermissionError(
                f'Cannot read "{file_path}" as it is outside the permitted working directory'
            )

        if not os.path.isfile(target_file):
            raise FileNotFoundError(
                f'File not found or is not a regular file: "{file_path}"'
            )

        with open(target_file, "r", encoding="utf-8") as f:
            content = f.read(MAX_CHARS)
            if f.read(1):
                content += (
                    f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                )
        return content

    except PermissionError as e:
        return f"Error: {e}"
    except FileNotFoundError as e:
        return f"Error: {e}"
    except OSError as e:
        return f"Error: {e}"
    except UnicodeDecodeError as e:
        return f"Error: Could not decode file as UTF-8: {e}"


get_file_content_tool: FunctionToolParam = {
    "type": "function",
    "name": "get_file_content",
    "description": "Reads the contents of a file located inside the working directory and returns the contents as a string.",
    "strict": True,
    "parameters": {
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "The path to the file to read, relative to the working directory.",
            }
        },
        "required": ["file_path"],
        "additionalProperties": False,
    },
}
