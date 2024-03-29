from __future__ import annotations

import os
import shutil
from pathlib import Path

import kuzu


def create_client_node_table(conn: kuzu.Connection) -> None:
    conn.execute(
        """
        CREATE NODE TABLE
            Client(
                client_id INT64,
                name STRING,
                age INT64,
                PRIMARY KEY (client_id)
            )
        """
    )


def create_city_node_table(conn: kuzu.Connection) -> None:
    conn.execute(
        """
        CREATE NODE TABLE
            City(
                city_id INT64,
                city STRING,
                PRIMARY KEY (city_id)
            )
        """
    )


def create_company_node_table(conn: kuzu.Connection) -> None:
    conn.execute(
        """
        CREATE NODE TABLE
            Company(
                company_id INT64,
                type STRING,
                company STRING,
                PRIMARY KEY (company_id)
            )
        """
    )


def create_merchant_node_table(conn: kuzu.Connection) -> None:
    conn.execute(
        """
        CREATE NODE TABLE
            Merchant(
                merchant_id INT64,
                company_id INT64,
                city_id INT64,
                PRIMARY KEY (merchant_id)
            )
        """
    )


def create_transaction_edge_file(conn: kuzu.Connection) -> None:
    """
    Create a new file `transacted_with.csv` that stores the
    edges between clients and merchants, with metadata.
    No headers are written
    """
    conn.execute(
    f"""
    COPY (
        LOAD FROM '{DATA_PATH}/transaction.csv' (header=true)
        RETURN
            client_id,
            merchant_id,
            amount_usd,
            timestamp
    )
    TO '{DATA_PATH}/transacted_with.csv';
    """
    )


def create_merchant_edge_file(conn: kuzu.Connection) -> None:
    """
    Create a new file `belongs_to.csv` that stores the
    edges between merchants and their parent companies
    No headers are written
    """
    conn.execute(
    f"""
    COPY (
        LOAD FROM '{DATA_PATH}/merchant.csv' (header=true)
        RETURN
            merchant_id,
            company_id
    )
    TO '{DATA_PATH}/belongs_to.csv';
    """
    )


def create_location_in_edge_file(conn: kuzu.Connection) -> None:
    """
    Create a new file `located_in.csv` that stores the
    edges between merchants and cities
    No headers are written
    """
    conn.execute(
    f"""
    COPY (
        LOAD FROM '{DATA_PATH}/merchant.csv' (header=true)
        RETURN
            merchant_id,
            city_id
    )
    TO '{DATA_PATH}/located_in.csv';
    """
    )


def create_node_tables(conn: kuzu.Connection) -> None:
    create_client_node_table(conn)
    create_city_node_table(conn)
    create_company_node_table(conn)
    create_merchant_node_table(conn)


def create_edge_tables(conn: kuzu.Connection) -> None:
    conn.execute(
        """
        CREATE REL TABLE 
            TransactedWith(
                FROM Client TO Merchant,
                amount_usd FLOAT,
                timestamp TIMESTAMP
            )
        """
    )
    conn.execute("CREATE REL TABLE LocatedIn(FROM Merchant TO City)")
    conn.execute("CREATE REL TABLE BelongsTo(FROM Merchant TO Company)")


def main(conn: kuzu.Connection, DATA_PATH: Path) -> None:
    # Create edge table files from existing data
    create_transaction_edge_file(conn)
    create_merchant_edge_file(conn)
    create_location_in_edge_file(conn)

    # Ingest nodes
    create_node_tables(conn)
    conn.execute(f"COPY Client FROM '{DATA_PATH}/client.csv' (header=true);")
    conn.execute(f"COPY City FROM '{DATA_PATH}/city.csv' (header=true);")
    conn.execute(f"COPY Company FROM '{DATA_PATH}/company.csv' (header=true);")
    conn.execute(f"COPY Merchant FROM '{DATA_PATH}/merchant.csv' (header=true);")
    print("Loaded nodes into KùzuDB")

    # Ingest edges
    create_edge_tables(conn)
    conn.execute(f"COPY TransactedWith FROM '{DATA_PATH}/transacted_with.csv';")
    conn.execute(f"COPY BelongsTo FROM '{DATA_PATH}/belongs_to.csv';")
    conn.execute(f"COPY LocatedIn FROM '{DATA_PATH}/located_in.csv';")
    print("Loaded edges into KùzuDB")

if __name__ == "__main__":
    DB_NAME = "transaction_db"
    # Delete directory each time till we have MERGE FROM available in kuzu
    if os.path.exists(DB_NAME):
        shutil.rmtree(DB_NAME)
    # Create database
    db = kuzu.Database(f"./{DB_NAME}")
    conn = kuzu.Connection(db)

    DATA_PATH = "./data"

    main(conn, DATA_PATH)
