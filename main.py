import asyncio
import json

from openai.types.responses import Response
from openai.types.responses.response_function_tool_call import ResponseFunctionToolCall
from openai.types.responses.response_input_param import ResponseInputParam
from rich.console import Console, Group
from rich.json import JSON
from rich.live import Live
from rich.panel import Panel
from rich.status import Status
from rich.table import Table
from rich.text import Text

from call_function import call_function
from custom_args import args

# from input import ChatInputApp
from response import get_response

console = Console(width=100)
status = Status("Crunching the tokens...", spinner="pipe", spinner_style="bold white")


# def construct_panel(content, **args):
#     return Panel(content, **args)


async def main():
    # if not args.one_shot:
    #     await ChatInputApp().run_async()
    #     return
    if not args.user_prompt:
        raise RuntimeError("One-shot (CLI mode) requires a prompt argument")

    resp: Response | None = None
    history: ResponseInputParam = []
    input = args.user_prompt
    function_calls = []
    function_results = []
    function_result_outputs = []
    ai_response = ""
    loop_iterations = 0
    # agent_memory = True

    history.append({"role": "user", "content": input})

    if args.dry_run:
        return

    with Live(Panel(Group(status), expand=False), console=console, transient=True):
        for i in range(20):
            loop_iterations = i + 1
            resp: Response | None = await get_response(history)

            function_calls: list[ResponseFunctionToolCall] = [
                item
                for item in resp.output
                if isinstance(item, ResponseFunctionToolCall)
            ]
            if len(function_calls) == 0:
                break
            for call in function_calls:
                call_result = call_function(call, verbose=args.verbose)
                function_results.append(call_result)
                function_result_outputs.append(call_result["output"])
            history.extend(function_results)
            ai_response = resp.output_text
            history.append({"role": "assistant", "content": ai_response})

        # print("resp:", resp.__dict__)
        if resp is None:
            raise RuntimeError("No response returned")
        assistant_response = Text()
        response_info = Text()
        response_info.append("User prompt: \n", style="bold")
        response_info.append(f"{input}")
        console.print(Panel(response_info, expand=False))
        if args.verbose:
            if not resp.usage:
                raise RuntimeError("No usage data found")
            usage = resp.usage
            # For testing purposes
            # print("User prompt: ", input)
            # print("Prompt tokens: ", usage.input_tokens)
            # print("Response tokens: ", usage.output_tokens)
            prompt_tokens = usage.input_tokens
            resp_tokens = usage.output_tokens
            reasoning_tokens = usage.output_tokens_details.reasoning_tokens

            tokens_table = Table(title="Tokens", title_justify="left")
            tokens_table.add_column("Token Type", justify="left", no_wrap=True)
            tokens_table.add_column("Count", justify="center", no_wrap=True)
            tokens_table.add_row("Prompt", str(prompt_tokens))
            tokens_table.add_row("Response", str(resp_tokens))
            tokens_table.add_row("Reasoning", str(reasoning_tokens))
            console.print(Panel(tokens_table, expand=False))

            model_info = Text()
            model_info.append("Model: ", style="bold")
            model_info.append(f"{resp.model}")
            if len(function_result_outputs) > 0:
                model_info.append("\nFunction call results: ", style="bold")
                for output in function_result_outputs:
                    model_info.append(f"{output}\n")
            console.print(Panel(model_info, expand=False))
        assistant_response.append("Assistant:\n\n", style="bold")
        assistant_response.append(ai_response)
        if len(function_calls) > 0:
            for call in function_calls:
                parsed_args = json.loads(call.arguments)
                assistant_response.append(
                    f"\nCalling function: {call.name}({parsed_args})"
                )
        console.print(Panel(assistant_response))
        if args.debug:
            # console.print("Response object: ", resp.model_dump())
            console.print(
                Panel(
                    JSON.from_data(resp.model_dump()),
                    title="Response object",
                    expand=True,
                )
            )
            console.print("Iteration(s): ", loop_iterations)


if __name__ == "__main__":
    asyncio.run(main())
