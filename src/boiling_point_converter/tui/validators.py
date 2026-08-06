"""Validation classes for numeric inputs.

Provides validators for Textual ``Input`` widgets.  The validators ensure
that the values are numeric and meet the expected physical constraints.

"""

from abc import ABC, abstractmethod

from textual.validation import ValidationResult, Validator

from boiling_point_converter.core.constants import KELVIN_CELSIUS_OFFSET


class FloatValidator(Validator, ABC):
    """Validate numeric input with subclass-defined constraints.

    Attempts to parse the supplied value as a valid float before delegating
    additional checks to :meth:`validate_number`.

    :param field_name: The field name to reference when creating
        validation error messages.
    """

    def __init__(self, field_name: str):
        super().__init__()
        self.field_name = field_name

    def validate(self, value: str) -> ValidationResult:
        """Validate a string entered into an ``Input`` widget.

        Empty values and values that cannot be parsed as a ``float`` are
        rejected before attempting to call :meth:`validate_number` to
        apply any additional constraints.

        :param value: The string to validate
        :returns: A :class:`~textual.validation.ValidationResult`
            describing whether or not the supplied value is valid.
        """

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
    def validate_number(self, number: float) -> str | None:
        """Validate a parsed numeric value.

        :param number: The passed floating-point value.
        :returns: The validation error message if validation fails,
        otherwise ``None``.
        """

        ...


class PressureValidator(FloatValidator):
    """Validate that a pressure is strictly positive."""

    def __init__(self):
        super().__init__(field_name="Pressure")

    def validate_number(self, number: float) -> str | None:
        if number <= 0:
            return "Pressure must be greater than zero."


class TemperatureValidator(FloatValidator):
    """Validate that a temperature is above absolute zero.

    Passed temperatures are interpreted as degrees Celsius.
    """

    def __init__(self):
        super().__init__(field_name="Temperature")

    def validate_number(self, number: float) -> str | None:
        if number <= -KELVIN_CELSIUS_OFFSET:
            return "Temperature must be greater than absolute zero."


class HeatOfVaporizationValidator(FloatValidator):
    """Validate that a molar heat of vaporization is greater than zero."""

    def __init__(self):
        super().__init__(field_name="Heat of Vaporization")

    def validate_number(self, number: float) -> str | None:
        if number < 0:
            return "Heat of vaporization must be greater than zero."
