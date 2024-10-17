import shutil

import kuzu

shutil.rmtree("ex_kuzu_db", ignore_errors=True)
db = kuzu.Database("ex_kuzu_db")
conn = kuzu.Connection(db)

conn.execute("INSTALL duckdb; LOAD EXTENSION duckdb;")
conn.execute("ATTACH 'person.duckdb' AS travel (dbtype duckdb);")

conn.execute("""
    CREATE NODE TABLE Person (
        name STRING,
        age UINT8,
        is_frequent_flyer BOOLEAN DEFAULT false,
        PRIMARY KEY (name)
    );
""")
conn.execute("CREATE NODE TABLE City (name STRING, PRIMARY KEY (name));")
conn.execute("CREATE REL TABLE LIVES_IN (FROM Person TO City);")
conn.execute("CREATE REL TABLE TRAVELS_TO (FROM Person TO City);")

# Copy directly from DuckDB tables
conn.execute(
    """
    COPY Person(name, age) FROM (
        LOAD FROM travel.person
        RETURN name, CAST(age AS UINT8)
    );
    """
)

conn.execute("""
    COPY City FROM (
        LOAD FROM travel.person
        RETURN DISTINCT lives_in
    );
    """)

conn.execute("""
    COPY LIVES_IN FROM (
        LOAD FROM travel.person
        RETURN name, lives_in
    );
    """)

conn.execute("""
    COPY TRAVELS_TO FROM (
        LOAD FROM travel.travel
        RETURN name, travels_to
    );
    """)

# Read in the frequent flyer table
res = conn.execute("""
    LOAD FROM travel.frequent_flyer
    WITH name, flights_taken
    WHERE flights_taken > 2
    MERGE (p:Person {name: name})
    ON MATCH SET p.is_frequent_flyer = true
    ON CREATE SET p.is_frequent_flyer = true
""")

res = conn.execute("""
    MATCH (p:Person)
    RETURN p.name AS person,
           p.age AS age,
           p.is_frequent_flyer AS is_frequent_flyer
    ORDER BY is_frequent_flyer DESC, age;
""")
print(res.get_as_pl())
