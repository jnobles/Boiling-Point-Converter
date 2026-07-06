from textual.app import ComposeResult
from textual.containers import VerticalGroup
from textual.widgets import Input, Static


class LabeledInput(VerticalGroup):
    DEFAULT_CSS = """
    LabeledInput > Static {
        margin: 0 1;
    }
    """

    def __init__(
        self,
        label: str,
        input_id: str,
        *,
        label_kwargs: dict | None = None,
        **input_kwargs,
    ):
        super().__init__()
        self.label = label
        self.input_id = input_id
        self.label_kwargs = label_kwargs or {}
        self.input_kwargs = input_kwargs
        self.Static: Static

    def compose(self) -> ComposeResult:
        yield Static(self.label, **self.label_kwargs)
        yield Input(id=self.input_id, **self.input_kwargs)
