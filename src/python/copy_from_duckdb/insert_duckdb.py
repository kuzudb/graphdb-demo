import duckdb

conn = duckdb.connect("person.duckdb")

conn.execute(
    """
    CREATE OR REPLACE TABLE person AS
    SELECT *
    FROM read_csv('travel/person.csv', header=true)
    """
)

conn.execute(
    """
    CREATE OR REPLACE TABLE travel AS
    SELECT *
    FROM read_csv('travel/travel.csv', header=true)
    """
)

conn.execute("""
    CREATE OR REPLACE TABLE frequent_flyer AS
    SELECT name, COUNT(DISTINCT travels_to) AS flights_taken
    FROM travel
    GROUP BY name
    ORDER BY flights_taken DESC;
""")

# Print the contents of the new table to verify
result = conn.execute("SELECT * FROM frequent_flyer LIMIT 3;")
print(result.fetchall())
