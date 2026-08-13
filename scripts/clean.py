import shutil
from pathlib import Path

for path in (
        "build",
        "dist",
        ".pytest_cache",
        ".ruff_cache",
        "tests/.hypothesis",
        "htmlcov"
):
    shutil.rmtree(path, ignore_errors=True)

for path in Path(".").rglob("__pycache__"):
    shutil.rmtree(path, ignore_errors=True)

for path in Path(".").rglob("*.pyc"):
    path.unlink(missing_ok=True)
