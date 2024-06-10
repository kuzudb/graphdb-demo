"""
Generate a random list customer IDs that follow a particular taster
"""

from pathlib import Path
import random
import polars as pl

random.seed(37)

output_path = Path("../final")

customers = list(range(1, 26))
tasters = pl.read_parquet(output_path / "tasters.parquet").select("taster_id").to_series().to_list()

# Match a customer with a random city
random.shuffle(tasters)
lives_in = list(zip(customers, tasters))

lives_in_df = pl.DataFrame(
    {
        "customer_id": [lives[0] for lives in lives_in],
        "taster_id": [lives[1] for lives in lives_in],
    }
)

# Write to a Parquet file
output_path.mkdir(exist_ok=True)
lives_in_df.write_parquet(output_path / "follows.parquet")
print("Finished generating follows relationships")
