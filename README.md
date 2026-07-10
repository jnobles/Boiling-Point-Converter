# Temperature-Pressure Conversion Calculator

The Temperature-Pressure Conversion Calculator is a terminal user interface (TUI) calculator for quickly using the Clausius–Clapeyron relation to estimate boiling point depression/elevation under varying temperatures and pressures.  Several standard molar enthalpies of evaporation are provided for common solvents.

```math
\ln\left(\frac{P_1}{P_0}\right)=\frac{L}{R}\left(\frac{1}{T_0}-\frac{1}{T_1}\right)
```

## Features

- Calculate the boiling point at a target pressure
- Calculate the pressure required to achieve a target boiling point
- Built-in heats of vaporization for common solvents
- TUI built using Textual

## Installation

### Windows executable

Download the Windows executable from the GitHub release assets and run it directly.  No existing Python installation is required.

### Install from wheel

Download the `.whl` file from the GitHub release assets and install with:

```powershell
pip install .\boiling_point_converter-0.1.0-py3-none-any.whl
```

### Install from source distribution

Download the `.tar.gz` file from the GitHub release assets and install with:

```powershell
pip install .\boiling_point_converter-0.1.0.tar.gz
```

Note the project was developed and tested using Python 3.12.  Other versions may work but have not been tested.

## Usage

Launch the Windows executable or run

```powershell
boiling-point-converter
```

to launch the TUI.

![Screenshot of the TUI on running](/docs/TUI_screenshot.png)

Enter the temperature and pressure of the known boiling point.  Then select and enter either

- A target temperature (to calculate the required pressure to achieve that boiling point) 
- A target pressure (to calculate the new boiling point at that pressure).  
 
Select the compound (or similar) from the list of saved molar enthalpies of vaporization, or enter a value if known using the `Custom Heat of Vaporization`.  Pressing calculate will show a readout of results.

![Screenshot of the TUI after calculation](/docs/TUI_calculation_screenshot.png)

## Acknowledgement

Thank you to Witek Mozga for inspiring this personal project with their [Physicochemical Calculators](http://nowa.trimen.pl/witek/kalkulatory/index.html).

## References

Default standard molar enthalpies of vaporization included are taken from:

- Burgess, D. and Hamins, A. (2023), Heats of Combustion and Related Properties of Pure Substances, Technical Note (NIST TN), National Institute of Standards and Technology, Gaithersburg, MD, [online], https://doi.org/10.6028/NIST.TN.2126
