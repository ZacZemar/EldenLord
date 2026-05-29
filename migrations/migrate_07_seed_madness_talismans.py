import sqlite3
import os


DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'elden_lord.db')


def migrate():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("Running migration: Seed Madness talismans...")

    # This migration seeds the initial Madness/Frenzied Flame-relevant talismans for v2.
    #
    # Scope:
    #   - Data only.
    #   - No query logic.
    #   - No CLI routing.
    #   - No talisman/build junction table yet.
    #
    # Modeling notes:
    #   TALISMANS currently stores general talisman data:
    #       - talisman_id
    #       - Name
    #       - Effect
    #
    #   Because the table does not yet have build_type or notes columns, this seed
    #   migration stores the player-facing reason directly in Effect.
    #
    #   A future schema improvement may split Effect into:
    #       - effect
    #       - build_type
    #       - notes
    #
    #   For v2, the goal is to seed only talismans with clear Madness/Frenzied
    #   Flame relevance rather than every talisman that could technically help.
    #
    # Madness relevance:
    #   Aged One's Exultation:
    #       Direct Madness synergy. Raises attack power when Madness is triggered nearby.
    #
    #   Fire Scorpion Charm:
    #       Indirect Frenzied Flame synergy. Boosts fire damage, which supports many
    #       Frenzied Flame attacks, but increases physical damage taken.
    #
    #   Shard of Alexander:
    #       Weapon skill synergy. Supports Madness setups using weapon skills such as
    #       Frenzyflame Thrust.

    madness_talismans = [
        (
            3,
            "Aged One's Exultation",
            "Raises attack power when Madness is triggered nearby. Direct Madness synergy."
        ),
        (
            4,
            "Fire Scorpion Charm",
            "Raises fire damage, but increases physical damage taken. Supports Frenzied Flame fire damage."
        ),
        (
            5,
            "Shard of Alexander",
            "Greatly boosts the attack power of skills. Supports Madness builds that rely on weapon skills."
        ),
    ]

    cursor.executemany("""
        INSERT OR IGNORE INTO TALISMANS
            (talisman_id, Name, Effect)
        VALUES (?, ?, ?)
    """, madness_talismans)

    print(f"  [OK] Seeded {cursor.rowcount} Madness talisman(s)")

    # Verify seeded Madness-relevant talismans
    cursor.execute("""
        SELECT talisman_id, Name, Effect
        FROM TALISMANS
        WHERE Name IN (
            "Aged One's Exultation",
            "Fire Scorpion Charm",
            "Shard of Alexander"
        )
        ORDER BY talisman_id
    """)
    rows = cursor.fetchall()

    print("\n  Current Madness-relevant talismans:")
    for row in rows:
        print(f"    id={row[0]} | {row[1]} | effect={row[2]}")

    conn.commit()
    conn.close()
    print("\nMigration complete.")


if __name__ == "__main__":
    migrate()