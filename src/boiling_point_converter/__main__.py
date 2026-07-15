"""Provides the main entry-point for the TUI.

Starts the TUI, displaying an optional splashscreen during unpacking if
run using the PyInstaller generated executable.
"""

from .app import BoilingPointConverterApp


def main() -> None:
    try:
        import pyi_splash

        pyi_splash.update_text("Loading finished...")
        pyi_splash.close()
    except ModuleNotFoundError:
        pass

    BoilingPointConverterApp().run()


if __name__ == "__main__":
    main()
