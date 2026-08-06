"""Provides the main entry-point for the TUI."""

from boiling_point_converter.tui.app import BoilingPointConverterApp


def main() -> None:
    BoilingPointConverterApp().run()


if __name__ == "__main__":
    main()
