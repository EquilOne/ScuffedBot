import os

from dotenv import load_dotenv
from openai import AsyncOpenAI
from openai.types.responses import Response
from openai.types.responses.response_input_param import ResponseInputParam

from call_function import available_functions
from prompts import system_prompt

load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")
if api_key is None:
    raise RuntimeError("Api key not found")


async def get_response(input: ResponseInputParam) -> Response:
    client = AsyncOpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    resp = await client.responses.create(
        model="inception/mercury-2:nitro",
        input=input,
        instructions=system_prompt,
        tools=available_functions,
        tool_choice="auto",
    )
    if not resp:
        raise RuntimeError("No response returned")
    return resp
