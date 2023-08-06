# Excel-compatible date and time functions

The _xldt_ module manipulates date and time by using sequential serial
numbers, like Microsoft Excel. The serial numbers are identical between
this module and Excel for dates starting with 1900-03-01 with the 1900
date system.

## Installation

If a _wheel_ is available for the target platform, one can install _xldt_ 
with _pip_, without other requirement:
```
pip install xldt
```
If a _wheel_ is not available for the target platform, a C compiler is
mandatory. The C compiler must be ABI-compatible with the one used to
compile the Python distribution importing the module. 

The source code can be cloned from GitHub with:
```
git clone https://github.com/vtudorache/xldt.git
```
The _build_ module is required, it can be installed from https://pypi.org 
with:
```
pip install build
```
Then, in the source directory, run:
```
python -m build
```
A `dist` directory will be created, containing a _wheel_ for the target
platform. The _wheel_ can be then installed from the `dist` directory
with _pip_.
