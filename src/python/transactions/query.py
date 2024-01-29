import kuzu


def query_1(conn: kuzu.Connection) -> None:
    "Who are the clients that made transactions in at least one of the merchants with IDs 2 and 11?"
    query = """
        MATCH (m1:Merchant {merchant_id: 7})<-[:TransactedWith]-(a:Client)-[:TransactedWith]->(m2:Merchant {merchant_id: 11}),
        (b:Client)-[:TransactedWith]->(m3:Merchant)
        RETURN DISTINCT b.client_id AS id, b.name as name
    """
    print(f"\nQuery 1:\n {query}")
    response = conn.execute(query)
    result = response.get_as_df()
    print(result)
    return result


def query_2(conn: kuzu.Connection) -> None:
    "Which city has the most merchant transactions?"
    query = """
        MATCH (:Client)-[t:TransactedWith]->(m:Merchant)-[:LocatedIn]->(city:City)
        RETURN city.city as city, COUNT(t) AS numTransactions
        ORDER BY numTransactions DESC LIMIT 1;
    """
    print(f"\nQuery 2:\n {query}")
    response = conn.execute(query)
    result = response.get_as_df()
    print(result)
    return result


def query_3(conn: kuzu.Connection) -> None:
    "Which company has the most merchants?"
    query = """
        MATCH (m:Merchant)-[:BelongsTo]->(co:Company)
        RETURN co.company AS company, COUNT(m) AS numMerchants
        ORDER BY numMerchants DESC LIMIT 1;
    """
    print(f"\nQuery 3:\n {query}")
    response = conn.execute(query)
    result = response.get_as_df()
    print(result)
    return result


def query_4(conn: kuzu.Connection) -> None:
    "Which company has the most merchant transactions above 100 dollars?"
    query = """
        MATCH (:Client)-[t:TransactedWith]-(:Merchant)-[:BelongsTo]->(co:Company)
        WHERE t.amount_usd > 100
        RETURN co.company AS company, COUNT(t) AS numTransactions
        ORDER BY numTransactions DESC LIMIT 1;
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
