"""
Generate a random list customer IDs that live in a specific country
"""

from pathlib import Path
import random
import polars as pl

random.seed(37)

output_path = Path("../final")

customers = list(range(1, 26))
countries = pl.read_parquet(output_path / "winemag-reviews.parquet").select("country").to_series().to_list()

# Match a customer with a random country
random.shuffle(countries)
lives_in = list(zip(customers, countries))

lives_in_df = pl.DataFrame(
    {
        "customer_id": [lives[0] for lives in lives_in],
        "country": [lives[1] for lives in lives_in],
    }
)

# Write to a Parquet file
output_path.mkdir(exist_ok=True)
lives_in_df.write_parquet(output_path / "lives_in.parquet")
print("Finished generating lives_in relationships")
