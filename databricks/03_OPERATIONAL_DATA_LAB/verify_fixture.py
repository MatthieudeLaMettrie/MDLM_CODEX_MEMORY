"""Independent fixture oracle; standard library only. Does not execute Spark.

Resolve the greatest sequence across all observed valid events, independently
of the notebook's per-batch merge, then reconcile against fixed expected data.
Run: python databricks/03_OPERATIONAL_DATA_LAB/verify_fixture.py
"""
import csv
import json
from collections import defaultdict
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path

HERE = Path(__file__).resolve().parent
STORES = {"S01": "Sydney", "S02": "Newcastle"}


def parse(row):
    reasons = []
    for field in ("source_system", "event_id", "order_id"):
        if not row[field].strip():
            reasons.append(f"missing_{field}")
    try:
        sequence = int(row["sequence_raw"])
        if sequence < 0:
            raise ValueError
    except ValueError:
        sequence = None
        reasons.append("invalid_sequence")
    try:
        day = date.fromisoformat(row["order_date_raw"])
        datetime.fromisoformat(row["event_ts_raw"])
    except ValueError:
        day = None
        reasons.append("invalid_date_or_timestamp")
    op = row["op"].strip().upper()
    if op not in {"UPSERT", "DELETE"}:
        reasons.append("invalid_op")
    try:
        amount = Decimal(row["amount_raw"]).quantize(Decimal("0.01"))
        if not amount.is_finite():
            raise InvalidOperation
    except InvalidOperation:
        amount = None
    if op == "UPSERT":
        if amount is None or amount < 0:
            reasons.append("invalid_amount")
        for field in ("store_id", "customer_id"):
            if not row[field].strip():
                reasons.append(f"missing_{field}")
    return ({**row, "sequence": sequence, "day": day, "amount": amount, "op": op}, reasons)


def resolve(rows):
    lines = {}
    for row in rows:
        line = row["line_id"]
        if line in lines and lines[line] != row:
            raise ValueError("Source line identity changed")
        lines[line] = row
    rejected, valid = [], []
    event_payloads = {}
    for row in lines.values():
        event_key = (row["source_system"], row["event_id"])
        signature = tuple(v for k, v in row.items() if k not in {"line_id", "batch_id"})
        if event_key in event_payloads and event_payloads[event_key] != signature:
            raise ValueError("Contradictory event identity")
        event_payloads[event_key] = signature
        typed, reasons = parse(row)
        (rejected if reasons else valid).append(typed)

    by_key = defaultdict(list)
    sequence_payloads = {}
    for row in valid:
        key = (row["source_system"], row["order_id"])
        sequence_key = (*key, row["sequence"])
        payload = (row["op"], row["store_id"], row["customer_id"], row["day"], row["amount"])
        if sequence_key in sequence_payloads and sequence_payloads[sequence_key] != payload:
            raise ValueError("Contradictory sequence")
        sequence_payloads[sequence_key] = payload
        by_key[key].append(row)
    # Global latest-state oracle, not a simulation of Delta transactions.
    state = {key: max(events, key=lambda r: (r["sequence"], r["event_id"]))
             for key, events in by_key.items()}
    active = [r for r in state.values() if r["op"] != "DELETE"]
    totals = defaultdict(lambda: [0, Decimal("0.00")])
    for row in active:
        key = (str(row["day"]), row["store_id"], STORES.get(row["store_id"], "Unknown"))
        totals[key][0] += 1
        totals[key][1] += row["amount"]
    result = {
        "bronze_lines": len(lines), "quarantine_lines": len(rejected),
        "state_rows": len(state), "active_orders": len(active),
        "active_amount": f"{sum((r['amount'] for r in active), Decimal('0.00')):.2f}",
        "gold": [[*key, count, f"{amount:.2f}"]
                 for key, (count, amount) in sorted(totals.items())],
    }
    assert len(lines) == len(rejected) + len(valid)
    return result, state


def main():
    with (HERE / "data/order_events.csv").open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    expected = json.loads((HERE / "data/expected_results.json").read_text(encoding="utf-8"))
    prefix = []
    for batch in ("B1", "B2", "B3"):
        prefix += [r for r in rows if r["batch_id"] == batch]
        actual, state = resolve(prefix)
        assert actual == expected[batch], (batch, actual, expected[batch])
        assert resolve(list(reversed(prefix)))[0] == actual, "Ordering changed latest state"
        assert resolve(prefix + prefix)[0] == actual, "Re-delivery changed result"
        if batch != "B1":
            assert state[("POS", "1002")]["op"] == "DELETE"
            assert state[("POS", "1002")]["sequence"] == 2
        print(f"{batch}: {actual['bronze_lines']} raw lines, "
              f"{actual['active_orders']} active orders, amount {actual['active_amount']}")
    assert resolve(rows)[0] == resolve(rows + [r for r in rows if r["batch_id"] == "B1"])[0]
    for changed, expected_error in (
        ({**rows[0], "amount_raw": "999.00"}, "Source line identity changed"),
        ({**rows[0], "line_id": "CONFLICT-1", "amount_raw": "999.00"}, "Contradictory event identity"),
        ({**rows[0], "line_id": "CONFLICT-2", "event_id": "new-event",
          "amount_raw": "999.00"}, "Contradictory sequence"),
    ):
        try:
            resolve(rows + [changed])
        except ValueError as error:
            assert str(error) == expected_error, error
        else:
            raise AssertionError(f"Expected oracle to detect {expected_error}")
    print("Fixture arithmetic, attribution, replay, ordering and conflict checks passed.")
    print("Spark notebook and Databricks bundle execution remain unverified.")


if __name__ == "__main__":
    main()
