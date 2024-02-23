import csv
import dis
from pathlib import Path
from typing import Any

import kuzu


def read_csv(file_path: Path) -> list[dict[str, Any]]:
    with open(file_path) as file:
        reader = csv.DictReader(file)
        return list(reader)


def mark_disputed_transactions(conn: kuzu.Connection, params: list[dict[str, Any]]) -> None:
    query = """
        MATCH (c:Client)-[t:TransactedWith]->(m:Merchant)
        WHERE t.transaction_id = $transaction_id
        SET t.is_disputed = TRUE
        RETURN *;
    """
    conn.execute(query, parameters=params)
    print(f"Transaction {params['transaction_id']} marked as disputed.")


def main() -> None:
    db = kuzu.Database(DB_NAME)
    conn = kuzu.Connection(db)
    # Read from CSV
    disputed_ids = read_csv(FILE_PATH / "disputed_transactions.csv")
    for record in disputed_ids:
        transaction_id = int(record["transaction_id"])
        mark_disputed_transactions(conn, {"transaction_id": transaction_id})


if __name__ == "__main__":
    DB_NAME = "./transaction_db"
    FILE_PATH = Path("./data/node")
    main()
