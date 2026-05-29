import sqlite3

DB_NAME = "elden_lord.db"

def get_bleed_weapons():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Fetch all bleed eligible weapons - qualifies if it meets ANY one condition
    cursor.execute("""
        SELECT weapon_id, Name, Scaling, Ash_of_War,
               has_innate_bleed, can_blood_infuse, can_receive_bleed_incantation
        FROM WEAPONS
        WHERE has_innate_bleed = 1
           OR can_blood_infuse = 1
           OR can_receive_bleed_incantation = 1
    """)
    weapons = cursor.fetchall()

    results = []

    for weapon in weapons:
        weapon_id, name, scaling, ash_of_war, innate, infuse, incant = weapon

        # Build a short eligibility summary
        reasons = []
        if innate:
            reasons.append("Innate Bleed")
        if infuse:
            reasons.append("Blood Infusion")
        if incant:
            reasons.append("Bleed Incantation")

        # Fetch compatible incantations from junction table
        cursor.execute("""
            SELECT I.Name
            FROM INCANTATIONS I
            JOIN WEAPON_INCANTATIONS WI ON I.incantation_id = WI.incantation_id
            WHERE WI.weapon_id = ?
        """, (weapon_id,))
        incantations = [row[0] for row in cursor.fetchall()]

        results.append({
            "name": name,
            "scaling": scaling,
            "ash_of_war": ash_of_war,
            "bleed_sources": reasons,
            "incantations": incantations if incantations else None
        })

    conn.close()
    return results


def display_bleed_weapons():
    weapons = get_bleed_weapons()

    print("\n=== BLEED ELIGIBLE WEAPONS ===\n")

    for w in weapons:
        print(f"Weapon     : {w['name']}")
        print(f"Scaling    : {w['scaling']}")
        print(f"Ash of War : {w['ash_of_war']}")
        print(f"Bleed Via  : {', '.join(w['bleed_sources'])}")

        if w["incantations"]:
            print(f"Incants    : {', '.join(w['incantations'])}")
        else:
            print(f"Incants    : No incantation buffs compatible")

        print("-" * 40)

def get_madness_weapons(db_name=DB_NAME):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT Name, Scaling, Damage, Passive, Ash_of_War
        FROM WEAPONS
        WHERE has_innate_madness = 1
        ORDER BY weapon_id
    """)
    weapons = cursor.fetchall()

    conn.close()

    return [
        {
            "name": name,
            "scaling": scaling,
            "damage": damage,
            "passive": passive,
            "ash_of_war": ash_of_war,
        }
        for name, scaling, damage, passive, ash_of_war in weapons
    ]


def get_madness_incantations(db_name=DB_NAME):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT Name, Description
        FROM INCANTATIONS
        WHERE damage_type = 'madness'
        ORDER BY incantation_id
    """)
    incantations = cursor.fetchall()

    conn.close()

    return [
        {
            "name": name,
            "description": description,
        }
        for name, description in incantations
    ]


def get_madness_seals(db_name=DB_NAME):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT Name, primary_scaling, incant_category, bonus_pct, notes
        FROM SEALS
        WHERE build_type = 'madness'
        ORDER BY seal_id
    """)
    seals = cursor.fetchall()

    conn.close()

    return [
        {
            "name": name,
            "primary_scaling": primary_scaling,
            "incant_category": incant_category,
            "bonus_pct": bonus_pct,
            "notes": notes,
        }
        for name, primary_scaling, incant_category, bonus_pct, notes in seals
    ]


def get_madness_talismans(db_name=DB_NAME):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT Name, Effect
        FROM TALISMANS
        WHERE Name IN (
            "Aged One's Exultation",
            "Fire Scorpion Charm",
            "Shard of Alexander"
        )
        ORDER BY talisman_id
    """)
    talismans = cursor.fetchall()

    conn.close()

    return [
        {
            "name": name,
            "effect": effect,
        }
        for name, effect in talismans
    ]


def get_madness_build(db_name=DB_NAME):
    return {
        "build_type": "madness",
        "summary": (
            "Madness/Frenzied Flame builds combine Madness weapons, "
            "Frenzied Flame incantations, recommended seals, and supporting talismans."
        ),
        "mechanic_notes": [
            (
                "Madness is heavily limited in PvE because most non-NPC enemies are immune. "
                "It is strongest against players, NPC invaders, and susceptible humanoid targets."
            ),
            (
                "Frenzied Flame Seal directly supports Frenzied Flame incantations through "
                "its passive bonus while equipped."
            ),
            (
                "Dragon Communion Seal does not passively boost Frenzied Flame damage. "
                "Its Madness relevance comes from Arcane scaling, which can improve Madness "
                "buildup from applicable incantations."
            ),
            (
                "This tool does not calculate exact Incantation Scaling, damage, or buildup values. "
                "It surfaces build-relevant options and mechanic context."
            ),
        ],
        "weapons": get_madness_weapons(db_name),
        "incantations": get_madness_incantations(db_name),
        "seals": get_madness_seals(db_name),
        "talismans": get_madness_talismans(db_name),
    }


def display_madness_build():
    build = get_madness_build()

    print("\n=== MADNESS / FRENZIED FLAME BUILD ===\n")
    print(build["summary"])

    print("\n--- Mechanic Notes ---")
    for note in build["mechanic_notes"]:
        print(f"- {note}")

    print("\n--- Madness Weapons ---")
    for weapon in build["weapons"]:
        print(f"Weapon     : {weapon['name']}")
        print(f"Scaling    : {weapon['scaling']}")
        print(f"Damage     : {weapon['damage']}")
        print(f"Passive    : {weapon['passive']}")
        print(f"Ash of War : {weapon['ash_of_war']}")
        print("-" * 40)

    print("\n--- Frenzied Flame Incantations ---")
    for incantation in build["incantations"]:
        print(f"Incantation : {incantation['name']}")
        print(f"Description : {incantation['description']}")
        print("-" * 40)

    print("\n--- Recommended Seals ---")
    for seal in build["seals"]:
        bonus_display = f"{seal['bonus_pct']}%" if seal["bonus_pct"] is not None else "None"

        print(f"Seal       : {seal['name']}")
        print(f"Scaling    : {seal['primary_scaling']}")
        print(f"Category   : {seal['incant_category']}")
        print(f"Bonus      : {bonus_display}")
        print(f"Notes      : {seal['notes']}")
        print("-" * 40)

    print("\n--- Supporting Talismans ---")
    for talisman in build["talismans"]:
        print(f"Talisman : {talisman['name']}")
        print(f"Effect   : {talisman['effect']}")
        print("-" * 40)


if __name__ == "__main__":
    display_bleed_weapons()