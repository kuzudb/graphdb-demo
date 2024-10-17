# Copy from DuckDB database to Kùzu

This demo shows how to attach an external DuckDB database to Kùzu and copy data from it to a Kùzu database to run graph analytics. This is especially useful when the query workloads benefit from graphs, and the data sits in an existing RDBMS like DuckDB.

## Problem statement

The dataset consists iof 

## Setup

Install the required dependencies via the `uv` package manager and `requirements.txt` file as follows:
```bash
# Create a virtual environment
uv venv
# On macOS and Linux
source .venv/bin/activate
# On Windows
.venv\Scripts\activate
# Install the required dependencies
uv pip install -r requirements.txt
```

## Run the workflow

The workflow is run via the provided scripts.

- `generate_travel_data.py` generates a CSV file of persons and the cities they travelled to from
the existing `data/person.csv` file.
- `insert_duck.py` inserts the raw data from the provided CSV files in `./data` into the DuckDB database
- `insert_kuzu.py` inserts the data from the DuckDB database into the Kùzu database. This script
utilizes the Kùzu DuckDB extension to copy the data from DuckDB into Kùzu.

Run the scripts in the following order:
```bash
python generate_travel_data.py
python insert_duck.py
python insert_kuzu.py
```
 