# ScuffedBot 🤖

ScuffedBot is a Python-based AI coding agent powered by the **OpenRouter API**. It can read files, list directories, write files, and execute Python scripts via LLM function calling. Features both a TUI (default) and a CLI one-shot mode.

## 🚀 Features

- **Function-Calling Agent**: The model can read files, list directories, write files, and run Python scripts — all within a secure path-scoped sandbox.
- **Interactive TUI** (default): Persistent chat session with Enter-to-submit, `/clear` command, and live loading indicator.
- **CLI One-Shot Mode**: Quick single-prompt execution for scripting and automation.
- **Rich CLI Output**: Token usage tables, model information, live status spinners, and debug views.
- **Async by Default**: Built on `openai`'s async client for non-blocking API communication.
- **Configurable Model**: Set via `MODEL_NAME` environment variable (defaults to `inception/mercury-2:nitro`).

## 🛠 Tech Stack

- **Language**: Python 3.13+
- **API**: [OpenRouter](https://openrouter.ai/)
- **CLI/Formatting**: `rich`
- **TUI Framework**: `textual`
- **Package Management**: `uv`
- **Environment**: `python-dotenv`

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/ScuffedBot.git
cd ScuffedBot

# Install dependencies
uv sync
```

## ⚙️ Setup

Create a `.env` file in the project root with your OpenRouter API key:

```env
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

Optionally override the model:

```env
MODEL_NAME=openai/gpt-4o
```

## 🖥 Usage

### TUI Mode (Default)
Launch the interactive chat interface:

```bash
uv run main.py
```

Type your message and press Enter. Shift+Enter inserts a newline. Type `/clear` to reset the conversation. The model can read files, list directories, write files, and run Python code as needed.

### CLI One-Shot Mode
Run a single prompt and exit:

```bash
uv run main.py -o "List the files in the calculator directory"
```

**Available Flags:**
| Flag                | Description                                       |
| ------------------- | ------------------------------------------------- |
| `-o`, `--one-shot`  | Run in CLI one-shot mode (default: TUI)           |
| `-v`, `--verbose`   | Show token usage and model information            |
| `-d`, `--debug`     | Print internal arguments and raw JSON response    |
| `-n`, `--dry-run`   | Skip the API call (useful for testing)            |

## 📁 Project Structure

```
call_function.py   — Function dispatch hub (routes tool calls to implementations)
config.py          — Centralized configuration (model, timeouts, paths)
custom_args.py     — CLI argument parsing
functions/         — Tool implementations (read, write, list, run)
input.py           — Textual TUI chat interface
main.py            — CLI entrypoint + one-shot agent loop
prompts.py         — System prompt for the AI model
response.py        — OpenRouter API interaction
```

## 📄 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.