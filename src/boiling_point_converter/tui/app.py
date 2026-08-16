from importlib.resources import files

from textual import on
from textual.app import App, Binding, ComposeResult
from textual.containers import Grid, Vertical
from textual.validation import (
    ValidationResult,
    Validator,
)
from textual.widgets import (
    Button,
    Footer,
    Header,
    Input,
    Label,
    OptionList,
    RadioButton,
    RadioSet,
)
from textual.widgets.option_list import Option

from boiling_point_converter.core.calculation import (
    InvalidPhysicalProperty,
    perform_calculation,
)
from boiling_point_converter.core.molar_heat_of_vaporization import (
    REFERENCE_HEATS_OF_VAPORIZATION,
    REFERENCE_HEATS_OF_VAPORIZATION_BY_COMPOUND,
)
from boiling_point_converter.tui.formatting import (
    format_output,
)
from boiling_point_converter.tui.widgets import LabeledInput


class FloatValidator(Validator):
    def __init__(self, field_name: str):
        super().__init__()
        self.field_name = field_name

    def validate(self, value: str) -> ValidationResult:
        if value == "":
            return self.failure(f"{self.field_name} required.")

        try:
            float(value)
        except ValueError:
            return self.failure(f"{self.field_name} must be numeric.")

        return self.success()


class BoilingPointConverterApp(App):
    BINDINGS = [Binding("ctrl+q", "quit", "Quit", show=True, priority=True)]

    CSS_PATH = files(__package__).joinpath("styles.tcss")

    p1_input: Input
    t1_input: Input
    at_value_input: Input
    solver_mode_radioset: RadioSet
    dh_vap_input: Input
    dh_vap_option_list: OptionList
    result_label: Label

    @on(OptionList.OptionSelected)
    def update_dh_vap(self, event: OptionList.OptionSelected) -> None:
        if event.option.id == "custom-dHvap":
            self.dh_vap_input.disabled = False
            self.dh_vap_input.value = ""
        else:
            self.dh_vap_input.value = str(
                REFERENCE_HEATS_OF_VAPORIZATION_BY_COMPOUND[event.option_id]
            )
            self.dh_vap_input.disabled = True

    @on(Button.Pressed, "#calculate")
    def calculate(self, event: Button.Pressed) -> None:
        if not all([item.is_valid for item in self.query(Input)]):
            for item in self.query(Input):
                if not item.is_valid:
                    self.notify(
                        "\n".join(item.validate(item.value).failure_descriptions)
                    )
            return

        try:
            p1 = float(self.p1_input.value)
            t1 = float(self.t1_input.value)
            dh_vap = float(self.dh_vap_input.value)
            at_value = float(self.at_value_input.value)
            mode = self.solver_mode_radioset.pressed_button.id
            result = perform_calculation(mode, p1, t1, at_value, dh_vap)
        except InvalidPhysicalProperty as e:
            self.notify(str(e))
        else:
            self.result_label.update(
                format_output(mode, p1, t1, at_value, result, dh_vap)
            )

    @on(RadioSet.Changed, "#solver-mode")
    def update_solver_mode(self, event: RadioSet.Changed) -> None:
        if event.pressed.id == "pressure":
            self.at_value_input.value = ""
            self.at_value_input.placeholder = "torr"
            self.at_value_input.validators = [FloatValidator("Pressure")]
        elif event.pressed.id == "temperature":
            self.at_value_input.value = ""
            self.at_value_input.placeholder = "\u00b0C"
            self.at_value_input.validators = [FloatValidator("Temperature")]

    def compose(self) -> ComposeResult:
        option_list = []
        for item in REFERENCE_HEATS_OF_VAPORIZATION:
            option_list.append(Option(item.compound, id=item.compound))
        option_list.append(None)
        option_list.append(
            Option("** Custom Heat of Vaporization **", id="custom-dHvap")
        )

        yield Header()
        yield Footer()
        with Grid(id="input-grid"):
            yield LabeledInput(
                "Enter the pressure of the known boiling point:",
                input_id="p1",
                placeholder="torr",
                type="number",
                validators=[FloatValidator("Pressure")],
            )
            yield LabeledInput(
                "Enter the boiling point at this pressure:",
                input_id="t1",
                placeholder="\u00b0C",
                type="number",
                validators=[FloatValidator("Temperature")],
            )
            with Vertical():
                with RadioSet(id="solver-mode"):
                    yield RadioButton("At pressure:", id="pressure", value=True)
                    yield RadioButton("At temperature:", id="temperature")
                yield Input(
                    id="at-value",
                    placeholder="torr",
                    type="number",
                    validators=[FloatValidator("Pressure")],
                )
            yield Button("Calculate", id="calculate")
            yield Label(id="result")
        with Vertical(id="right-div"):
            yield LabeledInput(
                label="Heat of Vaporization",
                input_id="dHvap",
                placeholder="\u0394H vap (kJ/mol)",
                type="number",
                validators=[FloatValidator("Heat of Vaporization")],
                disabled=True,
            )
            yield OptionList(*option_list, id="dHvap-selection")

    def on_mount(self) -> None:
        self.p1_input = self.query_one("#p1", Input)
        self.t1_input = self.query_one("#t1", Input)
        self.at_value_input = self.query_one("#at-value", Input)
        self.solver_mode_radioset = self.query_one("#solver-mode", RadioSet)
        self.dh_vap_input = self.query_one("#dHvap", Input)
        self.dh_vap_option_list = self.query_one("#dHvap-selection", OptionList)
        self.result_label = self.query_one("#result", Label)

        self.p1_input.focus()

        self.dh_vap_option_list.highlighted = self.dh_vap_option_list.get_option_index(
            "water"
        )
        self.dh_vap_input.value = str(
            REFERENCE_HEATS_OF_VAPORIZATION_BY_COMPOUND[
                self.dh_vap_option_list.highlighted_option.id
            ]
        )
