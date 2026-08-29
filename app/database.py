import sqlite3
from pathlib import Path

DATABASE = Path(__file__).resolve().parents[1] / "recovery_agent.db"

def get_connection():
    return sqlite3.connect(DATABASE)

def create_tables():
    connection = get_connection()

    connection.execute("""
         CREATE TABLE IF NOT EXISTS payment_events (
          event_id TEXT PRIMARY KEY,
          payment_id TEXT NOT NULL,
          status TEXT NOT NULL,
          failure_reason TEXT NOT NULL,
          amount REAL NOT NULL,
          customer_name TEXT NOT NULL,
          customer_email TEXT NOT NULL,
          received_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
          ) """)

    connection.commit()
    connection.close()


def save_payment_event(event):
    connection = get_connection()

    cursor = connection.execute("""
        INSERT OR IGNORE INTO payment_events (
            event_id,
            payment_id,
            status,
            failure_reason,
            amount,
            customer_name,
            customer_email
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        event.event_id,
        event.payment_id,
        event.status,
        event.failure_reason,
        event.amount,
        event.customer.name,
        event.customer.email
    ))

    connection.commit()
    connection.close()

    return cursor.rowcount == 1

def payment_event_exists(event_id):
    connection = get_connection()

    result = connection.execute(
        "SELECT 1 FROM payment_events WHERE event_id = ?",
        (event_id,)
    ).fetchone()

    connection.close()

    return result is not None


def get_recent_failed_events(minutes=5):
    connection = get_connection()

    rows = connection.execute("""
        SELECT event_id, payment_id, customer_email
        FROM payment_events
        WHERE status = 'failed'
        AND received_at >= datetime('now', ?)
    """, (f'-{minutes} minutes',)).fetchall()

    connection.close()

    return [
        {
            "event_id": row[0],
            "payment_id": row[1],
            "customer_email": row[2]
        }
        for row in rows
    ]
