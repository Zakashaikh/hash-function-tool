# database.py - SQLite persistence for hash operations.

import sqlite3
from datetime import datetime

DATABASE_NAME = "hash_results.db"


def init_db():
    """Create the hash_results table if it doesn't exist."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS hash_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            input_type TEXT NOT NULL,
            input_value TEXT NOT NULL,
            algorithm TEXT NOT NULL,
            hash_result TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def save_hash_result(input_type, input_value, algorithm, hash_result):
    """Insert one hash operation. input_type is 'text' or 'file'."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        """
        INSERT INTO hash_results (timestamp, input_type, input_value, algorithm, hash_result)
        VALUES (?, ?, ?, ?, ?)
        """,
        (timestamp, input_type, input_value, algorithm, hash_result),
    )
    conn.commit()
    conn.close()


def get_hash_history(limit=50):
    """Return the most recent operations, newest first, as dicts."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT timestamp, input_type, input_value, algorithm, hash_result
        FROM hash_results
        ORDER BY timestamp DESC
        LIMIT ?
        """,
        (limit,),
    )
    rows = cursor.fetchall()
    conn.close()
    return [
        {
            "timestamp": row[0],
            "input_type": row[1],
            "input_value": row[2],
            "algorithm": row[3],
            "hash_result": row[4],
        }
        for row in rows
    ]


def get_database_stats():
    """Return record counts overall, by algorithm, and by input type."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM hash_results")
    total_records = cursor.fetchone()[0]

    cursor.execute(
        "SELECT algorithm, COUNT(*) FROM hash_results GROUP BY algorithm"
    )
    algorithm_counts = cursor.fetchall()

    cursor.execute(
        "SELECT input_type, COUNT(*) FROM hash_results GROUP BY input_type"
    )
    input_type_counts = cursor.fetchall()

    conn.close()
    return {
        "total_records": total_records,
        "algorithm_counts": dict(algorithm_counts),
        "input_type_counts": dict(input_type_counts),
    }


if __name__ == "__main__":
    init_db()
    save_hash_result("text", "Hello World", "SHA-256", "test_hash_value")
    print(f"history rows: {len(get_hash_history(5))}")
    print(f"stats: {get_database_stats()}")
