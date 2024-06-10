# Dataset

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

