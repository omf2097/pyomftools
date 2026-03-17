# PyOMFTools

Some tools for decompiling and compiling OFM2097 AF files to JSON format
and back to help with poking at the binary.

## HTML cards

Prebuilt version of the HTML data is available at
https://katajakasa.fi/projects/openomf/cards/

## Installation

1. Make sure you have python 3.12 installed
2. Create a virtualenv, eg. `poetry env use 3.12` and install deps `poetry install --no-root`.
3. Activate the virtualenv, eg. `poetry shell`
4. Run! eg. `python -m omftools.cli.af_compile -h`

Or with pyenv:
1. `pyenv install 3.11.4`
2. `pyenv virtualenv 3.11.4 pyomftools-3.11`
3. `pyenv local pyomftools-3.11`
4. ...

## How to ...

### Generate the taglist.c

1. Do the installation step above
2. Make sure the tag `omftools/resources/tags.csv` is up-to-date.
3. Run `poetry run python -m omftools.cli.tags -i omftools/resources/tags.csv taglist.c`
4. Copy the generated `taglist.c` as required.
