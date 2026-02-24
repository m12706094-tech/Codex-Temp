import pytest

from app.db import init_db
from app.main import chat, query_spec, usage_summary


def setup_module():
    init_db()


def test_chat_total_revenue():
    body = chat("tenant_alpha", "analyst", "s1", "What is total revenue?")
    assert body["intent"] == "total_revenue"
    assert body["query"].strip().lower().startswith("select")
    assert "answer" in body


def test_query_spec_select_only():
    body = query_spec("Show monthly revenue trend")
    assert body["intent"] == "monthly_trend"
    assert body["query"].strip().lower().startswith("select")


def test_usage_summary_increments():
    chat("tenant_alpha", "viewer", "s2", "What is total revenue?")
    usage = usage_summary("tenant_alpha")
    assert usage["usage"]


def test_role_restricted():
    with pytest.raises(PermissionError):
        chat("tenant_alpha", "guest", "s3", "What is total revenue?")
