from importlib.resources import files

from textual import on
from textual.app import App, Binding, ComposeResult
from textual.containers import Grid, Vertical
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

from .molar_heat_of_vaporization import REFERENCE_HEATS_OF_VAPORIZATION
from .utils import (
    calculate_pressure_at_temperature,
    calculate_temperature_at_pressure,
    format_output,
)
from .validators import (
    HeatOfVaporizationValidator,
    PressureValidator,
    TemperatureValidator,
)
from .widgets import LabeledInput


class BoilingPointConverterApp(App):
    BINDINGS = [Binding("ctrl+q", "quit", "Quit", show=True, priority=True)]

    CSS_PATH = files("boiling_point_converter").joinpath("styles.tcss")

    p1_input: Input
    t1_input: Input
    at_value_input: Input
    solver_mode_radioset: RadioSet
    dh_vap_input: Input
    dh_vap_option_list: OptionList
    result_label: Label

    @on(OptionList.OptionSelected)
    def update_dh_vap(self, event: OptionList.OptionHighlighted) -> None:
        if event.option.prompt == "** Custom Heat of Vaporization **":
            self.dh_vap_input.disabled = False
            self.dh_vap_input.value = ""
        else:
            self.dh_vap_input.value = event.option_id
            self.dh_vap_input.disabled = True

    @on(Button.Pressed, "#calculate")
    def calculate(self, event: Button.Pressed) -> None:
        failing_validation = False
        for item in self.query(Input):
            response = item.validate(item.value)
            if not item.is_valid:
                self.notify("\n".join(response.failure_descriptions))
                failing_validation = True

        if failing_validation:
            return

        p1 = float(self.p1_input.value)
        t1 = float(self.t1_input.value)
        dh_vap = float(self.dh_vap_input.value)
        at_value = float(self.at_value_input.value)
        mode = self.solver_mode_radioset.pressed_button.id
        if mode == "pressure":
            result = calculate_temperature_at_pressure(p1, t1, at_value, dh_vap)
            self.result_label.update(format_output(p1, t1, at_value, result, dh_vap))
        elif mode == "temperature":
            result = calculate_pressure_at_temperature(p1, t1, at_value, dh_vap)
            self.result_label.update(format_output(p1, t1, result, at_value, dh_vap))

    @on(RadioSet.Changed, "#solver-mode")
    def update_solver_mode(self, event: RadioSet.Changed) -> None:
        if event.pressed.id == "pressure":
            self.at_value_input.value = ""
            self.at_value_input.placeholder = "torr"
            self.at_value_input.validators = [PressureValidator()]
        elif event.pressed.id == "temperature":
            self.at_value_input.value = ""
            self.at_value_input.placeholder = "\u00b0C"
            self.at_value_input.validators = [TemperatureValidator()]

    def compose(self) -> ComposeResult:
        option_list = []
        for item in REFERENCE_HEATS_OF_VAPORIZATION:
            option_list.append(Option(item.compound, id=str(item.dh_vap_kj_per_mol)))
        option_list.append(None)
        option_list.append(Option("** Custom Heat of Vaporization **"))

        yield Header()
        yield Footer()
        with Grid(id="input-grid"):
            yield LabeledInput(
                "Enter the pressure of the known boiling point:",
                input_id="p1",
                placeholder="torr",
                type="number",
                validators=[PressureValidator()],
            )
            yield LabeledInput(
                "Enter the boiling point at this pressure:",
                input_id="t1",
                placeholder="\u00b0C",
                type="number",
                validators=[TemperatureValidator()],
            )
            with Vertical():
                with RadioSet(id="solver-mode"):
                    yield RadioButton("At pressure:", id="pressure", value=True)
                    yield RadioButton("At temperature:", id="temperature")
                yield Input(
                    id="at-value",
                    placeholder="torr",
                    type="number",
                    validators=[PressureValidator()],
                )
            yield Button("Calculate", id="calculate")
            yield Label(id="result")
        with Vertical(id="right-div"):
            yield LabeledInput(
                label="Heat of Vaporization",
                input_id="dHvap",
                placeholder="\u0394H vap (kJ/mol)",
                type="number",
                validators=[HeatOfVaporizationValidator()],
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

        water_index = next(
            i
            for i, option in enumerate(self.dh_vap_option_list.options)
            if "water" in option.prompt.lower()
        )
        self.dh_vap_option_list.highlighted = water_index
        self.dh_vap_input.value = self.dh_vap_option_list.highlighted_option.id
