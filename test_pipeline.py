from src.pipeline import build_gold


def test_duplicate_events_are_removed():
    gold, quality = build_gold()
    assert quality["source_transactions"] == 8
    assert quality["duplicate_events_removed"] == 1
    assert len(gold) == 7


def test_gold_has_no_orphan_customers():
    _, quality = build_gold()
    assert quality["orphan_account_ids"] == 0


def test_signed_amount_has_expected_direction():
    gold, _ = build_gold()
    deposits = gold.loc[gold["event_type"] == "Deposit", "signed_amount"]
    withdrawals = gold.loc[gold["event_type"] == "Withdrawal", "signed_amount"]
    assert (deposits > 0).all()
    assert (withdrawals < 0).all()

