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

check: lint coverage

build: check
    uv build

[windows]
release: build
    uv run pyinstaller pyinstaller.spec
    uv run pip-licenses
    uv run scripts/package.py

clean:
    uv run scripts/clean.py
    uv run coverage erase

coverage:
    uv run coverage run -m pytest
    uv run coverage report
    uv run coverage html
