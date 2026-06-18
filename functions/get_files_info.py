import os

from openai.types.responses import FunctionToolParam


def get_files_info(working_directory, directory="."):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        valid_target_dir = (
            os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        )
        info_list = []

        if not valid_target_dir:
            raise PermissionError(
                f'Cannot list "{directory}" as it is outside the permitted working directory'
            )

        if not os.path.isdir(target_dir):
            raise NotADirectoryError(f'"{directory}" is not a directory')

        if not os.path.exists(target_dir):
            raise FileNotFoundError(f'"{directory}" does not exist')

        dir_contents = os.listdir(target_dir)

        for item in dir_contents:
            current_item_path = os.path.normpath(os.path.join(target_dir, item))
            item_info = f"- {item}: file_size={os.path.getsize(current_item_path)} bytes, is_dir={os.path.isdir(current_item_path)}"
            info_list.append(item_info)
        return "\n".join(info_list)

    except PermissionError as e:
        return f"Error: {e}"
    except NotADirectoryError as e:
        return f"Error: {e}"
    except FileNotFoundError as e:
        return f"Error: {e}"


get_files_info_tool: FunctionToolParam = {
    "type": "function",
    "name": "get_files_info",
    "description": "Lists the contents of a directory located inside the working directory and returns the contents as a string.",
    "strict": True,
    "parameters": {
        "type": "object",
        "properties": {
            "directory": {
                "type": "string",
                "description": "The path to the file to read, relative to the working directory.",
            }
        },
        "required": ["directory"],
        "additionalProperties": False,
    },
}
