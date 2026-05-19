import os


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
        if not os.path.isfile(file_path):
            raise FileNotFoundError(
                f'"{file_path}" does not exist or is not a regular file'
            )
        if not file_path.endswith(".py"):
            raise ValueError(f'"{file_path}" is not a Python file')

        command = ["python", target]
        command.extend(args)

    except PermissionError as e:
        return f"Error: {e}"
