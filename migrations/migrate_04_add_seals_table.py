import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'elden_lord.db')


def migrate():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("Running migration: Add SEALS table and seed initial Madness-relevant seals...")

    # SEALS table captures build-relevant seal recommendations.
    #
    # Context:
    #   Direct-damage/status incantations do not depend on the weapon in hand.
    #   They are cast through a Sacred Seal, and their damage is tied to that
    #   seal's Incantation Scaling.
    #
    #   This is different from weapon-buff incantations like Bloodflame Blade,
    #   which need weapon compatibility and belong in WEAPON_INCANTATIONS.
    #
    # Columns:
    #   primary_scaling:
    #       Stats that primarily drive the seal's Incantation Scaling.
    #
    #   incant_category:
    #       Incantation group affected by the seal's passive bonus.
    #       NULL if the seal has no category-specific passive bonus.
    #
    #   bonus_pct:
    #       Passive damage bonus percentage applied to incant_category.
    #       NULL if the seal has no category-specific passive bonus.
    #
    #   build_type:
    #       Build type this seal is relevant to in the CLI.
    #       This is recommendation-oriented, not a claim that the seal only
    #       works for that build.
    #
    #   notes:
    #       Plain-English player guidance explaining why the seal matters.
    #
    # Important Madness mechanic note:
    #   Frenzied Flame Seal directly supports Frenzied Flame incantations through
    #   its passive bonus.
    #
    #   Dragon Communion Seal does NOT passively boost Frenzied Flame damage.
    #   It is relevant to Madness builds because its Arcane scaling can improve
    #   Madness buildup from applicable incantations.
    #
    #   The tool is not calculating exact Incantation Scaling or buildup values
    #   in v2. This table is for reference/recommendation data only.

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS SEALS (
            seal_id INTEGER PRIMARY KEY,
            Name VARCHAR(255) NOT NULL UNIQUE,
            primary_scaling TEXT,
            incant_category TEXT,
            bonus_pct INTEGER,
            build_type TEXT,
            notes TEXT
        )
    """)
    print("  [OK] Created SEALS table if it did not already exist")

    # Seed initial v2 Madness-relevant seals.
    # Additional seals can be added as new build types are implemented.
    seals = [
        (
            1,
            "Frenzied Flame Seal",
            "STR / DEX / INT / Faith",
            "Frenzied Flame Incantations",
            20,
            "madness",
            "Directly supports Madness/Frenzied Flame builds by boosting "
            "Frenzied Flame incantation damage while equipped."
        ),
        (
            2,
            "Dragon Communion Seal",
            "Faith / Arcane",
            "Dragon Communion Incantations",
            15,
            "madness",
            "Relevant for Madness builds because Arcane scaling can improve "
            "Madness buildup from applicable incantations. Its passive bonus "
            "boosts Dragon Communion incantations, not Frenzied Flame incantations."
        ),
    ]

    cursor.executemany("""
        INSERT OR IGNORE INTO SEALS
            (seal_id, Name, primary_scaling, incant_category, bonus_pct, build_type, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, seals)
    print(f"  [OK] Seeded {cursor.rowcount} seal(s)")

    # Verify schema
    cursor.execute("PRAGMA table_info(SEALS)")
    columns_info = cursor.fetchall()

    print("\n  Current SEALS columns:")
    for col in columns_info:
        print(f"    {col[1]} ({col[2]})")

    # Verify seed data
    cursor.execute("""
        SELECT seal_id, Name, primary_scaling, incant_category, bonus_pct, build_type
        FROM SEALS
        ORDER BY seal_id
    """)
    rows = cursor.fetchall()

    print("\n  Current SEALS state:")
    for row in rows:
        bonus_display = f"{row[4]}%" if row[4] is not None else "None"
        print(
            f"    id={row[0]} | {row[1]} | scaling={row[2]} | "
            f"category={row[3]} | bonus={bonus_display} | type={row[5]}"
        )

    conn.commit()
    conn.close()
    print("\nMigration complete.")


if __name__ == "__main__":
    migrate()