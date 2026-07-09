set default-list := true
set windows-powershell := true

setup:
    uv sync --extra dev

lint:
    uv run ruff check --fix .

format:
    uv run ruff format .
    
clean: lint format

build:
    uv build
    uv run pyinstaller pyinstaller.spec

test:
    uv run pytest -v
