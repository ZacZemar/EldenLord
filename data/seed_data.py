import sqlite3

DB_NAME = "elden_lord.db"

def seed():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # --- WEAPONS ---
    weapons = [
        (1, "Hand of Malenia",     "STR E / DEX B", "Physical", "Bleed",  1, 0, 0, "Waterfowl Dance"),
        (2, "Bloodhound's Fang",   "STR D / DEX C", "Physical", "Bleed",  1, 0, 1, "Bloodhound's Finesse"),
        (3, "Backhand Blade",      "STR D / DEX C", "Physical", None,     0, 1, 1, "Blind Spot"),
        (4, "Noble Slender Sword", "STR E / DEX D", "Physical", None,     0, 1, 1, "No Skill"),
    ]

    cursor.executemany("""
        INSERT OR IGNORE INTO WEAPONS
            (weapon_id, Name, Scaling, Damage, Passive,
             has_innate_bleed, can_blood_infuse, can_receive_bleed_incantation, Ash_of_War)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, weapons)

    # --- INCANTATIONS ---
    incantations = [
        (1, "Bloodflame Blade",  "Coats weapon in bloodflame, adding fire and bleed buildup"),
        (2, "Bloodflame Talons", "Rakes bloodflame claws forward, dealing fire and bleed damage"),
    ]

    cursor.executemany("""
        INSERT OR IGNORE INTO INCANTATIONS (incantation_id, Name, Description)
        VALUES (?, ?, ?)
    """, incantations)

    # --- TALISMANS ---
    talismans = [
        (1, "Lord of Blood's Exultation", "Raises attack power when blood loss occurs nearby"),
        (2, "Rotten Winged Sword Insignia", "Greatly raises attack power with successive attacks"),
    ]

    cursor.executemany("""
        INSERT OR IGNORE INTO TALISMANS (talisman_id, Name, Effect)
        VALUES (?, ?, ?)
    """, talismans)

    # --- WEAPON_INCANTATIONS (junction table) ---
    # Hand of Malenia (1)      -> no incantation pairings (can_receive_bleed_incantation = 0)
    # Bloodhound's Fang (2)    -> Bloodflame Blade (1)
    # Backhand Blade (3)       -> Bloodflame Blade (1)
    # Noble Slender Sword (4)  -> Bloodflame Blade (1), Bloodflame Talons (2)
    weapon_incantations = [
        (2, 1),
        (3, 1),
        (4, 1),
        (4, 2),
    ]

    cursor.executemany("""
        INSERT OR IGNORE INTO WEAPON_INCANTATIONS (weapon_id, incantation_id)
        VALUES (?, ?)
    """, weapon_incantations)

    conn.commit()
    conn.close()
    print("Seed data inserted successfully.")

if __name__ == "__main__":
    seed()