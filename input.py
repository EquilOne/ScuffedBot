import asyncio

from openai.types.responses import EasyInputMessage
from openai.types.responses.response_function_tool_call import ResponseFunctionToolCall
from textual.app import App, ComposeResult
from textual.message import Message
from textual.widgets import Footer, Header, LoadingIndicator, RichLog, TextArea

from call_function import call_function
from config import MAX_ITERATIONS, TUI_TIMEOUT
from response import get_response


class ChatInput(TextArea):
    class Submitted(Message):
        def __init__(self, text: str) -> None:
            super().__init__()
            self.text = text

    def action_submit(self) -> None:
        text = self.text.strip()
        if text:
            self.post_message(self.Submitted(text))
            self.clear()

    async def _on_key(self, event) -> None:
        if event.key == "shift+enter":
            event.stop()
            self.insert("\n")
        elif event.key == "enter":
            event.prevent_default()
            self.action_submit()


class ChatInputApp(App):
    CSS = """
    ChatInput {
        height: 5;
        dock: bottom;
        border: tall $primary;
    }
    RichLog {
        height: 1fr;
        border: tall $surface;
    }
    LoadingIndicator {
        height: 1;
        dock: bottom;
        layer: top;
        display: none;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header()
        yield LoadingIndicator()
        yield RichLog(id="log", markup=True, wrap=True, auto_scroll=True)
        yield ChatInput(id="chat", placeholder="Type your message here...")
        yield Footer()

    def on_mount(self) -> None:
        self.history: list = []
        log = self.query_one("#log", RichLog)
        log.write("[bold cyan]ScuffedBot[/bold cyan] - AI coding agent")
        log.write(
            "[dim]Type your message and press Enter. Shift+Enter for newline. "
            "Type /clear to reset conversation.[/dim]"
        )
        log.write("")
        self.query_one(ChatInput).focus()

    async def on_chat_input_submitted(self, message: ChatInput.Submitted) -> None:
        text = message.text.strip()

        if text.lower() == "/clear":
            self.history = []
            log = self.query_one("#log", RichLog)
            log.clear()
            log.write("[yellow]Conversation cleared.[/yellow]")
            return

        loader = self.query_one(LoadingIndicator)
        loader.display = True
        log = self.query_one("#log", RichLog)
        chat = self.query_one("#chat", ChatInput)

        chat.disabled = True
        log.write(f"[bold rose]You:[/bold rose] {message.text}")

        history_len = len(self.history)
        self.history.append({"role": "user", "content": message.text})

        try:
            for _ in range(MAX_ITERATIONS):
                resp = await asyncio.wait_for(
                    get_response(self.history),
                    timeout=TUI_TIMEOUT,
                )

                if resp.status == "failed" or resp.error:
                    log.write(
                        f"[bold red]Error:[/bold red] API call failed: {resp.error}"
                    )
                    while len(self.history) > history_len:
                        self.history.pop()
                    return

                function_calls = [
                    item
                    for item in resp.output
                    if isinstance(item, ResponseFunctionToolCall)
                ]

                if not function_calls:
                    output_text = resp.output_text or ""
                    log.write(f"[bold rose]Assistant:[/bold rose] {output_text}")
                    self.history.append({"role": "assistant", "content": output_text})
                    return

                self.history.append(
                    EasyInputMessage(role="assistant", content=resp.output_text or "")
                )
                self.history.extend(function_calls)

                for call in function_calls:
                    log.write(f"[dim]Calling: {call.name}(...)[/dim]")
                    call_result = call_function(call)
                    self.history.append(call_result)

            log.write(
                "[yellow]Warning: max iterations reached. "
                "Response may be incomplete.[/yellow]"
            )

        except asyncio.TimeoutError:
            log.write(
                f"[bold red]Error:[/bold red] Request timed out after "
                f"{TUI_TIMEOUT} seconds"
            )
            while len(self.history) > history_len:
                self.history.pop()
        except Exception as e:
            log.write(f"[bold red]Error:[/bold red] {e}")
            while len(self.history) > history_len:
                self.history.pop()
        finally:
            loader.display = False
            chat.disabled = False
            chat.focus()
