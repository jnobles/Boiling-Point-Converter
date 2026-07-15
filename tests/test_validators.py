import pytest

from boiling_point_converter.validators import (
    FloatValidator,
    HeatOfVaporizationValidator,
    PressureValidator,
    TemperatureValidator,
)


class TestFloatValidator:
    class MinimalValidator(FloatValidator):
        def validate_number(self, number: float) -> str | None:
            return None

    validator = MinimalValidator("Value")

    def test_float_validator_rejects_empty(self):
        result = self.validator.validate("")

        assert result.is_valid is False
        assert result.failure_descriptions == ["Value required."]

    def test_float_validator_rejects_non_numeric(self):
        result = self.validator.validate("abc")

        assert result.is_valid is False
        assert result.failure_descriptions == ["Value must be numeric."]

    @pytest.mark.parametrize(
        "value",
        [
            "-1",
            "0",
            "1",
            "1.5",
            "1e5",
        ],
    )
    def test_float_accepts_numeric_values(self, value):
        result = self.validator.validate(value)

        assert result.is_valid is True
        assert result.failure_descriptions == []


class TestPressureValidator:
    validator = PressureValidator()

    def test_pressure_field_name(self):
        assert self.validator.field_name == "Pressure"

    @pytest.mark.parametrize(
        "value",
        [
            "0",
            "-1",
        ],
    )
    def test_pressure_rejects_non_positive(self, value):
        result = self.validator.validate(value)

        assert result.is_valid is False
        assert result.failure_descriptions == ["Pressure must be greater than zero."]

    @pytest.mark.parametrize(
        "value",
        [
            "0.5",
            "1",
            "1e5",
        ],
    )
    def test_pressure_accepts_positive(self, value):
        result = self.validator.validate(value)

        assert result.is_valid is True
        assert result.failure_descriptions == []


class TestTemperatureValidator:
    validator = TemperatureValidator()

    def test_temperature_field_name(self):
        assert self.validator.field_name == "Temperature"

    @pytest.mark.parametrize(
        "value",
        [
            "-273.15",
            "-300",
        ],
    )
    def test_temperature_reject_below_absolute_zero_and_below(self, value):
        result = self.validator.validate(value)

        assert result.is_valid is False
        assert result.failure_descriptions == [
            "Temperature must be greater than absolute zero."
        ]

    @pytest.mark.parametrize(
        "value",
        [
            "-273.14",
            "-1",
            "0",
            "1",
        ],
    )
    def test_temperature_accepts_greater_than_absolute_zero(self, value):
        result = self.validator.validate(value)

        assert result.is_valid is True
        assert result.failure_descriptions == []


class TestHeatOfVaporizationValidator:
    validator = HeatOfVaporizationValidator()

    def test_heat_of_vaporization_field_name(self):
        assert self.validator.field_name == "Heat of Vaporization"

    @pytest.mark.parametrize("value", ["-1"])
    def test_heat_of_vaporization_rejects_negative(self, value):
        result = self.validator.validate(value)

        assert result.is_valid is False
        assert result.failure_descriptions == [
            "Heat of vaporization must be greater than zero."
        ]

    @pytest.mark.parametrize(
        "value",
        [
            "0",
            "1",
        ],
    )
    def test_heat_of_vaporization_accepts_positive(self, value):
        result = self.validator.validate(value)

        assert result.is_valid is True
        assert result.failure_descriptions == []
