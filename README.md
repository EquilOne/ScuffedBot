# ScuffedBot 🤖

ScuffedBot is a professional-grade Python-based AI agent powered by the **OpenRouter API**. It provides a versatile interface for interacting with various LLMs, featuring both a high-fidelity CLI and an experimental TUI.

## 🚀 Features

- **Async API Interaction**: Built with `openai`'s async client for high-performance communication with OpenRouter.
- **Rich CLI Experience**:
  - Beautifully formatted output using the `rich` library.
  - Detailed **Token Usage Tables** (Prompt, Response, and Reasoning tokens).
  - Live status spinners and model information.
- **Experimental TUI**: An interactive, terminal-based user interface built with `textual` for persistent chat sessions (WIP).
- **Advanced CLI Arguments**:
  - `verbose`: Show detailed token counts and model metadata.
  - `debug`: Inspect raw API response objects.
  - `dry-run`: Test logic without consuming API credits.
  - `one-shot`: Quick single-prompt execution.

## 🛠 Tech Stack

- **Language**: Python 3.13+
- **API**: [OpenRouter](https://openrouter.ai/)
- **CLI/Formatting**: `rich`
- **TUI Framework**: `textual`
- **Package Management**: `uv`
- **Environment**: `python-dotenv`

## 📦 Installation

This project uses `uv` for lightning-fast dependency management.

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/ScuffedBot.git
   cd ScuffedBot
   ```

2. **Install dependencies**:
   ```bash
   uv sync
   ```

## ⚙️ Setup

Before running the bot, you must configure your OpenRouter API key.

1. Create a `.env` file in the project root:
   ```bash
   touch .env
   ```

2. Add your API key to the `.env` file:
   ```env
   OPENROUTER_API_KEY=your_openrouter_api_key_here
   ```

## 🖥 Usage

### CLI Mode (Recommended)
Run a quick prompt directly from your terminal:
```bash
uv run main.py "Explain quantum entanglement in 2 sentences."
```

**Available Flags:**
- `-v`, `--verbose`: Show token usage and model information.
- `-d`, `--debug`: Print internal arguments and raw JSON response.
- `-n`, `--dry-run`: Skip the API call (useful for testing CLI logic).
- `-O`, `--one-shot`: Run without the ScuffedBot intro greeting.

### TUI Mode (Experimental)
Launch the interactive terminal interface:
```bash
uv run input.py
```
*Note: The TUI is currently a work-in-progress and may have limited functionality compared to the CLI.*

## ⚖️ License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.
