import pytest

from boiling_point_converter.core.calculation import (
    InvalidPhysicalProperty,
    _validate_temperature,
    _validate_pressure,
    _validate_heat_of_vaporization,
)


@pytest.mark.parametrize(
    "value",
    [
        0,
        -1,
    ],
)
def test_pressure_rejects_non_positive(value):
    with pytest.raises(InvalidPhysicalProperty) as e_info:
        _validate_pressure(value)
    assert "Pressure must be greater than zero" in str(e_info.value)

@pytest.mark.parametrize(
    "value",
    [
        0.5,
        1,
        1e5,
    ],
)
def test_pressure_accepts_positive(value):
    _validate_pressure(value)

@pytest.mark.parametrize(
    "value",
    [
        -273.15,
        -300,
    ],
)
def test_temperature_reject_absolute_zero_and_below(value):
    with pytest.raises(InvalidPhysicalProperty) as e_info:
        _validate_temperature(value)
    assert "Temperature must be greater than absolute zero" in str(e_info.value)

@pytest.mark.parametrize(
    "value",
    [
        -273.14,
        -1,
        0,
        1,
    ],
)
def test_temperature_accepts_greater_than_absolute_zero(value):
    _validate_temperature(value)


@pytest.mark.parametrize(
    "value",
    [
        -1,
        0,
    ]
)
def test_heat_of_vaporization_rejects_negative(value):
    with pytest.raises(InvalidPhysicalProperty) as e_info:
        _validate_heat_of_vaporization(value)
    assert "Heat of vaporization must be greater than zero" in str(e_info.value)

@pytest.mark.parametrize(
    "value",
    [
        1,
    ],
)
def test_heat_of_vaporization_accepts_positive(value):
    _validate_heat_of_vaporization(value)
