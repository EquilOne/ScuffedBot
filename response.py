import os
from collections.abc import Sequence

from dotenv import load_dotenv
from openai import AsyncOpenAI
from openai.types.responses import Response
from openai.types.responses.response_input_item import ResponseInputItem

from call_function import available_functions
from config import API_BASE_URL, MODEL_NAME
from prompts import system_prompt


async def get_response(
    input_messages: Sequence[ResponseInputItem],
) -> Response:
    load_dotenv()
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY not found. Add it to .env")
    client = AsyncOpenAI(
        base_url=API_BASE_URL,
        api_key=api_key,
    )
    return await client.responses.create(
        model=MODEL_NAME,
        input=input_messages,  # type: ignore[arg-type]
        instructions=system_prompt,
        tools=available_functions,
        tool_choice="auto",
    )
