# BFAVCP

A converter to convert BFAV (Better Farm Animal Variety) mods to Content Patcher for the upcoming Stardew Valley 1.6.

## Usage

1. Download and install [Python](https://www.python.org/downloads/) (3.11 was used to develop this project.).
2. Clone this repository by using the following ***TWO*** commands:
    - `git clone https://github.com/anotherpillow/BFAV2CP.git && cd BFAV2CP`
    - `git submodule update --init --recursive`
3. Place your BFAV mod into the same directory as `main.py` and rename it to `input`, so the `manifest.json` is `<BFAV2CP Directory>/input/manifest.json`
4. Run `main.py` (preferably from a terminal)
5. Find your converted mod in `output/`
