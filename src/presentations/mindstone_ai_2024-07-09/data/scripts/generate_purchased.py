"""
Generate a random list customer IDs that purchased specific wines IDs
"""
import random
from pathlib import Path
import polars as pl

random.seed(37)

output_path = Path("../final")

customers = list(range(1, 26))
wines = pl.read_parquet(output_path / "winemag-reviews.parquet").select("id").to_series().to_list()

# Generate a random list of purchases
purchases = [(customer, random.choice(wines)) for customer in customers]
purchases_df = pl.DataFrame(
    {
        "customer_id": [purchase[0] for purchase in purchases],
        "wine_id": [purchase[1] for purchase in purchases],
    }
)
# Write to a CSV file
output_path.mkdir(exist_ok=True)
purchases_df.write_parquet(output_path / "purchases.parquet")
print("Finished generating purchases relationships")