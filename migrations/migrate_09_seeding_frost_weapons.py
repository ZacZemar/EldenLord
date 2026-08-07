import sqlite3
import os


DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'elden_lord.db')


def migrate():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("Running migration: Seed Frost weapons...")

    # This migration seeds the initial Frost-relevant weapons.
    #
    # Scope:
    #   - Data only.
    #   - No query logic.
    #   - No CLI routing.

    #
    # Modeling notes:
    #   We are only applying weapons that can directly have frost whether its applied and/or its innate.
    #
    #   All rows below have at least one frost identifier because they directly apply
    #   Frost buildup through normal weapon behavior/passive status. These include:
    #
    #   has_innate_frost = 1
    #   can_cold_infuse = 1
    #   can_receive_frozen_grease = 1
    #   can_receive_frozen_armament = 1
    #   
    # Scaling convention:
    #   Matches existing project convention:
    #   - standard affinity at max upgrade level
    #   - somber weapons at +10
    #   - regular smithing weapons at +25


    frost_weapons = [
        (
            9,
            "Frozen Needle",
            "STR D / DEX B",
            "Standard/Pierce",
            "Frost (60)",
            0,
            0,
            0,
            "Impaling Thrust",
            0,
            1,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
        ),
        (
            10,
            "Death's Poker",
            "STR C / Dex B / Int D",
            "Standard/Pierce",
            "Frost (65)",
            0,
            0,
            0,
            "Ghostflame Ignition",
            0,
            1,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
        ),
        (
            11,
            "Zamor Curved Sword",
            "STR C / DEX B",
            "Slash",
            "Frost (65)",
            0,
            0,
            0,
            "Zamor Ice Storm",
            0,
            1,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
        ),
        (
            12,
            "Icerind Hatchet",
            "STR D / DEX B",
            "Standard",
            "Frost (65)",
            0,
            0,
            0,
            "Hoarfrost Stomp",
            0,
            1,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
        ),
        (
            13,
            "Nagakiba",
            "STR D / DEX B",
            "Slash/Pierce",
            "Bleed (45)",
            1,
            1,
            1,
            "Unsheathe",
            0,
            0,
            0,
            0,
            0,
            0,
            1,
            1,
            1,
        ),
        
    ]

    cursor.executemany("""
        INSERT INTO WEAPONS
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
                has_innate_death_blight,
                can_cold_infuse,
                can_receive_frozen_armament,
                can_receive_frozen_grease
            )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(weapon_id) DO UPDATE SET
            has_innate_frost = excluded.has_innate_frost,
            can_cold_infuse = excluded.can_cold_infuse,
            can_receive_frozen_armament = excluded.can_receive_frozen_armament,
            can_receive_frozen_grease = excluded.can_receive_frozen_grease;
    """, frost_weapons)

    print(f"  [OK] Seeded {cursor.rowcount} Frost weapon(s)")

    # Verify
    cursor.execute("""
        SELECT
            weapon_id,
            Name,
            Scaling,
            Damage,
            Passive,
            Ash_of_War,
            has_innate_frost,
            can_cold_infuse,
            can_receive_frozen_armament,
            can_receive_frozen_grease
        FROM WEAPONS
        WHERE has_innate_frost = 1
            OR can_cold_infuse = 1
            OR can_receive_frozen_armament = 1
            OR can_receive_frozen_grease = 1
        ORDER BY weapon_id
    """)
    rows = cursor.fetchall()

    print("\n  Current Frost weapons:")
    for row in rows:
        print(
            f"    id={row[0]} | {row[1]} | scaling={row[2]} | "
            f"damage={row[3]} | passive={row[4]} | AoW={row[5]} | "
            f"has_innate_frost={row[6]} | can_cold_infuse={row[7]} | "
            f"can_receive_frozen_armament={row[8]} | can_receive_frozen_grease={row[9]} "
        )

    conn.commit()
    conn.close()
    print("\nMigration complete.")


if __name__ == "__main__":
    migrate()