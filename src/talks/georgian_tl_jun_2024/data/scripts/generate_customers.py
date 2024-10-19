"""
Generate fake customer profiles
"""

from pathlib import Path
import polars as pl
from faker import Faker

# Create a Faker instance
fake = Faker()
Faker.seed(37)

output_path = Path("../final")

# Generate a list of customer IDs
customer_ids = list(range(1, 26))
# Generate a list of customer first and last names
customers = [f"{fake.first_name()} {fake.last_name()}" for _ in customer_ids]
customer_age = [fake.random_int(min=21, max=80) for _ in customer_ids]
customers_df = pl.DataFrame(
    {
        "customer_id": customer_ids,
        "name": customers,
        "age": customer_age,
    }
)
# Write to a Parquet file
output_path.mkdir(exist_ok=True)
customers_df.write_parquet(output_path / "customers.parquet")
print("Finished generating customers")
