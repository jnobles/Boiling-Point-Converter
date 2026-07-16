import pytest

import boiling_point_converter.molar_heat_of_vaporization
import boiling_point_converter.utils as bp_utils
from boiling_point_converter.app import BoilingPointConverterApp


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
            p1=float(known_pressure),
            t1=float(known_temperature),
            p2=float(target_pressure),
            t2=float(target_temperature),
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
            p1=float(known_pressure),
            t1=float(known_temperature),
            p2=float(target_pressure),
            t2=float(target_temperature),
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
            p1=float(known_pressure),
            t1=float(known_temperature),
            p2=float(target_pressure),
            t2=float(target_temperature),
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
            p1=float(known_pressure),
            t1=float(known_temperature),
            p2=float(target_pressure),
            t2=float(target_temperature),
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
            boiling_point_converter.molar_heat_of_vaporization.REFERENCE_HEATS_OF_VAPORIZATION_BY_COMPOUND[
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
            boiling_point_converter.molar_heat_of_vaporization.REFERENCE_HEATS_OF_VAPORIZATION_BY_COMPOUND[
                "water"
            ]
        )


@pytest.mark.asyncio
async def test_custom_dh_used_in_temperature_calculation(mocker):
    known_pressure = "760"
    known_temperature = "100"
    target_pressure = "10"
    dH_vap = "30"

    calculate_temperature_at_pressure = mocker.patch(
        "boiling_point_converter.app.calculate_temperature_at_pressure", return_value=20
    )

    app = BoilingPointConverterApp()
    async with app.run_test() as pilot:
        await pilot.click("#p1")
        await pilot.press(*known_pressure)
        await pilot.click("#t1")
        await pilot.press(*known_temperature)
        await pilot.click("#at-value")
        await pilot.press(*target_pressure)
        option_list = app.query_one("#dHvap-selection")
        option_list.highlighted = option_list.get_option_index("custom-dHvap")
        option_list.action_select()
        await pilot.pause()
        await pilot.click("#dHvap")
        await pilot.press(*dH_vap)
        await pilot.click("#calculate")

        calculate_temperature_at_pressure.assert_called_once_with(
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

    mock_calculate_pressure_at_temperature = mocker.patch(
        "boiling_point_converter.app.calculate_pressure_at_temperature", return_value=20
    )

    app = BoilingPointConverterApp()
    async with app.run_test() as pilot:
        await pilot.click("#p1")
        await pilot.press(*known_pressure)
        await pilot.click("#t1")
        await pilot.press(*known_temperature)
        await pilot.click("#solver-mode > #temperature")
        await pilot.click("#at-value")
        await pilot.press(*target_temperature)
        option_list = app.query_one("#dHvap-selection")
        option_list.highlighted = option_list.get_option_index("custom-dHvap")
        option_list.action_select()
        await pilot.pause()
        await pilot.click("#dHvap")
        await pilot.press(*dH_vap)
        await pilot.click("#calculate")

        mock_calculate_pressure_at_temperature.assert_called_once_with(
            float(known_pressure),
            float(known_temperature),
            float(target_temperature),
            float(dH_vap),
        )


@pytest.mark.asyncio
async def test_switching_solver_mode_resets_target_field():
    app = BoilingPointConverterApp()
    async with app.run_test() as pilot:
        await pilot.click("#at-value")
        await pilot.press(*"10")

        assert app.query_one("#at-value").value == "10"
        await pilot.click("#solver-mode > #temperature")
        assert app.query_one("#at-value").value == ""

        await pilot.click("#at-value")
        await pilot.press(*"10")

        assert app.query_one("#at-value").value == "10"
        await pilot.click("#solver-mode > #pressure")
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
        await pilot.click(field)
        await pilot.press(*value)

        assert "-invalid" in app.query_one(field).classes


@pytest.mark.asyncio
async def test_invalid_dhvap_changes_input_css():
    app = BoilingPointConverterApp()
    async with app.run_test() as pilot:
        option_list = app.query_one("#dHvap-selection")
        option_list.highlighted = option_list.get_option_index("custom-dHvap")
        option_list.action_select()
        await pilot.pause()
        await pilot.click("#dHvap")
        await pilot.press(*"-10")

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
    mock_calculate_pressure = mocker.patch(
        "boiling_point_converter.app.calculate_pressure_at_temperature"
    )
    mock_calculate_temperature = mocker.patch(
        "boiling_point_converter.app.calculate_temperature_at_pressure"
    )
    app = BoilingPointConverterApp()
    async with app.run_test() as pilot:
        await pilot.click("#p1")
        await pilot.press(*"760")
        await pilot.click("#t1")
        await pilot.press(*"100")
        await pilot.click("#at-value")
        await pilot.press(*"10")

        await pilot.click(field)
        await pilot.press(*value)
        await pilot.click("#calculate")

    mock_notify.assert_called_once()
    mock_calculate_pressure.assert_not_called()
    mock_calculate_temperature.assert_not_called()


@pytest.mark.asyncio
async def test_calculate_with_invalid_dhvap_fails_and_notifies_user(mocker):
    mock_notify = mocker.patch(
        "boiling_point_converter.app.BoilingPointConverterApp.notify"
    )
    mock_calculate_pressure = mocker.patch(
        "boiling_point_converter.app.calculate_pressure_at_temperature"
    )
    mock_calculate_temperature = mocker.patch(
        "boiling_point_converter.app.calculate_temperature_at_pressure"
    )
    app = BoilingPointConverterApp()
    async with app.run_test() as pilot:
        await pilot.click("#p1")
        await pilot.press(*"760")
        await pilot.click("#t1")
        await pilot.press(*"100")
        await pilot.click("#at-value")
        await pilot.press(*"10")
        option_list = app.query_one("#dHvap-selection")
        option_list.highlighted = option_list.get_option_index("custom-dHvap")
        option_list.action_select()
        await pilot.pause()
        await pilot.click("#dHvap")
        await pilot.press(*"-10")
        await pilot.click("#calculate")

    mock_notify.assert_called_once()
    mock_calculate_pressure.assert_not_called()
    mock_calculate_temperature.assert_not_called()
