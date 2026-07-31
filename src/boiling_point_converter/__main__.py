"""Provides the main entry-point for the TUI."""

from .app import BoilingPointConverterApp


def main() -> None:
    BoilingPointConverterApp().run()


if __name__ == "__main__":
    main()
