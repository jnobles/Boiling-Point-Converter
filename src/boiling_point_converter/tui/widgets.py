"""Reusable custom Textual widgets.

Contains composite widgets used to encapsulate and standardize
common layout patterns.
"""

from textual.app import ComposeResult
from textual.containers import VerticalGroup
from textual.widgets import Input, Static


class LabeledInput(VerticalGroup):
    """
    A vertically stacked label and input field.

    Combines a `Static` widget with an `Input` widget to create a top-side
    labeled input.  Any arguments not consumed by the constructor are
    forwarded to the created `Input` widget.

    :param label: The text to display above the input field.
    :param input_id: Widget identifier to assign to the contained
        ``Input`` widget.
    :param label_kwargs: Optional arguments to forward to the contained
        ``Static`` widget.
    :param input_kwargs: Optional arguments to forward to the contained
        ``Input`` widget.
    """

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
