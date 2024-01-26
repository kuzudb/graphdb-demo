import kuzu


def query_1(conn: kuzu.Connection) -> None:
    "Which cities have the most merchant transactions?"
    query = """
        MATCH (:Client)-[t:TransactedWith]->(m:Merchant)-[:LocatedIn]->(city:City)
        RETURN city.city as city, COUNT(t) AS numTransactions
        ORDER BY numTransactions DESC LIMIT 5;
    """
    print(f"\nQuery 1:\n {query}")
    response = conn.execute(query)
    result = response.get_as_df()
    print(result)
    return result


def query_2(conn: kuzu.Connection) -> None:
    "Which company type does the merchant with the most transactions belong to?"
    query = """
        MATCH (:Client)-[t:TransactedWith]->(:Merchant)<-[:HasInstance]-(co:Company)
        RETURN co.type as companyType, COUNT(t) AS numTransactions
        ORDER BY numTransactions DESC LIMIT 1;
    """
    print(f"\nQuery 1:\n {query}")
    response = conn.execute(query)
    result = response.get_as_df()
    print(result)
    return result


def query_3(conn: kuzu.Connection) -> None:
    "Which companies have the most clients in Boston, and what is their average age?"
    query = """
        MATCH (ci:City)<-[:LocatedIn]-(m:Merchant)
        WHERE ci.city = "Boston"
        WITH ci, m
        MATCH (client:Client)-[:TransactedWith]-(m)<-[:HasInstance]-(co:Company)
        RETURN co.company as company, AVG(client.age) AS avgAge
        ORDER BY avgAge
    """
    print(f"\nQuery 1:\n {query}")
    response = conn.execute(query)
    result = response.get_as_df()
    print(result)
    return result


def main(conn: kuzu.Connection) -> None:
    query_1(conn)
    query_2(conn)
    query_3(conn)


if __name__ == "__main__":
    DB_NAME = "transaction_db"
    # Create database
    db = kuzu.Database(f"./{DB_NAME}")
    conn = kuzu.Connection(db)

    main(conn)
