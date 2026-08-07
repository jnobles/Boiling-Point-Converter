import math

import pytest
from hypothesis import assume, given
from hypothesis import strategies as st

from boiling_point_converter.core import calculation
from boiling_point_converter.core.calculation import (
    calculate_pressure_at_temperature,
    calculate_temperature_at_pressure,
    perform_calculation,
)
from boiling_point_converter.core.models import SolverMode


@given(t1=st.floats(1, 200), t2=st.floats(1, 200))
def test_calculate_pressure_monotonic(t1, t2):
    assume(t2 > t1)

    p1 = calculate_pressure_at_temperature(760, 100, t1, 40.65)
    p2 = calculate_pressure_at_temperature(760, 100, t2, 40.65)

    assert p2 > p1 or math.isclose(p1, p2)


@given(p1=st.floats(1, 200), p2=st.floats(1, 200))
def test_calculate_temperature_monotonic(p1, p2):
    assume(p2 > p1)

    t1 = calculate_temperature_at_pressure(760, 100, p1, 40.65)
    t2 = calculate_temperature_at_pressure(760, 100, p2, 40.65)

    assert t2 > t1 or math.isclose(t1, t2)


@given(t1=st.floats(1, 200), p1=st.floats(1, 200), t2=st.floats(1, 200))
def test_round_trip_calculation(t1, p1, t2):
    p2 = calculate_pressure_at_temperature(p1, t1, t2, 40.65)
    result = calculate_temperature_at_pressure(p1, t1, p2, 40.65)

    assert t2 == pytest.approx(result)


def test_same_pressure_returns_same_temperature():
    result = calculate_temperature_at_pressure(760, 100, 760, 40.65)

    assert result == pytest.approx(100)


def test_same_temperature_returns_same_pressure():
    result = calculate_pressure_at_temperature(760, 100, 100, 40.65)

    assert result == pytest.approx(760)


@pytest.mark.parametrize(
    "mode",
    [
        SolverMode.PRESSURE,
        SolverMode.TEMPERATURE,
    ],
)
def test_perform_calculation_calls_correct_calculator(mocker, mode):
    mock_pressure = mocker.Mock(return_value=7.3)
    mocker.patch.dict(calculation._CALCULATORS, {mode: mock_pressure})
    result = perform_calculation(mode, 760, 100, 10, 40.65)
    assert result == 7.3
    mock_pressure.assert_called_once_with(760, 100, 10, 40.65)


def test_perform_calculation_with_invalid_solver_raises_error():
    with pytest.raises(ValueError):
        perform_calculation("Invalid Mode", 760, 100, 10, 40.65)
