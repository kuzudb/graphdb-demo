import os
import shutil
import kuzu


def create_db(conn):
    conn.execute(
        """
        CREATE NODE TABLE Person(
            id UINT64,
            name STRING,
            age UINT8,
            PRIMARY KEY (id)
        )
        """
    )

    conn.execute(
        """
        CREATE NODE TABLE Item(
            id UINT64,
            name STRING,
            vector DOUBLE[],
            PRIMARY KEY (id)
        )
        """
    )

    conn.execute(
        """
        CREATE REL TABLE Purchased(
            FROM Person
            TO Item
        )
        """
    )

def get_embedding(query_item: str) -> list[float]:
    import warnings
    from sentence_transformers import SentenceTransformer
    warnings.filterwarnings("ignore")

    model = SentenceTransformer("Snowflake/snowflake-arctic-embed-xs")

    return model.encode(query_item).tolist()


def write_data_to_parquet():
    import polars as pl

    persons = [
        {"id": 1, "name": "Karissa", "age": 25},
        {"id": 2, "name": "Zhang", "age": 29},
        {"id": 3, "name": "Noura", "age": 31},
    ]

    items = [
        {"id": 1, "name": "espresso machine", "vector": get_embedding("espresso machine")},
        {"id": 2, "name": "yoga mat", "vector": get_embedding("yoga mat")},
    ]

    purchased = [
        {"from": 1, "to": 1},
        {"from": 1, "to": 2},
        {"from": 2, "to": 1},
        {"from": 3, "to": 2},
    ]

    df_persons = pl.DataFrame(persons).with_columns(
        pl.col("id").cast(pl.UInt64),
        pl.col("age").cast(pl.UInt8),
    )
    df_items = pl.DataFrame(items).with_columns(
        pl.col("id").cast(pl.UInt64),
        pl.col("vector").cast(pl.Array(pl.Float64, width=384)),
    )
    df_purchased = pl.DataFrame(purchased).with_columns(
        pl.col("from").cast(pl.UInt64),
        pl.col("to").cast(pl.UInt64),
    )
    print(df_persons)
    print(df_items)
    df_persons.write_parquet("persons.parquet")
    df_items.write_parquet("items.parquet")
    df_purchased.write_parquet("purchased.parquet")


def build_graph(conn):
    conn.execute(
        """
        COPY Person FROM 'persons.parquet';
        COPY Item FROM 'items.parquet';
        COPY Purchased FROM 'purchased.parquet';
        """
    )
    print("Finished importing nodes and rels")


if __name__ == "__main__":
    if os.path.exists("./vdb"):
        shutil.rmtree("./vdb")

    # Create database
    db = kuzu.Database("./vdb")
    conn = kuzu.Connection(db)
    create_db(conn)

    write_data_to_parquet()

    # Load data from parquet to graph
    build_graph(conn)


