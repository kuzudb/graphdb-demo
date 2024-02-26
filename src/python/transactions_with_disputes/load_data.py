from __future__ import annotations

import os
import shutil

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
                transaction_id INT64,
                amount_usd FLOAT,
                timestamp TIMESTAMP,
                is_disputed BOOLEAN
            )
        """
    )
    conn.execute("CREATE REL TABLE LocatedIn(FROM Merchant TO City)")
    conn.execute("CREATE REL TABLE BelongsTo(FROM Merchant TO Company)")


def main(conn: kuzu.Connection) -> None:
    # Ingest nodes
    create_node_tables(conn)
    conn.execute(f"COPY Client FROM '{NODE_PATH}/client.csv' (header=true);")
    conn.execute(f"COPY City FROM '{NODE_PATH}/city.csv' (header=true);")
    conn.execute(f"COPY Company FROM '{NODE_PATH}/company.csv' (header=true);")
    conn.execute(f"COPY Merchant FROM '{NODE_PATH}/merchant.csv' (header=true);")
    print("Loaded nodes into KùzuDB")

    # Ingest edges
    create_edge_tables(conn)
    conn.execute(f"COPY TransactedWith FROM '{REL_PATH}/transacted_with.csv';")
    conn.execute(f"COPY BelongsTo FROM '{REL_PATH}/belongs_to.csv';")
    conn.execute(f"COPY LocatedIn FROM '{REL_PATH}/located_in.csv';")
    print("Loaded edges into KùzuDB")


if __name__ == "__main__":
    DB_NAME = "transaction_db"
    # Delete directory each time till we have MERGE FROM available in kuzu
    if os.path.exists(DB_NAME):
        shutil.rmtree(DB_NAME)
    # Create database
    db = kuzu.Database(f"./{DB_NAME}")
    conn = kuzu.Connection(db)

    NODE_PATH = "./data/node"
    REL_PATH = "./data/rel"

    main(conn)
