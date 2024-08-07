import asyncio

import asyncpg
import kuzu
import networkx as nx
import polars as pl
from asyncpg.pool import Pool

PG_URI = "postgresql://postgres:testpassword@localhost:5432/postgres"
db = kuzu.Database("./ex_db_kuzu")
conn = kuzu.Connection(db)
# print(f"Kùzu version: {kuzu.__version__}")


def get_betweenness_centrality_records() -> list[dict[str, float]]:
    res = conn.execute(
        """
        MATCH (a1:Account)-[t:Transfer]->(a2:Account)
        RETURN *
        """
    )

    G = res.get_as_networkx(directed=False)
    bc = nx.betweenness_centrality(G, normalized=True)
    bc_records = [
        {"id": node.replace("Account_", ""), "betweenness_centrality": bc[node]} for node in bc
    ]
    return bc_records


# --- Write results to Kùzu ---
def update_account_node_table(conn: kuzu.Connection) -> None:
    try:
        conn.execute(
            """
            ALTER TABLE Account ADD betweenness_centrality REAL DEFAULT 0.0
            """
        )
    except RuntimeError:
        print("Column already exists, skipping creation.")


def update_accounts_betweenness_centrality(bc_records: list[dict[str, float]]) -> None:
    account_df = pl.DataFrame(bc_records)
    conn.execute(
        """
        LOAD FROM account_df
        WITH CAST(id AS INT32) AS id, betweenness_centrality
        MERGE (a:Account {id: id})
        ON MATCH SET a.betweenness_centrality = betweenness_centrality
        """
    )
    print(f"Inserted {len(bc_records)} betweenness centrality records to Kùzu")


# --- Write results to Postgres ---
async def update_accounts_table(pool: Pool) -> None:
    async with pool.acquire() as conn:
        await conn.execute(
            """
            ALTER TABLE account
            ADD COLUMN IF NOT EXISTS betweenness_centrality REAL DEFAULT 0.0
            """
        )


async def insert_betweenness_centrality_records(pool: Pool, records: list[dict]) -> None:
    async with pool.acquire() as conn:
        await conn.executemany(
            "UPDATE account SET betweenness_centrality = $2 WHERE id = $1",
            [(int(record["id"]), record["betweenness_centrality"]) for record in records],
        )


async def main():
    # Update Postgres database
    async with asyncpg.create_pool(PG_URI, min_size=5, max_size=20) as pool:
        bc_records = get_betweenness_centrality_records()
        await update_accounts_table(pool)
        await insert_betweenness_centrality_records(pool, bc_records)
        print(f"Inserted {len(bc_records)} betweenness centrality records to Postgres")
    # Update Kùzu database
    update_account_node_table(conn)
    update_accounts_betweenness_centrality(bc_records)


if __name__ == "__main__":
    asyncio.run(main())
