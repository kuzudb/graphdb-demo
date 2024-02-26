from typing import Any

import kuzu
import networkx as nx
import pandas as pd


def get_closeness_centrality(conn: kuzu.Connection) -> pd.DataFrame:
    """
    Get closeness centrality for merchant nodes
    """
    clients_and_merchants = conn.execute(
        """
        MATCH (c:Client)-[t:TransactedWith]->(m:Merchant)
        RETURN *;
        """
    )
    # Convert to networkx DiGraph
    G = clients_and_merchants.get_as_networkx(directed=True)
    # Get closeness centrality for merchants
    closeness_centrality = nx.closeness_centrality(G).items()
    df = pd.DataFrame(closeness_centrality, columns=["node_id", "closeness_centrality"])
    df = df[df["node_id"].str.startswith("Merchant_")]
    df["node_id"] = df["node_id"].str.replace("Merchant_", "").astype(int)
    df = df.sort_values(by="closeness_centrality", ascending=False).reset_index(drop=True)
    print(f"\n---\nTop 5 merchants by closeness centrality for node type Merchant:\n{df.head()}")
    return df


def get_weakly_connected_components(conn: kuzu.Connection) -> list[set[Any]]:
    """
    Get weakly connected components for the vicinity of disputed transactions -- includes a combination
    of client and merchant nodes
    """
    disputed_vicinity = conn.execute(
        """
        MATCH (c1:Client)-[t1:TransactedWith]->(m:Merchant)<-[t2:TransactedWith]-(c2:Client)
        WHERE t1.is_disputed = true
        RETURN *;
        """
    )
    # Convert to networkx DiGraph
    G = disputed_vicinity.get_as_networkx(directed=True)
    # Get weakly connected components
    weakly_connected_components = list(nx.weakly_connected_components(G))
    print(f"\n---\nNumber of weakly connected components: {len(weakly_connected_components)}")
    for i, component in enumerate(weakly_connected_components, 1):
        print(f"Number of nodes in component {i}: {len(component)}")
    return weakly_connected_components


def main(conn: kuzu.Connection):
    _ = get_weakly_connected_components(conn)
    _ = get_closeness_centrality(conn)


if __name__ == "__main__":
    db = kuzu.Database("./transaction_db")
    conn = kuzu.Connection(db)

    main(conn)
