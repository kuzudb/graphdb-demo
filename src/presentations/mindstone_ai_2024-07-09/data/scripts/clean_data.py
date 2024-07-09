"""
Extract and clean the wine reviews data from the raw input file
"""
import polars as pl
from pathlib import Path

output_path = Path("../final")

FILE_NAME = "winemag-data-v2-small.csv"
df = pl.read_csv(f"../{FILE_NAME}").rename({"": "id"})
wines = df.select([
    "id",
    "title",
    "country",
    "description",
    "variety",
    "points",
    "price",
    "region_1",
    "taster_name",
    "taster_twitter_handle",
])

output_path.mkdir(exist_ok=True)
wines.write_parquet(output_path /"winemag-reviews.parquet")