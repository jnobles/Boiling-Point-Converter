from abc import ABC, abstractmethod

from textual.validation import ValidationResult, Validator

from .constants import K


class FloatValidator(Validator, ABC):
    def __init__(self, field_name: str):
        super().__init__()
        self.field_name = field_name

    def validate(self, value: str) -> ValidationResult:
        if value == "":
            return self.failure(f"{self.field_name} required.")

        try:
            number = float(value)
        except ValueError:
            return self.failure(f"{self.field_name} must be numeric.")

        error = self.validate_number(number)

        if error is not None:
            return self.failure(error)
        return self.success()

    @abstractmethod
    def validate_number(self, number: float) -> str | None: ...


class PressureValidator(FloatValidator):
    def __init__(self):
        super().__init__(field_name="Pressure")

    def validate_number(self, number: float) -> str | None:
        if number <= 0:
            return "Pressure cannot be negative."


class TemperatureValidator(FloatValidator):
    def __init__(self):
        super().__init__(field_name="Temperature")

    def validate_number(self, number: float) -> str | None:
        if number < -K:
            return "Temperature cannot be below absolute zero."


class HeatOfVaporizationValidator(FloatValidator):
    def __init__(self):
        super().__init__(field_name="Heat of Vaporization")

    def validate_number(self, number: float) -> str | None:
        if number < 0:
            return "Heat of vaporization cannot be negative."
