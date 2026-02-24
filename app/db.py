import random
import sqlite3
from datetime import date, timedelta
from pathlib import Path

DB_PATH = Path("data/sales.db")

COUNTRY_CITIES = {
    "Germany": ["Berlin", "Munich", "Hamburg"],
    "France": ["Paris", "Lyon", "Marseille"],
    "USA": ["New York", "Austin", "San Francisco"],
    "India": ["Bengaluru", "Mumbai", "Delhi"],
}

PRODUCT_PRICING = {
    "CRM Suite": 120,
    "Analytics Pro": 220,
    "Automation Lite": 85,
    "Enterprise AI": 410,
}

TENANTS = ["tenant_alpha", "tenant_beta", "tenant_gamma"]


def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS sales (
            tenant_id TEXT NOT NULL,
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            phone_number TEXT NOT NULL,
            city TEXT NOT NULL,
            country TEXT NOT NULL,
            amount INTEGER NOT NULL,
            product TEXT NOT NULL,
            per_price REAL NOT NULL,
            price REAL NOT NULL,
            date TEXT NOT NULL
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS query_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tenant_id TEXT NOT NULL,
            role TEXT NOT NULL,
            question TEXT NOT NULL,
            intent TEXT NOT NULL,
            query TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS usage_tracking (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tenant_id TEXT NOT NULL,
            endpoint TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    cur.execute("SELECT COUNT(*) AS c FROM sales")
    if cur.fetchone()["c"] == 0:
        seed_sales_data(conn, rows=1000)

    conn.commit()
    conn.close()


def seed_sales_data(conn: sqlite3.Connection, rows: int = 1000) -> None:
    random.seed(42)
    cur = conn.cursor()
    start = date(2024, 1, 1)
    names = [
        "Alex Johnson",
        "Priya Sharma",
        "Liam Martin",
        "Sofia Nguyen",
        "Noah Brown",
        "Emma Garcia",
    ]

    for i in range(1, rows + 1):
        tenant_id = random.choices(TENANTS, weights=[0.5, 0.3, 0.2])[0]
        country = random.choice(list(COUNTRY_CITIES.keys()))
        city = random.choice(COUNTRY_CITIES[country])
        product = random.choices(
            list(PRODUCT_PRICING.keys()), weights=[0.35, 0.25, 0.25, 0.15]
        )[0]
        amount = random.randint(1, 12)
        per_price = PRODUCT_PRICING[product]
        price = amount * per_price
        sale_date = start + timedelta(days=random.randint(0, 270))
        name = random.choice(names)
        phone_number = f"+1-555-{random.randint(1000000, 9999999)}"

        cur.execute(
            """
            INSERT INTO sales (
                tenant_id, id, name, phone_number, city, country,
                amount, product, per_price, price, date
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                tenant_id,
                i,
                name,
                phone_number,
                city,
                country,
                amount,
                product,
                per_price,
                price,
                sale_date.isoformat(),
            ),
        )


def track_usage(conn: sqlite3.Connection, tenant_id: str, endpoint: str) -> None:
    conn.execute(
        "INSERT INTO usage_tracking (tenant_id, endpoint) VALUES (?, ?)",
        (tenant_id, endpoint),
    )
    conn.commit()
