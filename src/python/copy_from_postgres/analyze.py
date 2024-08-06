import asyncio
import kuzu
import networkx as nx
import asyncpg
from asyncpg.pool import Pool

PG_URI = "postgresql://postgres:testpassword@localhost:5432/postgres"
db = kuzu.Database("./ex_db_kuzu")
conn = kuzu.Connection(db)
print(f"Kùzu version: {kuzu.__version__}")

def get_betweenness_centrality_records() -> list[dict[str, float]]:
    res = conn.execute(
        """
        MATCH (a1:Account)-[t:Transfer]->(a2:Account)
        RETURN *
        """
    )

    G = res.get_as_networkx(directed=False)
    bc = nx.betweenness_centrality(G, normalized=True)
    bc_records = [{"id": node.replace("Account_", ""), "betweenness_centrality": bc[node]} for node in bc]
    return bc_records


async def update_accounts_table(pool: Pool) -> None:
    async with pool.acquire() as conn:
        await conn.execute(
            """
            ALTER TABLE account
            ADD COLUMN IF NOT EXISTS betweenness_centrality REAL DEFAULT 0.0
            """)


async def insert_betweenness_centrality_records(pool: Pool, records: list[dict]) -> None:
    async with pool.acquire() as conn:
        await conn.executemany(
            "UPDATE account SET betweenness_centrality = $2 WHERE id = $1",
            [(int(record["id"]), record["betweenness_centrality"]) for record in records],
        )


async def main():
    async with asyncpg.create_pool(PG_URI, min_size=5, max_size=20) as pool:
        bc_records = get_betweenness_centrality_records()
        await update_accounts_table(pool)
        await insert_betweenness_centrality_records(pool, bc_records)
        print(f"Finished loading {len(bc_records)} betweenness centrality records to Postgres table")


if __name__ == "__main__":
    asyncio.run(main())