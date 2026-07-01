import json
from collections.abc import Callable

from openai.types.responses import ToolParam
from openai.types.responses.response_function_tool_call import ResponseFunctionToolCall
from openai.types.responses.response_input_item import FunctionCallOutput
from rich.console import Console

from config import WORKING_DIRECTORY
from functions.get_file_content import get_file_content, get_file_content_tool
from functions.get_files_info import get_files_info, get_files_info_tool
from functions.run_python_file import run_python_file, run_python_file_tool
from functions.write_file import write_file, write_file_tool

console = Console()

available_functions: list[ToolParam] = [
    get_file_content_tool,
    get_files_info_tool,
    write_file_tool,
    run_python_file_tool,
]

function_map: dict[str, Callable[..., str]] = {
    "get_file_content": get_file_content,
    "get_files_info": get_files_info,
    "write_file": write_file,
    "run_python_file": run_python_file,
}


def call_function(
    function_call: ResponseFunctionToolCall, verbose: bool = False
) -> FunctionCallOutput:
    function_name = function_call.name or ""
    function_id = function_call.call_id
    try:
        function_args: dict = (
            json.loads(function_call.arguments) if function_call.arguments else {}
        )
    except json.JSONDecodeError:
        console.print(
            f"[yellow]Warning: malformed JSON arguments for {function_name}: "
            f"{function_call.arguments}[/yellow]"
        )
        function_args = {}

    if verbose:
        console.print(f"Calling function: {function_name}({function_args})")
    else:
        console.print(f"Calling function: {function_name}")

    if function_name not in function_map:
        return FunctionCallOutput(
            type="function_call_output",
            call_id=function_id,
            output=json.dumps({"error": f"Unknown function: {function_name}"}),
        )

    function_args["working_directory"] = WORKING_DIRECTORY

    try:
        function_result: str = function_map[function_name](**function_args)
    except Exception as e:
        return FunctionCallOutput(
            type="function_call_output",
            call_id=function_id,
            output=json.dumps({"error": f"Function execution failed: {e}"}),
        )

    if verbose:
        console.print(f"-> {function_result}")

    return FunctionCallOutput(
        type="function_call_output",
        call_id=function_id,
        output=json.dumps({"result": function_result}),
    )
