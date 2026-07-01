# AGENTS.md - ScuffedBot Development Guidelines

## Project Overview
A Python-based AI agent using OpenRouter API, `rich` for CLI output, and `textual` for a TUI.

## Developer Commands
- **Run TUI (default)**: `uv run main.py`
- **Run CLI one-shot**: `uv run main.py -o "your prompt"`
- **Install dependencies**: `uv sync`

## Environment Setup
- Create a `.env` file with `OPENROUTER_API_KEY`.
- API calls are routed through `https://openrouter.ai/api/v1`.

## High-Signal Quirks
- **Entrypoints**: `main.py` is the CLI entrypoint (default: TUI). Pass `-o` for one-shot mode. `input.py` is the Textual TUI module (imported by `main.py`).
- **Async Flow**: `main.py` and `input.py` are fully async.
- **API Model**: Defaults to `inception/mercury-2:nitro` in `config.py`. Override via `MODEL_NAME` env var.
- **CLI Flags**: 
  - `-v`, `--verbose`: Show token usage and model info.
  - `-d`, `--debug`: Print internal args and raw response.
  - `-n`, `--dry-run`: Skip the API call.
  - `-o`, `--one-shot`: Run in CLI one-shot mode (default: TUI).
- **Function Sandbox**: All tool operations are scoped to the working directory. Path traversal and symlink escapes are blocked.

## Communication Modes
- **Caveman Mode**: Ultra-compressed technical communication.
- **Caveman Commit**: Terse, exact conventional commits.
- **Caveman Review**: High-signal, noise-free code review.

## Architecture
- `response.py`: Core logic for API interaction.
- `custom_args.py`: Argument parsing for `main.py`.
- `input.py`: Functional Textual TUI with chat history and LoadingIndicator.