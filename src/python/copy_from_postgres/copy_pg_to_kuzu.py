import shutil

import kuzu

shutil.rmtree("./ex_db_kuzu", ignore_errors=True)
db = kuzu.Database("./ex_db_kuzu")
conn = kuzu.Connection(db)

# --- Create node tables ---
conn.execute(
    """
    CREATE NODE TABLE Person (
        id INT32,
        name STRING,
        email STRING,
        PRIMARY KEY (id)
    )
    """
)

conn.execute(
    """
    CREATE NODE TABLE Address (
        address STRING,
        PRIMARY KEY (address)
    )
    """
)

conn.execute(
    """
    CREATE NODE TABLE Account (
        id INT32,
        account_id STRING,
        balance FLOAT,
        PRIMARY KEY (id)
    )
    """
)

# --- Create relationship tables ---
conn.execute("CREATE REL TABLE Owns (FROM Person TO Account)")
conn.execute("CREATE REL TABLE LivesIn (FROM Person TO Address)")
conn.execute(
    """
    CREATE REL TABLE Transfer (
        FROM Account TO Account,
        amount FLOAT,
        transaction_id STRING
    )
    """
)

# --- Attach Postgres DB ---
PG_CONNECTION_STRING = (
    "dbname=postgres user=postgres host=localhost password=testpassword port=5432"
)

conn.execute("INSTALL postgres;")
# Install and load Postgres extension
conn.execute("LOAD EXTENSION postgres;")
# Attach Postgres database
conn.execute(
    f"""
    ATTACH '{PG_CONNECTION_STRING}' AS pg_db (
        dbtype postgres,
        skip_unsupported_table=false
    )
    """
)

# --- Copy nodes ---
conn.execute("COPY Person FROM (LOAD FROM pg_db.person RETURN id, name, email)")
conn.execute("COPY Account FROM (LOAD FROM pg_db.account RETURN id, account_id, balance)")
conn.execute("COPY Address FROM (LOAD FROM pg_db.person RETURN DISTINCT address)")

# --- Copy relationships ---

conn.execute("COPY Owns FROM (LOAD FROM pg_db.account RETURN owner, id)")
conn.execute("COPY LivesIn FROM (LOAD FROM pg_db.person RETURN id, address)")
conn.execute("COPY Transfer FROM pg_db.transfer")
