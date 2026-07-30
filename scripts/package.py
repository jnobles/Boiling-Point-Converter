import sys
import shutil
import zipfile
from pathlib import Path
from importlib.metadata import version

dist_dir = Path("dist")
root_dir = Path(".")
project_version = version("boiling-point-converter")
zip_path = dist_dir / f"boiling_point_converter-{project_version}-windows.zip"

required_files = {
    dist_dir / "Boiling Point Converter.exe",
    dist_dir / f"boiling_point_converter-{project_version}-py3-none-any.whl",
    dist_dir / f"boiling_point_converter-{project_version}.tar.gz",
    root_dir / "LICENSE.txt",
    root_dir / "THIRD_PARTY_LICENSES.txt",
}

files_to_zip = [
    dist_dir / "Boiling Point Converter.exe",
    root_dir / "LICENSE.txt",
    root_dir / "THIRD_PARTY_LICENSES.txt",
]

distributable_objects = {
    dist_dir / f"boiling_point_converter-{project_version}-py3-none-any.whl",
    dist_dir / f"boiling_point_converter-{project_version}.tar.gz",
    zip_path,
}

required_files_present = True
for path in required_files:
    if not path.exists():
        print(f"Required file {path} not found.")
        required_files_present = False

if not required_files_present:
    print("Required files are missing... Aborting.")
    sys.exit(1)

print("Creating distribution archive...")

with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
    for path in files_to_zip:
        zf.write(path, path.name)
        print(f"Added {path} to archive...")

print(f"Compressed archive created at {zip_path}.")

print(f"Cleaning up {dist_dir} ...")

for path in dist_dir.iterdir():
    if path not in distributable_objects:
        if path.is_file():
            path.unlink()
        elif path.is_dir():
            shutil.rmtree(path)

print(f"Removed all non-release assets from {dist_dir}.")
