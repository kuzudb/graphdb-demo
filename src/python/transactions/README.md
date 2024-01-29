# Analyzing Transactions

This directory contains a set of scripts that can be used to analyze
a dataset of merchants, customers and transactions. The goal is to study
the transactions and their relationships using graph queries, and to perform
more sophisticated analysis using graph algorithms.

## Getting Started

To get started, you'll need to install the Kuzu Python SDK. It's recommended to
use a virtual environment.

```bash
# Create a virtual environment
python -m venv venv
source venv/bin/activate
# Assuming Python 3.8+ is installed
pip install kuzu
```

## Loading the dataset

The dataset is a set of CSV files that can be loaded into Kuzu using the
`kuzu import` command. The dataset is available in the `data` directory.

```bash
python load_data.py
```

## Running the queries

The `queries.py` script contains a set of queries that can be run against th
dataset. The queries are written in Cypher.

```bash
python query.py
```

## Visualization

Visualization of the graph can be done using the [Kuzu Explorer](https://github.com/kuzudb/explorer)
tool. You can start an instance of the Explorer using a Docker command.

```bash
# Ensure you use absolute paths when mounting the database
docker run -p 8000:8000 \
        -v /absolute/path/to/transaction_db:/database \
        --rm kuzudb/explorer:latest
```

Alternatively, you can use the provided `docker-compose.yml` configured with the relative path
to your data and start/stop the container as follows:

```bash
# Run container in detached mode
docker compose up -d
# Stop container
docker compose down
```
