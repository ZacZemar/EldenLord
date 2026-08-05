import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'elden_lord.db')

def migrate():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("Running migration: Add Frost weapon eligibility columns to WEAPONS...")


    columns = [
        "can_cold_infuse",
        "can_receive_frozen_armament",
        "can_receive_frozen_grease",
    ]

    for col_name in columns:
        # Step 1 — Add new weapons column (SQLite allows this via ALTER TABLE)
        try:
            cursor.execute(f"""
                ALTER TABLE WEAPONS ADD COLUMN {col_name} BOOL DEFAULT 0
            """)
            print(f"  [OK] Added {col_name} column to WEAPONS")
        except Exception as e:
            print(f"  [SKIP] Column may already exist: {e}")

    # Step 3 — Verify Schema
    cursor.execute("PRAGMA table_info(WEAPONS)")
    columns_info = cursor.fetchall()
    print("\n Current WEAPONS columns:")
    for col in columns_info:
        print(f"    {col[1]} ({col[2]})")


    conn.commit()
    conn.close()
    print("\nMigration complete.")

if __name__ == "__main__":
    migrate()
