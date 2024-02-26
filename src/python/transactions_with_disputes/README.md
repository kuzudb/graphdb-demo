# Analyzing Transactions with Disputes

This directory contains a set of scripts that can be used to analyze
a dataset of merchants, customers and transactions, including disputed transactions.
The goal is to showcase how to use a combination of Cypher queries, graph visualization and
network analysis to answer questions about the data.

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

## Loading the transaction dataset

The dataset is a set of CSV files that can be loaded into Kuzu using the
`kuzu import` command. The dataset is available in the `data` directory.

```bash
python load_data.py
```

## Adding disputed transactions

The disputed transactions are added as boolean properties to the transaction edges that were
created in the previous step.

Simply run the following command to add the disputed transactions:

```bash
python mark_disputed_transactions.py
```

This will mark only the transactions that are disputed as `true`.

## Visualization

Visualization of the graph requires the [Kuzu Explorer](https://github.com/kuzudb/explorer)
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

## Running graph algorithms

The `analyze.py` script contains some examples of NetworkX algorithms that can be run on the Kùzu
graph.

```bash
python analyze.py
```
