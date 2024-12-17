"""
Extract and clean the wine reviews data from the raw input file
"""
import polars as pl
from pathlib import Path

output_path = Path("../final")

df = pl.read_csv("../winemag-data-130k-v2.csv").rename({"": "id"})
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
# Write a smaller version for demo on GitHub
wines.head(100).write_parquet(output_path / "winemag-reviews-small.parquet")