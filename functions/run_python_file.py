import os
import subprocess


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

        command = ["python", target]
        if args is not None:
            command.extend(*args)

        result = subprocess.run(command, capture_output=True, text=True)
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
