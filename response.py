import os

from dotenv import load_dotenv
from openai import OpenAI
from openai.types.responses import Response
from openai.types.responses.response_input_param import ResponseInputParam

load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")
if api_key is None:
    raise RuntimeError("Api key not found")


def get_response(input: ResponseInputParam) -> Response:
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    resp = client.responses.create(
        model="openrouter/free",
        input=input,
    )
    if not resp:
        raise RuntimeError("No response returned")
    return resp
