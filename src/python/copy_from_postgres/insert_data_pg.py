import asyncio
import csv
from typing import Any, Dict

import asyncpg
from asyncpg.pool import Pool

Record = Dict[str, Any]
PG_URI = "postgresql://postgres:testpassword@localhost:5432/postgres"


# Import CSV as a list of dictionaries
def import_csv(file_path: str) -> list[Record]:
    with open(file_path) as file:
        reader = csv.DictReader(file)
        return list(reader)


async def truncate_tables(pool: Pool) -> None:
    async with pool.acquire() as conn:
        await conn.execute("TRUNCATE TABLE person, account, transfer;")


async def create_person_table(pool: Pool):
    async with pool.acquire() as conn:
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS person (
                id INTEGER PRIMARY KEY,
                name VARCHAR,
                address VARCHAR(512),
                state VARCHAR(2),
                zipcode VARCHAR(12),
                email VARCHAR(128)
            )
            """
        )


async def create_account_table(pool: Pool):
    async with pool.acquire() as conn:
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS account (
                id INTEGER PRIMARY KEY,
                account_id VARCHAR(128),
                owner INTEGER REFERENCES person(id),
                balance REAL
            )
            """
        )


async def create_transfer_table(pool: Pool):
    async with pool.acquire() as conn:
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS transfer (
                source INTEGER REFERENCES account(id),
                target INTEGER REFERENCES account(id),
                amount REAL,
                transaction_id VARCHAR(128) PRIMARY KEY
            )
            """
        )


async def insert_person_record(pool: Pool, record: Record):
    async with pool.acquire() as conn:
        await conn.execute(
            """
            INSERT INTO person (
                id,
                name,
                address,
                state,
                zipcode,
                email
            )
            VALUES ($1, $2, $3, $4, $5, $6);
            """,
            int(record["id"]),
            record["name"],
            record["address"],
            record["state"],
            record["zipcode"],
            record["email"],
        )


async def insert_account_record(pool: Pool, record: Record):
    async with pool.acquire() as conn:
        await conn.execute(
            """
            INSERT INTO account (
                id,
                account_id,
                owner,
                balance
            )
            VALUES ($1, $2, $3, $4);
            """,
            int(record["id"]),
            record["account_id"],
            int(record["owner"]),
            float(record["balance"]),
        )


async def insert_transfer_record(pool: Pool, record: Record):
    async with pool.acquire() as conn:
        await conn.execute(
            """
            INSERT INTO transfer (
                source,
                target,
                amount,
                transaction_id
            )
            VALUES ($1, $2, $3, $4);
            """,
            int(record["source"]),
            int(record["target"]),
            float(record["amount"]),
            record["transaction_id"],
        )


async def main():
    person_records = import_csv("data/person.csv")
    account_records = import_csv("data/account.csv")
    transfer_records = import_csv("data/transfer.csv")

    async with asyncpg.create_pool(PG_URI, min_size=5, max_size=20) as pool:
        # Create tables asynchronously using a connection pool
        await create_person_table(pool)
        await create_account_table(pool)
        await create_transfer_table(pool)
        # Truncate tables before inserting data
        await truncate_tables(pool)
        # Insert records asynchronously
        await asyncio.gather(*[insert_person_record(pool, record) for record in person_records])
        print(f"Inserted {len(person_records)} person records")

        await asyncio.gather(*[insert_account_record(pool, record) for record in account_records])
        print(f"Inserted {len(account_records)} account records")

        await asyncio.gather(*[insert_transfer_record(pool, record) for record in transfer_records])
        print(f"Inserted {len(transfer_records)} transfer records")


if __name__ == "__main__":
    asyncio.run(main())
