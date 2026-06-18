import asyncio
import json

from openai.types.responses.response_function_tool_call import ResponseFunctionToolCall
from openai.types.responses.response_input_param import ResponseInputParam
from rich import print
from rich.console import Console, Group
from rich.live import Live
from rich.panel import Panel
from rich.status import Status
from rich.table import Table
from rich.text import Text

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

    history: ResponseInputParam = []
    input = args.user_prompt
    # agent_memory = True

    history.append({"role": "user", "content": input})

    if args.dry_run:
        return

    with Live(Panel(Group(status), expand=False), console=console, transient=True):
        resp = await get_response(history)

    ai_response = resp.output_text
    function_calls: list[ResponseFunctionToolCall] = [
        item for item in resp.output if isinstance(item, ResponseFunctionToolCall)
    ]

    # print("resp:", resp.__dict__)

    if args.verbose:
        if not resp.usage:
            raise RuntimeError("No usage data found")
        usage = resp.usage
        # For testing purposes
        print("User prompt: ", input)
        print("Prompt tokens: ", usage.input_tokens)
        print("Response tokens: ", usage.output_tokens)
        prompt_tokens = usage.input_tokens
        resp_tokens = usage.output_tokens
        reasoning_tokens = usage.output_tokens_details.reasoning_tokens

        tokens_table = Table(title="Tokens", title_justify="left")
        tokens_table.add_column("Token Type", justify="left", no_wrap=True)
        tokens_table.add_column("Count", justify="center", no_wrap=True)
        tokens_table.add_row("Prompt", str(prompt_tokens))
        tokens_table.add_row("Response", str(resp_tokens))
        tokens_table.add_row("Reasoning", str(reasoning_tokens))
        print(Panel(tokens_table, expand=False))

        response_info = Text()
        response_info.append("User prompt: ", style="bold")
        response_info.append(f"{input}\n")
        response_info.append("Model: ", style="bold")
        response_info.append(resp.model)
        # print("User prompt: ", input)
        # print("Model: ", resp.model)
        print(Panel(response_info, expand=False))
    if args.debug:
        console.print("Response object: ", resp.model_dump())

    assistant_response = Text()
    assistant_response.append("Assistant:\n\n", style="bold")
    assistant_response.append(ai_response)
    if function_calls:
        for call in function_calls:
            parsed_args = json.loads(call.arguments)
            assistant_response.append(f"\nCalling function: {call.name}({parsed_args})")
    print(Panel(assistant_response))


if __name__ == "__main__":
    asyncio.run(main())
