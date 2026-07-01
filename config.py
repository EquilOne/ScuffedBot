import os

MAX_CHARS = 10000
MAX_ITERATIONS = 20
WORKING_DIRECTORY = "."
API_BASE_URL = "https://openrouter.ai/api/v1"
MODEL_NAME = os.getenv("MODEL_NAME", "inception/mercury-2:nitro")
SUBPROCESS_TIMEOUT = 30
TUI_TIMEOUT = 30
