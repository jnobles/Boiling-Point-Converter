import pytest

import boiling_point_converter.core.molar_heat_of_vaporization
import boiling_point_converter.utils as bp_utils
from boiling_point_converter.tui.app import BoilingPointConverterApp
from boiling_point_converter.utils import SolverMode


@pytest.mark.asyncio
async def test_keyboard_workflow_basic():
    app = BoilingPointConverterApp()
    async with app.run_test() as pilot:
        known_pressure = "760"
        known_temperature = "100"
        target_pressure = "10"
        dh_vap = app.query_one("#dHvap").value

        await pilot.press(*known_pressure)
        await pilot.press("tab")
        await pilot.press(*known_temperature)
        await pilot.press("tab")
        await pilot.press("tab")
        await pilot.press(*target_pressure)
        await pilot.press("tab")
        await pilot.press("enter")
        await pilot.pause()

        target_temperature = bp_utils.calculate_temperature_at_pressure(
            pressure_torr=float(known_pressure),
            temperature_c=float(known_temperature),
            target_pressure_torr=float(target_pressure),
            dh_vap_kj_per_mol=float(dh_vap),
        )

        expected_result = bp_utils.format_output(
            mode=SolverMode.PRESSURE,
            p1=float(known_pressure),
            t1=float(known_temperature),
            at_value=float(target_pressure),
            result=target_temperature,
            dh_vap=float(dh_vap),
        )

        assert app.query_one("#result").content == expected_result


@pytest.mark.asyncio
async def test_keyboard_workflow_switch_mode():
    app = BoilingPointConverterApp()
    async with app.run_test() as pilot:
        known_pressure = "760"
        known_temperature = "100"
        target_temperature = "10"
        dh_vap = app.query_one("#dHvap").value

        await pilot.press(*known_pressure)
        await pilot.press("tab")
        await pilot.press(*known_temperature)
        await pilot.press("tab")
        await pilot.press("down", "space")
        await pilot.press("tab")
        await pilot.press(*target_temperature)
        await pilot.press("tab")
        await pilot.press("enter")
        await pilot.pause()

        target_pressure = bp_utils.calculate_pressure_at_temperature(
            pressure_torr=float(known_pressure),
            temperature_c=float(known_temperature),
            target_temperature_c=float(target_temperature),
            dh_vap_kj_per_mol=float(dh_vap),
        )

        expected_result = bp_utils.format_output(
            mode=SolverMode.TEMPERATURE,
            p1=float(known_pressure),
            t1=float(known_temperature),
            at_value=float(target_temperature),
            result=target_pressure,
            dh_vap=float(dh_vap),
        )

        assert app.query_one("#result").content == expected_result


@pytest.mark.asyncio
async def test_mouse_workflow_basic():
    app = BoilingPointConverterApp()
    async with app.run_test() as pilot:
        known_pressure = "760"
        known_temperature = "100"
        target_pressure = "10"
        dh_vap = app.query_one("#dHvap").value

        await pilot.click("#p1")
        await pilot.press(*known_pressure)
        await pilot.click("#t1")
        await pilot.press(*known_temperature)
        await pilot.click("#at-value")
        await pilot.press(*target_pressure)
        await pilot.click("#calculate")
        await pilot.pause()

        target_temperature = bp_utils.calculate_temperature_at_pressure(
            pressure_torr=float(known_pressure),
            temperature_c=float(known_temperature),
            target_pressure_torr=float(target_pressure),
            dh_vap_kj_per_mol=float(dh_vap),
        )

        expected_result = bp_utils.format_output(
            mode=SolverMode.PRESSURE,
            p1=float(known_pressure),
            t1=float(known_temperature),
            at_value=float(target_pressure),
            result=float(target_temperature),
            dh_vap=float(dh_vap),
        )

        assert app.query_one("#result").content == expected_result


@pytest.mark.asyncio
async def test_mouse_workflow_switch_mode():
    app = BoilingPointConverterApp()
    async with app.run_test() as pilot:
        known_pressure = "760"
        known_temperature = "100"
        target_temperature = "10"
        dh_vap = app.query_one("#dHvap").value

        await pilot.click("#p1")
        await pilot.press(*known_pressure)
        await pilot.click("#t1")
        await pilot.press(*known_temperature)
        await pilot.click("#solver-mode > #temperature")
        await pilot.click("#at-value")
        await pilot.press(*target_temperature)
        await pilot.click("#calculate")
        await pilot.pause()

        target_pressure = bp_utils.calculate_pressure_at_temperature(
            pressure_torr=float(known_pressure),
            temperature_c=float(known_temperature),
            target_temperature_c=float(target_temperature),
            dh_vap_kj_per_mol=float(dh_vap),
        )

        expected_result = bp_utils.format_output(
            mode=SolverMode.TEMPERATURE,
            p1=float(known_pressure),
            t1=float(known_temperature),
            at_value=float(target_temperature),
            result=float(target_pressure),
            dh_vap=float(dh_vap),
        )

        assert app.query_one("#result").content == expected_result


@pytest.mark.asyncio
async def test_custom_dh_toggles_and_resets_field():
    app = BoilingPointConverterApp()
    async with app.run_test() as pilot:
        option_list = app.query_one("#dHvap-selection")

        option_list.highlighted = option_list.get_option_index("custom-dHvap")
        option_list.action_select()
        await pilot.pause()

        assert not app.query_one("#dHvap").disabled
        assert app.query_one("#dHvap").value == ""

        option_list.highlighted = option_list.get_option_index("water")
        option_list.action_select()
        await pilot.pause()

        assert app.query_one("#dHvap").disabled
        assert app.query_one("#dHvap").value == str(
            boiling_point_converter.core.molar_heat_of_vaporization.REFERENCE_HEATS_OF_VAPORIZATION_BY_COMPOUND[
                "water"
            ]
        )


@pytest.mark.asyncio
async def test_initial_state_defaults():
    app = BoilingPointConverterApp()
    async with app.run_test():
        assert app.focused.id == "p1"
        assert app.query_one("#dHvap-selection").highlighted_option.id == "water"
        assert app.query_one("#dHvap").value == str(
            boiling_point_converter.core.molar_heat_of_vaporization.REFERENCE_HEATS_OF_VAPORIZATION_BY_COMPOUND[
                "water"
            ]
        )


@pytest.mark.asyncio
async def test_custom_dh_used_in_temperature_calculation(mocker):
    known_pressure = "760"
    known_temperature = "100"
    target_pressure = "10"
    dH_vap = "30"

    calculate_perform_calculation = mocker.patch(
        "boiling_point_converter.app.perform_calculation", return_value=20
    )

    app = BoilingPointConverterApp()
    async with app.run_test() as pilot:
        app.query_one("#p1").value = known_pressure
        app.query_one("#t1").value = known_temperature
        app.query_one("#at-value").value = target_pressure
        option_list = app.query_one("#dHvap-selection")
        option_list.highlighted = option_list.get_option_index("custom-dHvap")
        option_list.action_select()
        await pilot.pause()
        app.query_one("#dHvap").value = dH_vap
        await pilot.click("#calculate")

        calculate_perform_calculation.assert_called_once_with(
            "pressure",
            float(known_pressure),
            float(known_temperature),
            float(target_pressure),
            float(dH_vap),
        )


@pytest.mark.asyncio
async def test_custom_dh_used_in_pressure_calculation(mocker):
    known_pressure = "760"
    known_temperature = "100"
    target_temperature = "10"
    dH_vap = "30"

    mock_perform_calculation = mocker.patch(
        "boiling_point_converter.app.perform_calculation", return_value=20
    )

    app = BoilingPointConverterApp()
    async with app.run_test() as pilot:
        app.query_one("#p1").value = known_pressure
        app.query_one("#t1").value = known_temperature
        mode_list = app.query_one("#solver-mode")
        mode_list.pressed_button_id = "pressure"
        app.query_one("#at-value").value = target_temperature
        option_list = app.query_one("#dHvap-selection")
        option_list.highlighted = option_list.get_option_index("custom-dHvap")
        option_list.action_select()
        await pilot.pause()
        app.query_one("#dHvap").value = dH_vap
        await pilot.click("#calculate")

        mock_perform_calculation.assert_called_once_with(
            "pressure",
            float(known_pressure),
            float(known_temperature),
            float(target_temperature),
            float(dH_vap),
        )


@pytest.mark.asyncio
async def test_switching_solver_mode_resets_target_field():
    app = BoilingPointConverterApp()
    async with app.run_test() as pilot:
        app.query_one("#at-value").value = "10"

        assert app.query_one("#at-value").value == "10"
        await pilot.click("#solver-mode > #temperature")
        assert app.query_one("#at-value").value == ""


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "field,value",
    [
        ("#p1", "-1"),
        ("#t1", "-300"),
        ("#at-value", "-999"),
    ],
)
async def test_invalid_input_changes_input_css(field, value):
    app = BoilingPointConverterApp()
    async with app.run_test() as pilot:
        app.query_one(field).value = value
        await pilot.pause()

        assert "-invalid" in app.query_one(field).classes


@pytest.mark.asyncio
async def test_invalid_dhvap_changes_input_css():
    app = BoilingPointConverterApp()
    async with app.run_test() as pilot:
        option_list = app.query_one("#dHvap-selection")
        option_list.highlighted = option_list.get_option_index("custom-dHvap")
        option_list.action_select()
        app.query_one("#dHvap").value = "-10"
        await pilot.pause()

        assert "-invalid" in app.query_one("#dHvap").classes


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "field,value", [("#p1", "-1"), ("#t1", "-300"), ("#at-value", "-999")]
)
async def test_calculate_with_invalid_field_notifies_user(field, value, mocker):
    # TODO: Consider asserting toast message
    mock_notify = mocker.patch(
        "boiling_point_converter.app.BoilingPointConverterApp.notify"
    )
    mock_perform_calculation = mocker.patch(
        "boiling_point_converter.app.perform_calculation"
    )
    app = BoilingPointConverterApp()
    async with app.run_test() as pilot:
        app.query_one("#p1").value = "760"
        app.query_one("#t1").value = "100"
        app.query_one("#at-value").value = "10"

        app.query_one(field).value = value
        await pilot.click("#calculate")

    mock_notify.assert_called_once()
    mock_perform_calculation.assert_not_called()


@pytest.mark.asyncio
async def test_calculate_with_invalid_dhvap_fails_and_notifies_user(mocker):
    mock_notify = mocker.patch(
        "boiling_point_converter.app.BoilingPointConverterApp.notify"
    )
    mock_perform_calculation = mocker.patch(
        "boiling_point_converter.app.perform_calculation"
    )
    app = BoilingPointConverterApp()
    async with app.run_test() as pilot:
        app.query_one("#p1").value = "760"
        app.query_one("#t1").value = "100"
        app.query_one("#at-value").value = "10"
        option_list = app.query_one("#dHvap-selection")
        option_list.highlighted = option_list.get_option_index("custom-dHvap")
        option_list.action_select()
        await pilot.pause()
        app.query_one("#dHvap").value = "-10"
        await pilot.click("#calculate")

    mock_notify.assert_called_once()
    mock_perform_calculation.assert_not_called()
