# /// script
# dependencies = [
#   "kuzu==0.10.0",
#   "polars==1.29.0",
#   "pyarrow==20.0.0",
#   "yfiles_jupyter_graphs_for_kuzu==0.0.4",
#   "networkx==3.4.2",
# ]
# ///
import shutil

import kuzu
import networkx as nx
import polars as pl
from yfiles_jupyter_graphs_for_kuzu import KuzuGraphWidget

# Create a new database and connection object
shutil.rmtree("test_db", ignore_errors=True)
db = kuzu.Database("test_db")
conn = kuzu.Connection(db)

# Install the unity catalog and attach the unity database
conn.execute("INSTALL unity_catalog; LOAD unity_catalog;")
conn.execute("ATTACH 'unity' AS unity (dbtype UC_CATALOG);")

# Create node and relationship tables (define the schema)
conn.execute("CREATE NODE TABLE Person(pname STRING PRIMARY KEY, age INT64);")
conn.execute("CREATE NODE TABLE Country(cname STRING PRIMARY KEY);")
conn.execute("CREATE REL TABLE LIVES_IN(FROM Person TO Country);")

# Copy data from the Unity catalog to the node and relationship tables
conn.execute(
    """
    COPY Person FROM (
        LOAD FROM unity.user_countries
        RETURN first_name AS pname, age
    )
    """
)

conn.execute(
    """
    COPY Country FROM (
        LOAD FROM unity.user_countries
        RETURN DISTINCT country AS cname
    )
    """
)

conn.execute(
    """
    COPY LIVES_IN FROM (
        LOAD FROM unity.user_countries
        RETURN first_name AS pname, country AS cname
    )
    """
)

# Execute a Cypher query to retrieve the data
res = conn.execute(
    """
    MATCH (p:Person)-[:LIVES_IN]->(c:Country)
    RETURN p.pname, c.cname;
    """
)
res.get_as_pl()  # type: ignore

print("Finished inserting data into the database.")

# Visualize the graph!
g = KuzuGraphWidget(conn)

g.show_cypher("MATCH (p:Person)-[l:LIVES_IN]->(c:Country) RETURN *")

# Transform the graph to a NetworkX graph
networkx_graph = conn.execute(
    """
    MATCH (p:Person)-[l:LIVES_IN]->(c:Country)
    RETURN *
    """
).get_as_networkx(directed=True)    # type: ignore

# Calculate the degree centrality metric for Person and Country nodes using NetworkX
degree_centrality = nx.degree_centrality(networkx_graph)

degree_centrality_df = pl.DataFrame({"name": k, "degree_centrality": v} for k, v in degree_centrality.items())
degree_centrality_df = degree_centrality_df.with_columns(
    pl.col("name").str.split("_").list.first().alias("type")
)
degree_centrality_df = (
    degree_centrality_df.with_columns(
        pl.col("name").str.replace("Person_", "").str.replace("Country_", ""),
    )
)

# Let's add new degree centrality columns to the Person and Country tables
conn.execute(
    """
    ALTER TABLE Person ADD degree_centrality DOUBLE DEFAULT 0.0;
    ALTER TABLE Country ADD degree_centrality DOUBLE DEFAULT 0.0;
    """
)

# Copy the degree centrality values from the NetworkX results to the Person table
conn.execute(
    """
    LOAD FROM degree_centrality_df
    WITH name AS pname, degree_centrality
    MATCH (p:Person {pname: pname})
    SET p.degree_centrality = degree_centrality
    """
)

# Copy the degree centrality values from the NetworkX results to the Country table
conn.execute(
    """
    LOAD FROM degree_centrality_df
    WITH name AS cname, degree_centrality
    MATCH (c:Country {cname: cname})
    SET c.degree_centrality = degree_centrality
    """
)

# Visualize the graph again!
g.show_cypher("MATCH (p:Person)-[l:LIVES_IN]->(c:Country) RETURN *")

# See which countries have the highest degree centrality
res = conn.execute(
    """
    MATCH (c:Country)
    RETURN c.cname, c.degree_centrality
    ORDER BY c.degree_centrality DESC
    """
)
res.get_as_pl()    # type: ignore

print("Finished the workflow!")
