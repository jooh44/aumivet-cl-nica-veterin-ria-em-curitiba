"""Lê o histórico recente de mudanças na conta para reconstruir o que foi alterado."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from core.client import get_client, CUSTOMER_ID
from core.reports import _query


def changes(days: int = 14):
    print(f"=== CHANGE EVENTS últimos {days}d ===")
    gaql = f"""
        SELECT
            change_event.change_date_time,
            change_event.user_email,
            change_event.client_type,
            change_event.change_resource_type,
            change_event.resource_change_operation,
            change_event.campaign,
            change_event.changed_fields,
            change_event.old_resource,
            change_event.new_resource
        FROM change_event
        WHERE change_event.change_date_time DURING LAST_14_DAYS
        ORDER BY change_event.change_date_time DESC
        LIMIT 200
    """
    for row in _query(gaql):
        ce = row.change_event
        fields = str(ce.changed_fields).replace("\n", " ")
        print(
            f"  {ce.change_date_time}  {ce.resource_change_operation.name:8}  "
            f"{ce.change_resource_type.name:30}  by {ce.user_email}  "
            f"fields={fields[:120]}"
        )
        old = str(ce.old_resource).replace("\n", " | ")[:200]
        new = str(ce.new_resource).replace("\n", " | ")[:200]
        if old.strip():
            print(f"     OLD: {old}")
        if new.strip():
            print(f"     NEW: {new}")


if __name__ == "__main__":
    changes()
