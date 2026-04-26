# AGENTS.md - ScuffedBot Development Guidelines

## Project Overview
A Python-based AI agent using OpenRouter API, `rich` for CLI output, and `textual` for an experimental TUI.

## Developer Commands
- **Run CLI**: `uv run main.py "your prompt"`
- **Run TUI**: `uv run input.py`
- **Install dependencies**: `uv sync`

## Environment Setup
- Create a `.env` file with `OPENROUTER_API_KEY`.
- API calls are routed through `https://openrouter.ai/api/v1`.

## High-Signal Quirks
- **Entrypoints**: `main.py` is the primary CLI entrypoint. `input.py` is the Textual TUI.
- **Async Flow**: `main.py` and `input.py` are fully async.
- **API Model**: Defaults to `openrouter/free` in `response.py`.
- **CLI Flags**: 
  - `-v`, `--verbose`: Show token usage and model info.
  - `-d`, `--debug`: Print internal args and raw response.
  - `-n`, `--dry-run`: Skip the API call.
  - `-o`, `--one-shot`: Disable "ScuffedBot" intro greeting.

## Communication Modes
- **Caveman Mode**: Ultra-compressed technical communication.
- **Caveman Commit**: Terse, exact conventional commits.
- **Caveman Review**: High-signal, noise-free code review.

## Architecture
- `response.py`: Core logic for API interaction.
- `custom_args.py`: Argument parsing for `main.py`.
- `input.py`: Functional Textual TUI with chat history and LoadingIndicator.