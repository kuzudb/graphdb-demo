# Mindstone AI Meetup

This repo contains the code to reproduce the demo presented at the Mindstone AI Meetup
in Toronto on 9 July 2024.

## Dataset

This demo uses a wine reviews dataset downloaded [from Kaggle](https://www.kaggle.com/datasets/zynicide/wine-reviews). The dataset consists of 130k wine reviews with the variety, location, winery, price, description, and some other metadata provided for each wine.

For reference, a sample wine item in JSON format is shown below.

```json
{
    "points": "90",
    "title": "Castello San Donato in Perano 2009 Riserva  (Chianti Classico)",
    "description": "Made from a blend of 85% Sangiovese and 15% Merlot, this ripe wine delivers soft plum, black currants, clove and cracked pepper sensations accented with coffee and espresso notes. A backbone of firm tannins give structure. Drink now through 2019.",
    "taster_name": "Kerin O'Keefe",
    "taster_twitter_handle": "@kerinokeefe",
    "price": 30,
    "designation": "Riserva",
    "variety": "Red Blend",
    "region_1": "Chianti Classico",
    "region_2": null,
    "province": "Tuscany",
    "country": "Italy",
    "winery": "Castello San Donato in Perano",
    "id": 40825
}
```

Download the file `winemag-data-130k-v2.csv` to this path.

## Artificial data generation

To generate the required artificial data of customers and purchases that are shown in the demo, run the
bash script `run_generators.sh` in the `scripts` directory. This will generate the requisite files
in the `data/final` directory. The script uses the `Faker` library to generate the data, so
make sure to run `pip install faker` first.

```
$ ./run_generators.sh
Finished generating customers
Finished generating tasters
Finished generating follows relationships
Finished generating lives_in relationships
Finished generating purchases relationships
Finished generating tasted relationships
```
The following files will be generated:
```
.
├── final
    ├── customers.parquet
    ├── follows.parquet
    ├── lives_in.parquet
    ├── purchases.parquet
    ├── tasted.parquet
    ├── tasters.parquet
    └── winemag-reviews.parquet
```

Once these files exist, you can proceed to run the demo notebooks!

## Notebooks

The demo consists of three notebooks:

- `demo_1.ipynb`: Ingest the data to Kùzu and perform some basic exploratory data analysis.
- `demo_2.ipynb`: Learn how to Kùzu's `GraphQAChain` in LangChain to query the graph using an LLM.
- `demo_3.ipynb`: Run a graph algorithm to find the most influential tasters in the network, and learn how to use Kùzu as a backend to PyTorch Geometric for graph machine learning.

## Setup

To run the notebooks, you will need to install the dependencies using `requirements.txt`. You can do this by running:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

Activate the virtual environment in Jupyter Notebook by creating a new `ipython` kernel:

```bash
ipython kernel install --user --name=.venv
```

Then, start Jupyter Notebook and connect to the kernel you just created so your Python dependencies are available in the notebook.

## Visualization

You can visualize the Kùzu graph using the Kùzu Explorer tool. Download and install Docker, and run the
provided `docker-compose.yml` file to start Kùzu Explorer on your machine. Simply ensure that
the directory to the local database directory is correctly specified in `docker-compose.yml`.

```bash
docker compose up
```

ALternatively, you can run the following Docker command from the terminal, once again taking care to
ensure that the correct path to the local database directory is specified:

```bash
docker run -p 8000:8000 \
           -v ./db:/database \
           -e MODE=READ_ONLY \
           --rm kuzudb/explorer:latest
```

Open a web browser and navigate to `http://localhost:8000` to work within Kùzu Explorer.
