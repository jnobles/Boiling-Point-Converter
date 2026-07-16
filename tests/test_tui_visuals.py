from boiling_point_converter.app import BoilingPointConverterApp


def test_tui_visual(snap_compare):
    terminal_size = (132, 43)
    app = BoilingPointConverterApp()
    assert snap_compare(app, terminal_size=terminal_size)
