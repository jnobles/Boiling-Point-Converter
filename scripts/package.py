import sys
import zipfile
from pathlib import Path

dist_dir = Path("dist")
root_dir = Path(".")
target_file_list = [
    dist_dir / "Boiling Point Converter.exe",
    root_dir / "LICENSE.txt",
    root_dir / "THIRD_PARTY_LICENSES.txt",
]

failed = False
for file in target_file_list:
    if not file.exists():
        print(f"Required file {file} not found.")
        failed = True

if failed:
    print("Required files are missing... Aborting.")
    sys.exit(1)

zip_path = dist_dir / "Boiling-Point-Converter.zip"

print("Creating distribution archive...")

with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
    for file in target_file_list:
        zf.write(file, file.name)
        print(f"Added {file} to archive...")

print(f"Compressed archive created at {zip_path}.")
sys.exit(0)
