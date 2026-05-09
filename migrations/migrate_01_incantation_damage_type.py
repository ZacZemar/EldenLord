import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'elden_lord.db')

def migrate():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("Running migration: Add damage_type column to INCANTATIONS...")

    # Step 1 — Add damage_type column (SQLite allows this via ALTER TABLE)
    try:
        cursor.execute("""
            ALTER TABLE INCANTATIONS ADD COLUMN damage_type TEXT
        """)
        print("  [OK] Added damage_type column to INCANTATIONS")
    except Exception as e:
        print(f"  [SKIP] Column may already exist: {e}")

    # Step 2 — Backfill existing bleed incantations
    cursor.execute("""
        UPDATE INCANTATIONS
        SET damage_type = 'bleed'
        WHERE Name IN ('Bloodflame Blade', 'Bloodflame Talons')
    """)
    updated = cursor.rowcount
    print(f"  [OK] Updated {updated} existing incantation(s) to damage_type = 'bleed'")

    # Step 3 — Verify
    cursor.execute("SELECT incantation_id, Name, damage_type FROM INCANTATIONS")
    rows = cursor.fetchall()
    print("\n  Current INCANTATIONS state:")
    for row in rows:
        print(f"    id={row[0]} | {row[1]} | damage_type={row[2]}")

    conn.commit()
    conn.close()
    print("\nMigration complete.")

if __name__ == "__main__":
    migrate()
