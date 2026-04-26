from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.message import Message
from textual.widgets import Footer, Header, RichLog, TextArea

from response import get_response


class ChatInput(TextArea):
    class Submitted(Message):
        def __init__(self, text: str) -> None:
            super().__init__()
            self.text = text

    BINDINGS = [
        Binding("enter", "submit", "Submit", show=False),
    ]

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
        height: 5;           /* input box height */
        dock: bottom;        /* pin to bottom */
        border: tall $primary;
    }
    RichLog {
        height: 1fr;         /* takes remaining space */
        border: tall $surface;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header()
        yield RichLog(id="log", markup=True, wrap=True)
        yield ChatInput(id="chat", placeholder="Type your message here...")
        yield Footer()

    def on_mount(self) -> None:
        self.query_one(ChatInput).focus()

    async def on_chat_input_submitted(self, message: ChatInput.Submitted) -> None:
        log = self.query_one("#log", RichLog)
        log.write(f"[bold rose]You:[/bold rose] {message.text}")

        resp = await get_response()
        log.write(f"[bold rose]Assistant:[/bold rose] {resp}")


ChatInputApp().run()
