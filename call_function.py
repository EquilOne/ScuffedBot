from openai.types.responses import ToolParam

from functions.get_file_content import get_file_content_tool
from functions.get_files_info import get_files_info_tool
from functions.run_python_file import run_python_file_tool
from functions.write_file import write_file_tool

available_functions: list[ToolParam] = [
    get_file_content_tool,
    get_files_info_tool,
    write_file_tool,
    run_python_file_tool,
]
