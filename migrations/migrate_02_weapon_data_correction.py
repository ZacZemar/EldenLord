import sqlite3
import os


DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'elden_lord.db')


def migrate():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("Running migration: Weapon data corrections...")

    # Fix 1 — Noble Slender Sword: correct Ash of War
    cursor.execute("""
        UPDATE WEAPONS
        SET Ash_of_War = 'Square Off'
        WHERE Name = 'Noble Slender Sword'
    """)
    print(f"  [OK] Noble Slender Sword Ash_of_War updated ({cursor.rowcount} row affected)")

    # Fix 2 — Noble Slender Sword: correct DEX scaling D -> C (standard +25)
    cursor.execute("""
        UPDATE WEAPONS
        SET Scaling = 'STR E / DEX C'
        WHERE Name = 'Noble Slender Sword'
    """)
    print(f"  [OK] Noble Slender Sword Scaling updated ({cursor.rowcount} row affected)")

    # Fix 3 — Backhand Blade: correct STR scaling D -> C (standard +25)
    cursor.execute("""
        UPDATE WEAPONS
        SET Scaling = 'STR C / DEX C'
        WHERE Name = 'Backhand Blade'
    """)
    print(f"  [OK] Backhand Blade Scaling updated ({cursor.rowcount} row affected)")

    # Note: Backhand Blade can_receive_bleed_incantation = 1 is correct.
    # Bloodflame Blade applies on standard/keen/quality infusions.
    # Blood and occult infusions block weapon buffs — this is a universal
    # game mechanic, not a per-weapon data issue. No data change required.

    # Verify all weapon data
    cursor.execute("""
        SELECT Name, Scaling, Ash_of_War
        FROM WEAPONS
        ORDER BY weapon_id
    """)
    rows = cursor.fetchall()
    print("\n  Current WEAPONS state:")
    for row in rows:
        print(f"    {row[0]} | Scaling: {row[1]} | AoW: {row[2]}")

    conn.commit()
    conn.close()
    print("\nMigration complete.")

if __name__ == "__main__":
    migrate()