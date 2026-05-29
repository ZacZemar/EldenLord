import sqlite3
import os


DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'elden_lord.db')


def migrate():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("Running migration: Seed Madness incantations...")

    # This migration seeds the initial Frenzied Flame / Madness incantations for v2.
    #
    # Scope:
    #   - Data only.
    #   - No query logic.
    #   - No CLI routing.
    #   - No weapon/incantation junction rows.
    #
    # Modeling notes:
    #   These are direct-cast incantations. Their damage/status output depends on
    #   the seal used to cast them, not the weapon in the player's hand.
    #
    #   This is different from weapon-buff incantations like Bloodflame Blade,
    #   which require weapon compatibility and belong in WEAPON_INCANTATIONS.
    #
    #   Because these incantations do not buff weapons, they should only be
    #   categorized with damage_type = 'madness' in INCANTATIONS.
    #
    # Important Madness mechanic note:
    #   Madness is heavily limited in PvE because most non-NPC enemies are immune.
    #   That caveat belongs in the future Madness query/display output.

    madness_incantations = [
        (
            3,
            "The Flame of Frenzy",
            "Conjures multiple offensive flames of frenzy that travel forward, dealing fire damage and causing Madness buildup.",
            "madness",
        ),
        (
            4,
            "Frenzied Burst",
            "Fires a concentrated beam of frenzied flame from the caster's eyes, dealing fire damage and causing Madness buildup.",
            "madness",
        ),
        (
            5,
            "Howl of Shabriri",
            "Lets out a maddening howl that causes Madness buildup nearby and increases damage dealt and taken.",
            "madness",
        ),
        (
            6,
            "Unendurable Frenzy",
            "Violently spews frenzied flame from the caster's eyes, dealing fire damage and causing Madness buildup.",
            "madness",
        ),
        (
            7,
            "Inescapable Frenzy",
            "Grabs a human-sized target and causes Madness buildup through a close-range Frenzied Flame attack.",
            "madness",
        ),
        (
            8,
            "Midra's Flame of Frenzy",
            "Summons an apparition of the Lord of Frenzied Flame's head to spew frenzied flame.",
            "madness",
        ),
    ]

    cursor.executemany("""
        INSERT OR IGNORE INTO INCANTATIONS
            (incantation_id, Name, Description, damage_type)
        VALUES (?, ?, ?, ?)
    """, madness_incantations)

    print(f"  [OK] Seeded {cursor.rowcount} Madness incantation(s)")

    # Verify Madness incantations
    cursor.execute("""
        SELECT incantation_id, Name, damage_type
        FROM INCANTATIONS
        WHERE damage_type = 'madness'
        ORDER BY incantation_id
    """)
    rows = cursor.fetchall()

    print("\n  Current Madness incantations:")
    for row in rows:
        print(f"    id={row[0]} | {row[1]} | damage_type={row[2]}")

    # Verify no weapon/incantation junction rows were created for Madness incantations.
    cursor.execute("""
        SELECT COUNT(*)
        FROM WEAPON_INCANTATIONS WI
        JOIN INCANTATIONS I ON WI.incantation_id = I.incantation_id
        WHERE I.damage_type = 'madness'
    """)
    junction_count = cursor.fetchone()[0]

    print(
        "\n  Madness weapon/incantation junction rows: "
        f"{junction_count} "
        "(expected 0 for direct-cast incantations)"
    )

    conn.commit()
    conn.close()
    print("\nMigration complete.")


if __name__ == "__main__":
    migrate()