# ShopSmart

ShopSmart is a terminal based shopping and budget tracker written in Python. It stores products, purchases, and budget settings in local JSON files.

## Features

- Add, update, search, filter, and remove products
- Record purchases and update product inventory
- Compare products and get recommendations
- Track a budget and view spending analytics
- Export reports and back up or restore local data

## Requirements

- Python 3.10 or newer
- pip

## Setup

From the project directory, create and activate a virtual environment:

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

macOS or Linux:

```bash
source .venv/bin/activate
```

Install dependencies and start ShopSmart:

```bash
python -m pip install -r requirements.txt
python main.py
```

Use the arrow keys and Enter for interactive menus. If the terminal cannot support interactive prompts, ShopSmart falls back to numbered or text input.

## Tests

Run the unit tests from the project directory:

```bash
python -m unittest discover -s tests -v
```

## Project layout

```text
main.py        Terminal interface
modules/       Product, purchase, budget, comparison, analytics, and report logic
utils/         Validation, helpers, and JSON persistence
data/          Starter product, purchase, and budget data
tests/         Unit tests
```

ShopSmart writes its current data to `data/` and creates snapshots under `backups/` when backups are requested. Keep a copy of those files if you need to preserve changes between machines.
