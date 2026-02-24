from __future__ import annotations

from collections import defaultdict
import json
import sqlite3
from typing import Any

from app.db import get_conn, init_db, track_usage

ALLOWED_ROLES = {"viewer", "analyst", "admin"}
SESSIONS: dict[str, list[str]] = defaultdict(list)


def detect_intent(msg: str) -> str:
    text = msg.lower()
    if "total revenue" in text:
        return "total_revenue"
    if "monthly" in text and "trend" in text:
        return "monthly_trend"
    if "daily" in text and "revenue" in text:
        return "daily_revenue"
    if "by country" in text or "between" in text:
        return "revenue_by_country"
    if "by city" in text:
        return "revenue_by_city"
    if "by product" in text or "product performance" in text:
        return "revenue_by_product"
    if "average deal" in text:
        return "average_deal_size"
    if "top customers" in text:
        return "top_customers"
    if "concentration" in text:
        return "revenue_concentration"
    if "mom" in text or "month-over-month" in text:
        return "mom_growth"
    if "compare" in text:
        return "revenue_comparison"
    if "why did revenue drop" in text or "why" in text:
        return "diagnostic_drop"
    return "clarification_needed"


def generate_query(intent: str) -> dict[str, str]:
    mapping = {
        "total_revenue": "SELECT SUM(price) AS total_revenue FROM sales WHERE tenant_id = :tenant_id",
        "monthly_trend": "SELECT substr(date,1,7) AS month, SUM(price) AS revenue FROM sales WHERE tenant_id = :tenant_id GROUP BY substr(date,1,7) ORDER BY month",
        "daily_revenue": "SELECT date, SUM(price) AS revenue FROM sales WHERE tenant_id = :tenant_id GROUP BY date ORDER BY date",
        "revenue_by_country": "SELECT country, SUM(price) AS revenue FROM sales WHERE tenant_id = :tenant_id GROUP BY country ORDER BY revenue DESC",
        "revenue_by_city": "SELECT city, SUM(price) AS revenue FROM sales WHERE tenant_id = :tenant_id GROUP BY city ORDER BY revenue DESC",
        "revenue_by_product": "SELECT product, SUM(price) AS revenue FROM sales WHERE tenant_id = :tenant_id GROUP BY product ORDER BY revenue DESC",
        "average_deal_size": "SELECT AVG(price) AS average_deal_size FROM sales WHERE tenant_id = :tenant_id",
        "top_customers": "SELECT name, SUM(price) AS revenue FROM sales WHERE tenant_id = :tenant_id GROUP BY name ORDER BY revenue DESC LIMIT 5",
        "revenue_concentration": "SELECT name, SUM(price) AS revenue FROM sales WHERE tenant_id = :tenant_id GROUP BY name ORDER BY revenue DESC LIMIT 10",
        "mom_growth": "SELECT substr(date,1,7) AS month, SUM(price) AS revenue FROM sales WHERE tenant_id = :tenant_id GROUP BY substr(date,1,7) ORDER BY month",
        "revenue_comparison": "SELECT country, SUM(price) AS revenue FROM sales WHERE tenant_id = :tenant_id GROUP BY country ORDER BY revenue DESC",
        "diagnostic_drop": "SELECT substr(date,1,7) AS month, product, SUM(price) AS revenue FROM sales WHERE tenant_id = :tenant_id GROUP BY month, product ORDER BY month",
    }
    return {"intent": intent, "query": mapping.get(intent, "")}


def validate_query(query: str) -> None:
    q = query.strip().lower()
    if not q.startswith("select"):
        raise ValueError("Only SELECT queries are allowed.")
    forbidden = ["insert", "update", "delete", "drop", "alter", "pragma"]
    if any(token in q for token in forbidden):
        raise ValueError("Destructive query blocked.")
    if " from sales " not in f" {q} ":
        raise ValueError("Only sales table is allowed.")


def run_query(conn: sqlite3.Connection, query: str, tenant_id: str) -> list[dict[str, Any]]:
    cur = conn.execute(query, {"tenant_id": tenant_id})
    return [dict(r) for r in cur.fetchall()]


def recommend_visualization(intent: str) -> str:
    if intent in {"monthly_trend", "daily_revenue", "mom_growth"}:
        return "line_chart"
    if intent in {
        "revenue_by_country",
        "revenue_by_city",
        "revenue_by_product",
        "revenue_comparison",
        "top_customers",
    }:
        return "bar_chart"
    if intent == "revenue_concentration":
        return "pie_chart"
    return "table"


def insight_from_rows(intent: str, rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "Insufficient data."
    if intent == "total_revenue":
        return f"Total revenue is {rows[0]['total_revenue']:.2f}."
    if intent == "average_deal_size":
        return f"Average deal size is {rows[0]['average_deal_size']:.2f}."
    if intent in {"monthly_trend", "daily_revenue"}:
        vals = [r["revenue"] for r in rows if r.get("revenue") is not None]
        return f"Revenue trend ranges from {min(vals):.2f} to {max(vals):.2f}." if vals else "Insufficient data."
    if intent in {"revenue_by_country", "revenue_by_city", "revenue_by_product", "top_customers"}:
        top = rows[0]
        key = next(k for k in top.keys() if k != "revenue")
        return f"Top performer is {top[key]} with revenue {top['revenue']:.2f}."
    if intent in {"revenue_comparison", "mom_growth"}:
        vals = [r["revenue"] for r in rows]
        if len(vals) < 2:
            return "Insufficient data."
        diff = ((vals[0] - vals[1]) / vals[1]) * 100 if vals[1] else 0
        return f"Leading segment is ahead by {diff:.2f}% compared with next segment."
    if intent == "revenue_concentration":
        vals = [r["revenue"] for r in rows]
        total = sum(vals)
        top_share = (vals[0] / total) * 100 if total else 0
        return f"Top customer contributes {top_share:.2f}% of top-10 revenue."
    if intent == "diagnostic_drop":
        by_month = defaultdict(float)
        for r in rows:
            by_month[r["month"]] += r["revenue"]
        months = sorted(by_month)
        if len(months) < 2:
            return "Insufficient data."
        latest, prev = months[-1], months[-2]
        change = ((by_month[latest] - by_month[prev]) / by_month[prev]) * 100 if by_month[prev] else 0
        return f"Latest month changed by {change:.2f}% vs previous month."
    return "Insufficient data."


def chat(tenant_id: str, role: str, session_id: str, message: str) -> dict[str, Any]:
    if role not in ALLOWED_ROLES:
        raise PermissionError("Role not permitted.")

    SESSIONS[session_id].append(message)
    intent = detect_intent(message)
    spec = generate_query(intent)

    if not spec["query"]:
        return {
            "intent": "clarification_needed",
            "answer": "Can you clarify the KPI or comparison you want?",
            "query": "",
            "visualization": "table",
        }

    validate_query(spec["query"])

    conn = get_conn()
    try:
        track_usage(conn, tenant_id, "chat")
        rows = run_query(conn, spec["query"], tenant_id)
        insight = insight_from_rows(spec["intent"], rows)
        visualization = recommend_visualization(spec["intent"])

        conn.execute(
            "INSERT INTO query_log (tenant_id, role, question, intent, query) VALUES (?, ?, ?, ?, ?)",
            (tenant_id, role, message, spec["intent"], spec["query"]),
        )
        conn.commit()

        return {
            "intent": spec["intent"],
            "query": spec["query"],
            "rows": rows,
            "answer": insight,
            "visualization": visualization,
            "session_turns": len(SESSIONS[session_id]),
        }
    finally:
        conn.close()


def query_spec(message: str) -> dict[str, str]:
    intent = detect_intent(message)
    spec = generate_query(intent)
    if spec["query"]:
        validate_query(spec["query"])
    return spec


def usage_summary(tenant_id: str) -> dict[str, Any]:
    conn = get_conn()
    try:
        rows = run_query(
            conn,
            "SELECT endpoint, COUNT(*) as calls FROM usage_tracking WHERE tenant_id = :tenant_id GROUP BY endpoint",
            tenant_id,
        )
        return {"tenant_id": tenant_id, "usage": rows}
    finally:
        conn.close()


def main() -> None:
    init_db()
    sample = chat("tenant_alpha", "analyst", "cli-session", "What is total revenue?")
    print(json.dumps(sample, indent=2))


if __name__ == "__main__":
    main()
