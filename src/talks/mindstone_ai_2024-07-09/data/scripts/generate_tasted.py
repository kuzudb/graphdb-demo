"""
Generate a list of relationships between wine tasters and the wines they tasted for a review

This script joins the existing `tasters.parquet` and `winemag-reviews.parquet` files
"""
import polars as pl
from pathlib import Path

output_path = Path("../final")

# Read the tasters and reviews data
tasters = pl.read_parquet(output_path / "tasters.parquet")
reviews = pl.read_parquet(output_path / "winemag-reviews.parquet")

joined = reviews.join(tasters, on="taster_name", how="full").select("taster_id", "id").drop_nulls()

# Write to a parquet file
output_path.mkdir(exist_ok=True)
joined.write_parquet(output_path / "tasted.parquet")
print("Finished generating tasted relationships")

