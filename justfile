set default-list := true
set windows-powershell := true

setup:
    uv sync --extra dev

lint: setup
    uv run ruff check --fix .

format: setup
    uv run ruff format .
    
clean: setup lint format

build: setup
    uv build
    uv run pyinstaller pyinstaller.spec
