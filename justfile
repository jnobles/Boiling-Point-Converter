set default-list := true
set windows-powershell := true

setup:
    uv sync --extra dev

lint:
    uv run ruff check .

fix:
    uv run ruff check --fix .
    uv run ruff format .

build:
    uv build
    uv run pyinstaller pyinstaller.spec

test:
    uv run pytest -v

release: test build
    uv run pip-license
    tar.exe acvf dist/Temperature-Pressure\ Calculator.zip -C dist Temperature-Pressure\ Calculator.exe -C .. LICENSE.txt THIRDPARTYLICENSES.txt