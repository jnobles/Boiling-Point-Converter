from boiling_point_converter.core.models import SolverMode
from boiling_point_converter.tui.formatting import format_output


def test_format_output():
    mode = SolverMode.PRESSURE
    p1 = 760
    t1 = 100
    at_value = 10
    calculation_result = 7.3
    dh_vap = 40.65
    result = format_output(mode, p1, t1, at_value, calculation_result, dh_vap)

    assert "40.65 kJ/mol" in result
    assert "760.00 torr" in result
    assert "100.00 °C" in result
    assert "10.00 torr" in result
    assert "7.30 °C" in result
