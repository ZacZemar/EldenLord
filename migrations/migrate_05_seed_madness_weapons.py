import sqlite3
import os


DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'elden_lord.db')


def migrate():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("Running migration: Seed Madness weapons...")

    # This migration seeds the initial Madness-relevant weapons for v2.
    #
    # Scope:
    #   - Data only.
    #   - No query logic.
    #   - No CLI routing.
    #   - No weapon_type column yet.
    #
    # Modeling notes:
    #   Frenzyflame Perfume Bottle is seeded in WEAPONS because it is a weapon-class
    #   DLC item, not a crafted consumable perfume.
    #
    #   All rows below have has_innate_madness = 1 because they directly apply
    #   Madness buildup through normal weapon behavior/passive status.
    #
    # Scaling convention:
    #   Matches existing project convention:
    #   - standard affinity at max upgrade level
    #   - somber weapons at +10
    #   - regular smithing weapons at +25
    #
    # Important:
    #   Madness is much more limited in PvE than statuses like bleed or frost.
    #   Most non-NPC enemies are immune. That caveat belongs in the future
    #   Madness query/display output, not in this seed migration.

    madness_weapons = [
        (
            5,
            "Vyke's War Spear",
            "STR D / DEX B / FAI C",
            "Physical / Fire",
            "Madness (65)",
            0,
            0,
            0,
            "Frenzyflame Thrust",
            1,
            0,
            0,
            0,
            0,
            0,
        ),
        (
            6,
            "Fingerprint Stone Shield",
            "STR B",
            "Physical",
            "Madness (70)",
            0,
            0,
            0,
            "Shield Bash",
            1,
            0,
            0,
            0,
            0,
            0,
        ),
        (
            7,
            "Madding Hand",
            "STR D / DEX D / INT D / FAI D",
            "Physical / Fire",
            "Madness (55); attack boost when Madness occurs nearby",
            0,
            0,
            0,
            "Madding Spear-Hand Strike",
            1,
            0,
            0,
            0,
            0,
            0,
        ),
        (
            8,
            "Frenzyflame Perfume Bottle",
            "STR D / DEX C / INT D / FAI D",
            "Fire",
            "Madness (60)",
            0,
            0,
            0,
            "Kick",
            1,
            0,
            0,
            0,
            0,
            0,
        ),
    ]

    cursor.executemany("""
        INSERT OR IGNORE INTO WEAPONS
            (
                weapon_id,
                Name,
                Scaling,
                Damage,
                Passive,
                has_innate_bleed,
                can_blood_infuse,
                can_receive_bleed_incantation,
                Ash_of_War,
                has_innate_madness,
                has_innate_frost,
                has_innate_poison,
                has_innate_scarlet_rot,
                has_innate_sleep,
                has_innate_death_blight
            )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, madness_weapons)

    print(f"  [OK] Seeded {cursor.rowcount} Madness weapon(s)")

    # Verify
    cursor.execute("""
        SELECT
            weapon_id,
            Name,
            Scaling,
            Damage,
            Passive,
            Ash_of_War,
            has_innate_madness
        FROM WEAPONS
        WHERE has_innate_madness = 1
        ORDER BY weapon_id
    """)
    rows = cursor.fetchall()

    print("\n  Current Madness weapons:")
    for row in rows:
        print(
            f"    id={row[0]} | {row[1]} | scaling={row[2]} | "
            f"damage={row[3]} | passive={row[4]} | AoW={row[5]} | "
            f"has_innate_madness={row[6]}"
        )

    conn.commit()
    conn.close()
    print("\nMigration complete.")


if __name__ == "__main__":
    migrate()