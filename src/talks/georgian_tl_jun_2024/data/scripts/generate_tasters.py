"""
Generate a unique list of all wine tasters who reviewed wines in the dataset
"""

from pathlib import Path
import polars as pl

output_path = Path("../final")

tasters = pl.read_parquet(output_path / "winemag-reviews.parquet").select("taster_twitter_handle", "taster_name").unique().drop_nulls(subset=["taster_name"])

tasters_df = tasters.with_columns(
    pl.col("taster_name")
    .str.to_lowercase()
    .str.replace(" ", "_")
    .str.replace("’", "_")
    .str.replace(". ", "_")
    .alias("taster_id")
)

# Write to a parquet file
output_path.mkdir(exist_ok=True)
tasters_df.write_parquet(output_path / "tasters.parquet")
print("Finished generating tasters")