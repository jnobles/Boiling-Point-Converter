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
