# Trade optimizer
A trading algorithm that, given historical data, attempts to determine the
best trades that could have been made to maximise profits.

## Setup
Create virtual environment and activate it.
```
python -m venv .venv
source .venv/bin/activate
```

Install dependencies.
```
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Run
Run the `trade_optimizer.py` script, passing the name of the CSV file you want to process.
```
python trade_optimizer.py data_3600.csv
```

## Debugging
On VSCode, just press F5, configuration is in `.vscode/launch.json`.
