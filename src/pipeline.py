"""Small, reviewable analytics pipeline using synthetic financial-services data."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"


def read_sources() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    customers = pd.read_csv(RAW / "customers.csv")
    accounts = pd.read_csv(RAW / "accounts.csv")
    transactions = pd.read_csv(RAW / "transactions.csv")
    return customers, accounts, transactions


def build_gold() -> tuple[pd.DataFrame, dict[str, int]]:
    customers, accounts, transactions = read_sources()

    customers["created_date"] = pd.to_datetime(customers["created_date"], utc=True)
    accounts["opened_date"] = pd.to_datetime(accounts["opened_date"], utc=True)
    transactions["event_timestamp"] = pd.to_datetime(transactions["event_timestamp"], utc=True)

    # Keep the latest copy of a retried event and preserve a measurable audit count.
    before_dedup = len(transactions)
    transactions = transactions.sort_values("event_timestamp").drop_duplicates("event_id", keep="last")
    duplicate_events_removed = before_dedup - len(transactions)

    valid_types = {"Deposit", "Withdrawal", "Fee"}
    invalid_types = int((~transactions["event_type"].isin(valid_types)).sum())
    negative_amounts = int((transactions["amount"] < 0).sum())

    gold = (
        transactions.merge(accounts, on="account_id", how="left", validate="many_to_one")
        .merge(customers, on="customer_id", how="left", validate="many_to_one")
        .assign(
            event_date=lambda frame: frame["event_timestamp"].dt.date.astype(str),
            signed_amount=lambda frame: frame["amount"].where(
                frame["event_type"].eq("Deposit"), -frame["amount"]
            ),
            is_exception=lambda frame: frame["status"].ne("Active"),
        )
    )

    quality = {
        "source_transactions": before_dedup,
        "duplicate_events_removed": duplicate_events_removed,
        "invalid_event_types": invalid_types,
        "negative_amounts": negative_amounts,
        "orphan_account_ids": int(gold["customer_id"].isna().sum()),
        "gold_rows": len(gold),
    }
    return gold, quality


def run() -> dict[str, int]:
    gold, quality = build_gold()
    PROCESSED.mkdir(parents=True, exist_ok=True)
    gold.to_csv(PROCESSED / "fact_transactions.csv", index=False)
    pd.DataFrame([quality]).to_csv(PROCESSED / "pipeline_quality_summary.csv", index=False)
    print("Pipeline completed")
    for key, value in quality.items():
        print(f"- {key}: {value}")
    return quality


if __name__ == "__main__":
    run()

