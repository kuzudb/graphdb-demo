import kuzu


def query_1(conn: kuzu.Connection) -> None:
    "Q1. Who are the clients that transacted with the merchants of 'Starbucks'?"
    query = """
        MATCH (c:Client)-[:TransactedWith]->(:Merchant)-[:BelongsTo]->(co:Company)
        WHERE co.company = "Starbucks"
        RETURN DISTINCT c.client_id AS id, c.name AS name;
    """
    print(f"\nQuery 1:\n {query}")
    response = conn.execute(query)
    result = response.get_as_df()
    print(result)
    return result


def query_2(conn: kuzu.Connection) -> None:
    "Q2. Who are the clients who transacted with at least 2 separate merchants operating in Los Angeles?"
    query = """
        MATCH (c:Client)-[:TransactedWith]->(m1:Merchant)-[:LocatedIn]->(ci:City),
            (c)-[:TransactedWith]->(m2:Merchant)-[:LocatedIn]->(ci)
        WHERE ci.city = "Los Angeles" AND m1.merchant_id <> m2.merchant_id
        RETURN DISTINCT c.client_id AS id, c.name as name;
    """
    print(f"\nQuery 2:\n {query}")
    response = conn.execute(query)
    result = response.get_as_df()
    print(result)
    return result


def query_3(conn: kuzu.Connection) -> None:
    "Q3. Which companies have merchants in New York City, Boston **and** Los Angeles?"
    query = """
        MATCH (:City {city: "New York City"})<-[]-(m1:Merchant)-[]->(co:Company),
            (:City {city: "Boston"})<-[]-(m2)-[]->(co),
            (:City {city: "Los Angeles"})<-[]-(m3)-[]->(co)
        RETURN DISTINCT co.company AS company
    """
    print(f"\nQuery 3:\n {query}")
    response = conn.execute(query)
    result = response.get_as_df()
    print(result)
    return result


def query_4(conn: kuzu.Connection) -> None:
    "Q4. How many common connections (cities, merchants, companies) exist between Client IDs 4 and 5?"
    query = """
        MATCH (c1:Client)-[*1..2]->(common)<-[*1..2]-(c2:Client)
        WHERE c1.client_id = 4 AND c2.client_id = 5
        RETURN label(common) AS connectionType, COUNT(label(common)) AS count;
    """
    print(f"\nQuery 4:\n {query}")
    response = conn.execute(query)
    result = response.get_as_df()
    print(result)
    return result


def main(conn: kuzu.Connection) -> None:
    query_1(conn)
    query_2(conn)
    query_3(conn)
    query_4(conn)


if __name__ == "__main__":
    DB_NAME = "transaction_db"
    # Create database
    db = kuzu.Database(f"./{DB_NAME}")
    conn = kuzu.Connection(db)

    main(conn)
