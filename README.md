# PyOMFTools

Some tools for decompiling and compiling OFM2097 AF files to JSON format
and back to help with poking at the binary.

## HTML cards

Prebuilt version of the HTML data is available at 
https://katajakasa.fi/projects/openomf/cards/

## Installation

1. Make sure you have python 3.11 installed
2. Create a virtualenv, eg. `poetry env use 3.11` and install deps `poetry install --no-root`.
3. Activate the virtualenv, eg. `poetry shell`
4. Run! eg. `python -m omftools.cli.af_compile -h`
