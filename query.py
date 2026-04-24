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


if __name__ == "__main__":
    display_bleed_weapons()