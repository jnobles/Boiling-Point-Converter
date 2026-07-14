set default-list := true
set windows-powershell := true

setup:
    uv sync --group dev

lint:
    uv run ruff check .

format:
    uv run ruff format .

fix:
    uv run ruff check --fix .
    just format

test:
    uv run pytest

check: lint test

build: check
    uv build
    uv run pyinstaller pyinstaller.spec

release: build
    uv run pip-licenses
    uv run scripts/package.py

clean:
    uv run scripts/clean.py
