import math

import pytest
from hypothesis import assume, given
from hypothesis import strategies as st

import boiling_point_converter.utils as utils
from boiling_point_converter.utils import (
    SolverMode,
    calculate_pressure_at_temperature,
    calculate_temperature_at_pressure,
    format_output,
    perform_calculation,
)


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
    ]
)
def test_perform_calculation_calls_correct_calculator(mocker, mode):
    mock_pressure = mocker.Mock(return_value=7.3)
    mocker.patch.dict(
        utils._CALCULATORS,
        {mode: mock_pressure}
    )
    result = perform_calculation(mode, 760, 100, 10, 40.65)
    assert result == 7.3
    mock_pressure.assert_called_once_with(760, 100, 10, 40.65)


def test_perform_calculation_with_invalid_solver_raises_error():
    with pytest.raises(ValueError):
        perform_calculation("Invalid Mode", 760, 100, 10, 40.65)


def test_format_output():
    mode = SolverMode.PRESSURE
    p1 = 760
    t1 = 100
    at_value = 10
    dh_vap = 40.65
    calculation_result = perform_calculation(mode, p1, t1, at_value, dh_vap)
    result = format_output(mode, p1, t1, at_value, calculation_result, dh_vap)

    assert "40.65 kJ/mol" in result
    assert "760.00 torr" in result
    assert "100.00 °C" in result
    assert "10.00 torr" in result
    assert "7.30 °C" in result
