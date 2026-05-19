import os


def write_file(working_dir: str, file_path: str, content: str) -> str:
    try:
        working_dir_abs = os.path.abspath(working_dir)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        parent_dir = os.path.dirname(target_file)
        valid_target_path = (
            os.path.commonpath([working_dir_abs, parent_dir]) == working_dir_abs
        )
        if not valid_target_path:
            raise PermissionError(
                f'Cannot write to "{file_path}" as it is outside the permitted working directory'
            )

        if os.path.isdir(target_file):
            raise IsADirectoryError(
                f'Cannot write to "{file_path}" as it is a directory'
            )

        os.makedirs(parent_dir, exist_ok=True)
        with open(target_file, "w") as f:
            f.write(content)
        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )

    except PermissionError as e:
        return f"Error: {e}"
    except IsADirectoryError as e:
        return f"Error: {e}"
