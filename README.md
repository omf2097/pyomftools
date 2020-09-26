# PyOMFTools

Some tools for decompiling and compiling OFM2097 AF files to JSON format
and back to help with poking at the binary.

## HTML cards

Prebuilt version of the HTML data is available at 
https://katajakasa.fi/projects/openomf/cards/

## Installation

1. Make sure you have python 3.7 installed
2. Create a virtualenv, eg. `virtualenv -p /usr/bin/python3.7 pyomftools`
3. Activate the virtualenv, eg. `source pyomftools/bin/activate`
3. Install dependencies inside the virtualenv: `pip install -r requirements.txt`
3. Run! eg. `python -m omftools.cli.af_compile -h`
