# Demo workflows

This section contains the demo workflows for the Georgian TL presentation in June 2024. The demo
is divided into three parts

## Workflow 1

- Demonstrate the general process of starting with structured data and ending with a graph
- Show some of the interop and direct scanning capabilities of Kùzu that make it flexible for a
variety of data sources
- Introduce the idea of data transformation and how it can be used to clean and enrich data before
thinking of it as a graph

## Workflow 2

- Demonstrate how to combine data from multiple tables/sources into a single graph
- Show how to use the graph to answer questions that would be difficult (or at the very least, more
verbose) to answer using SQL or tabular data transformations
- Show how to conceptualize and define a graph schema in Kùzu
- Bulk-insert data from multiple sources into node and relationship tables
- Query the graph to answer questions about the data
- Visualize the graph

## Workflow 3

- Demonstrate a simple GraphQA pipeline in LangChain
- Leverage an existing Kùzu for question-answering in natural language

## Setup

It's strongly recommended to set up a virtual environment in Python. The `uv` package manager is
a great option.

```bash
uv venv
source ./venv/bin/activate
uv pip install -r requirements.txt
```
