# v1.0.0

First stable release of the temperature-pressure boiling point converter.

This release focuses on improving reliability, maintainability, and distribution.  Included are the expansion of the testing suite to cover user interaction with the terminal user interface (TUI).  Additionally, automated continuous-integration (CI) checks and reproducible release workflows have been implemented.

## Highlights

- Added automated CI checks for Linux and Windows
- Added release workflow for Windows distributions
- Created test coverage for TUI workflows
- Improved packaging and distribution workflow

### Added

- Added user interaction tests for TUI workflows
- Added automated coverage reporting
- Added CI workflow for linting and testing
- Added Windows release workflow
- Added third-party license collection for packaged releases
- Added docstrings to describe usage of core utilities
- Added explicit reference to the scientific assumptions used during calculation

### Changed

- Refactored utility responsibilities into clearer modules
- Simplified TUI interaction handling
- Improved package metadata
- Updated development tooling and workflow

### Fixed

- Fixed edge-case potential for division by zero
- Corrected event type annotations
- Corrected package tooling references

## Distribution

This release provides the following formats:

- Windows standalone executable
- Python wheel package
- Python source distribution

## Installation

### Standalone executable (Windows)

Download and extract the Windows zip archive and run directly.  No existing Python installation is required.

### Install from wheel (Python)

Download the wheel file and install with:

```powershell
pip install .\boiling_point_converter-1.0.0-py3-none-any.whl
```

Then run with:

```powershell
boiling-point-converter
```

## Release Assets

- `boiling_point_converter-1.0.0-windows.zip`: zip archive containing the standalone Windows executable and licensing information
- `boiling_point_converter-1.0.0-py3-none-any.whl`: Python wheel package
- `boiling_point_converter-1.0.0.tar.gz`: Python source distribution