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