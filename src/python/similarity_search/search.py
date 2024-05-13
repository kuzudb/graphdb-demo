import kuzu
import warnings
from sentence_transformers import SentenceTransformer
warnings.filterwarnings("ignore")

model = SentenceTransformer("Snowflake/snowflake-arctic-embed-xs")

# Create database
db = kuzu.Database("./vdb")
conn = kuzu.Connection(db)

def get_embedding(query_item: str) -> list[float]:
    return model.encode(query_item).tolist()


if __name__ == "__main__":
    query_item = "coffee maker"
    query_vector = get_embedding(query_item)
    res = conn.execute(
        """
        MATCH (p:Person)-[:Purchased]->(i:Item)
        WITH p, i, CAST($query_vector, "DOUBLE[384]") AS query_vector
        RETURN
          p.name as person,
          p.age as age,
          i.name as item,
          array_cosine_similarity(i.vector, query_vector) AS similarity
        ORDER BY similarity DESC, age
        """,
        parameters={"query_vector": query_vector}
    )
    print(res.get_as_pl())
