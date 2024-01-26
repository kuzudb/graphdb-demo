from __future__ import annotations

import os
import shutil
from pathlib import Path

import kuzu
import util


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


def create_node_tables(conn: kuzu.Connection) -> None:
    create_client_node_table(conn)
    create_city_node_table(conn)
    create_company_node_table(conn)
    create_merchant_node_table(conn)


def create_edge_tables(conn: kuzu.Connection) -> None:
    # Create edge schemas
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
    conn.execute("CREATE REL TABLE HasInstance(FROM Company TO Merchant)")


def main(conn: kuzu.Connection, data_path: Path) -> None:
    # Create edge table files from existing data
    util.create_transaction_edge_file(data_path)
    util.create_merchant_instance_edge_file(data_path)
    util.create_merchant_city_edge_file(data_path)

    # Ingest nodes
    create_node_tables(conn)
    conn.execute(f"COPY Client FROM '{data_path}/client.csv' (header=true);")
    conn.execute(f"COPY City FROM '{data_path}/city.csv' (header=true);")
    conn.execute(f"COPY Company FROM '{data_path}/company.csv' (header=true);")
    conn.execute(f"COPY Merchant FROM '{data_path}/merchant.csv' (header=true);")
    print("Successfully loaded nodes into KùzuDB!")

    # Ingest edges
    create_edge_tables(conn)
    conn.execute(f"COPY TransactedWith FROM '{data_path}/transacted_with.csv' (header=true);")
    conn.execute(f"COPY LocatedIn FROM '{data_path}/located_in.csv' (header=true);")
    conn.execute(f"COPY HasInstance FROM '{data_path}/has_instance.csv' (header=true);")
    print("Successfully loaded edges into KùzuDB!")


if __name__ == "__main__":
    DB_NAME = "transaction_db"
    # Delete directory each time till we have MERGE FROM available in kuzu
    if os.path.exists(DB_NAME):
        shutil.rmtree(DB_NAME)
    # Create database
    db = kuzu.Database(f"./{DB_NAME}")
    conn = kuzu.Connection(db)

    data_path = "./data"

    main(conn, data_path)
