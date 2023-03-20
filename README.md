# conda-export
Refine of conda env export --from-history.
Now you can export environment with version using --from-history option.
You can choose which package should not appear in the environment.yaml file by CLI and a .yaml file.

## Installation
You may install the package as follows:
```bash
# Install from pypi
pip install ecoport

# Install from source code
git clone https://github.com/eiphy/conda-export.git
cd conda-export && pip install .

# Install in editabble mode
git clone https://github.com/eiphy/conda-export.git
cd conda-export && pip install -e .
```

## Sample Output
Output of `conda env export --from-history` with version number.
```yaml
name: torch
channels:
- pytorch
- defaults
dependencies:
- isort=5.9.3
- python=3.10.6
- pytorch=1.13.0
- torchaudio=0.13.0
- torchvision=0.14.0
```

## Usage
```bash
python -m ecoport -f tmp.yaml                   # Save env to ./tmp.yaml
python -m ecoport                               # Save env to ./environment.yaml
python -m ecoport --exclusions isort            # Excludes isort
python -m ecoport --config test/config.yaml     # Using config option (current only option for exclusion). --exclusion has higher priority.
python -m ecoport --no-prefix                   # Eliminate the prefix entry
```

Sample config file (test/config.yaml):
```yaml
exclusions:
- black
- isort
```