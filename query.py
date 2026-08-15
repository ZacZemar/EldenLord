import sqlite3

DB_NAME = "elden_lord.db"

def get_bleed_weapons(db_name=DB_NAME):
    conn = sqlite3.connect(db_name)
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
            "status_effect_sources": reasons,
            "incantations": incantations if incantations else None
        })

    conn.close()
    return results


def get_bleed_incantations(db_name=DB_NAME):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT Name, Description
        FROM INCANTATIONS
        WHERE damage_type = 'bleed'
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


def get_bleed_talismans(db_name=DB_NAME):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT Name, Effect
        FROM TALISMANS
        WHERE Name IN (
            "Lord of Blood's Exultation",
            "Rotten Winged Sword Insignia"
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


def get_bleed_build(db_name=DB_NAME):
    return {
        "build_type": "bleed",
        "summary": (
            "Bleed builds focus on triggering blood loss through innate bleed weapons, "
            "blood infusion, or compatible bleed-related incantations."
        ),
        "mechanic_notes": [
            (
                "A weapon qualifies for this Bleed build view if it has innate bleed, "
                "can receive blood infusion, or can receive a bleed-related weapon buff."
            ),
            (
                "Bloodflame Blade is a weapon-buff incantation, so weapon compatibility "
                "matters for that specific type of incantation."
            ),
            (
                "This tool does not calculate exact damage, exact status buildup, "
                "or affinity-specific scaling values yet."
            ),
        ],
        "weapons": get_bleed_weapons(db_name),
        "incantations": get_bleed_incantations(db_name),
        "talismans": get_bleed_talismans(db_name),
    }



def build_madness_sources(
has_innate_madness,
):
    status_effect_sources = []

    if has_innate_madness:
        status_effect_sources.append("Innate Madness")

    return status_effect_sources

def get_madness_weapons(db_name=DB_NAME):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

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

    madness = cursor.fetchall()

    conn.close()

    results = []

    for weapon in madness:
        (
            weapon_id,
            name,
            scaling,
            damage,
            passive,
            ash_of_war,
            has_innate_madness,
        ) = weapon

        status_effect_sources = build_madness_sources(
            has_innate_madness,
        )

        results.append({
            "weapon_id": weapon_id,
            "name": name,
            "scaling": scaling,
            "damage": damage,
            "passive": passive,
            "ash_of_war": ash_of_war,
            "status_effect_sources": status_effect_sources,
        })

    return results


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



def build_frost_sources(
has_innate_frost,
can_cold_infuse,
can_receive_frozen_armament,
can_receive_frozen_grease,
):
    status_effect_sources = []

    if has_innate_frost:
        status_effect_sources.append("Innate Frostbite")

    if can_cold_infuse:
        status_effect_sources.append("Cold Affinity")

    if can_receive_frozen_armament:
        status_effect_sources.append("Frozen Armament")

    if can_receive_frozen_grease:
        status_effect_sources.append("Frozen Grease")

    return status_effect_sources


def get_frost_weapons(db_name=DB_NAME):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

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

    frost =  cursor.fetchall()

    conn.close()

    results = []

    for weapon in frost:
        (
            weapon_id,
            name,
            scaling,
            damage,
            passive,
            ash_of_war,
            has_innate_frost,
            can_cold_infuse,
            can_receive_frozen_armament,
            can_receive_frozen_grease,
        ) = weapon

        status_effect_sources = build_frost_sources(
            has_innate_frost,
            can_cold_infuse,
            can_receive_frozen_armament,
            can_receive_frozen_grease,
        )

        results.append({
            "weapon_id": weapon_id,
            "name": name,
            "scaling": scaling,
            "damage": damage,
            "passive": passive,
            "ash_of_war": ash_of_war,
            "status_effect_sources": status_effect_sources,
        })

    return results


def get_frost_build(db_name=DB_NAME):
    return {
        "build_type": "frost",
        "summary": (
            "Frost builds focus on triggering frost bite through innate frost weapons, "
            "cold infusion, or weapon direct frost buffs."
        ),
        "mechanic_notes": [
            (
                "A weapon qualifies for this Frost build view if it has innate frost, "
                "can receive a frost infusion, or can receive a frost-related weapon buff."
            ),
            (
                "Frozen Armament is a weapon-buff sorcery, so weapon compatibility matters "
                "for that specific Frost path. It adds Frostbite buildup to the buffed weapon, "
                "but this tool does not calculate exact buildup values."
            ),
            (
                "Cold affinity can add Magic damage and INT scaling to a weapon, but INT does "
                "not increase Frostbite buildup. Frostbite buildup should not be modeled as "
                "scaling with INT or Arcane."
            ),
        ],
        "weapons": get_frost_weapons(db_name),
        "incantations": [],
        "sorceries": [],
        "talismans": [],
        "seals": []
    }