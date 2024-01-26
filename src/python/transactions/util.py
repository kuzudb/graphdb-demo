from __future__ import annotations

import csv
from pathlib import Path


def format_path(data_path: str | Path) -> Path:
    if isinstance(data_path, str):
        data_path = Path(data_path)
    return data_path


def create_transaction_edge_file(data_path: str | Path) -> None:
    """
    Transform transaction.csv into transacted_with.csv edge file
    with the correct headers.
    """
    data_path = format_path(data_path)
    with open(data_path / "transaction.csv") as transaction:
        transaction_reader = csv.reader(transaction)
        next(transaction_reader, None)  # skip the headers
        with open(data_path / "transacted_with.csv", "w") as transaction_edges:
            transaction_edges_writer = csv.writer(transaction_edges)
            colnames = ["from", "to", "amount_usd", "timestamp"]
            transaction_edges_writer.writerow(colnames)

            for row in transaction_reader:
                transaction_edges_writer.writerow(row[1:])
    print(f"Created edge file '{data_path}/transacted_with.csv'")


def create_merchant_instance_edge_file(data_path) -> None:
    """
    Transform merchant.csv into has_instance.csv edge file.
    This contains edges from company to merchant.
    """
    data_path = format_path(data_path)
    with open(data_path / "merchant.csv") as merchant:
        merchant_reader = csv.reader(merchant)
        next(merchant_reader, None)  # skip the headers
        with open(data_path / "has_instance.csv", "w") as merchant_edges:
            merchant_edges_writer = csv.writer(merchant_edges)
            colnames = ["from", "to"]
            merchant_edges_writer.writerow(colnames)

            for row in merchant_reader:
                merchant_edges_writer.writerow([row[1], row[0]])
    print(f"Created edge file '{data_path}/has_instance.csv'")


def create_merchant_city_edge_file(data_path) -> None:
    """
    Transform merchant.csv into located_in.csv edge file.
    This contains edges from merchant to city.
    """
    data_path = format_path(data_path)
    with open(data_path / "merchant.csv") as merchant:
        merchant_reader = csv.reader(merchant)
        next(merchant_reader, None)  # skip the headers
        with open(data_path / "located_in.csv", "w") as merchant_edges:
            merchant_edges_writer = csv.writer(merchant_edges)
            colnames = ["from", "to"]
            merchant_edges_writer.writerow(colnames)

            for row in merchant_reader:
                merchant_edges_writer.writerow([row[0], row[2]])
    print(f"Created edge file '{data_path}/located_in.csv'")


if __name__ == "__main__":
    data_path = Path("./data")
    create_transaction_edge_file(data_path)
    create_merchant_instance_edge_file(data_path)
    create_merchant_city_edge_file(data_path)
