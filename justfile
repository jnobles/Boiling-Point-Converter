set default-list := true
set windows-powershell := true

setup:
    uv sync --extra dev

lint:
    uv run ruff check .

fix:
    uv run ruff check --fix .
    uv run ruff format .

build: test
    uv build
    uv run pyinstaller pyinstaller.spec

test:
    uv run pytest -v

check: lint test

release: check build
    uv run pip-licenses
    tar.exe acvf "dist/Temperature-Pressure Boiling Point Converter.zip" -C dist "Temperature-Pressure Boiling Point Converter.exe" -C .. LICENSE.txt THIRD_PARTY_LICENSES.txt

release: test build
    uv run pip-license
    tar.exe acvf dist/Temperature-Pressure\ Calculator.zip -C dist Temperature-Pressure\ Calculator.exe -C .. LICENSE.txt THIRDPARTYLICENSES.txt

check: lint test

clean:
    uv run scripts/clean.py
