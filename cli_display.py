# This is for displaying the various builds such as Bleed, Frost, etc.

from query import get_bleed_build, get_madness_build, get_frost_build


def display_bleed_build():
    build = get_bleed_build()

    print("\n=== BLEED BUILD ===\n")
    print(build["summary"])

    print("\n--- Mechanic Notes ---")
    for note in build["mechanic_notes"]:
        print(f"- {note}")

    print("\n--- Bleed Eligible Weapons ---")
    for weapon in build["weapons"]:
        print(f"Weapon     : {weapon['name']}")
        print(f"Scaling    : {weapon['scaling']}")
        print(f"Ash of War : {weapon['ash_of_war']}")
        print(f"Bleed Via  : {', '.join(weapon['status_effect_sources'])}")

        if weapon["incantations"]:
            print(f"Incants    : {', '.join(weapon['incantations'])}")
        else:
            print("Incants    : No incantation buffs compatible")

        print("-" * 40)

    print("\n--- Bleed Incantations ---")
    for incantation in build["incantations"]:
        print(f"Incantation : {incantation['name']}")
        print(f"Description : {incantation['description']}")
        print("-" * 40)

    print("\n--- Supporting Talismans ---")
    for talisman in build["talismans"]:
        print(f"Talisman : {talisman['name']}")
        print(f"Effect   : {talisman['effect']}")
        print("-" * 40)


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
        print(f"Madness Via  : {', '.join(weapon['status_effect_sources'])}")
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


def display_frost_build():
    build = get_frost_build()

    print("\n=== FROST BUILD ===\n")
    print(build["summary"])

    print("\n--- Mechanic Notes ---")
    for note in build["mechanic_notes"]:
        print(f"- {note}")

    print("\n--- Frost Eligible Weapons ---")
    for weapon in build["weapons"]:
        print(f"Weapon     : {weapon['name']}")
        print(f"Scaling    : {weapon['scaling']}")
        print(f"Ash of War : {weapon['ash_of_war']}")
        print(f"Frost Via  : {', '.join(weapon['status_effect_sources'])}")

        print("-" * 40)
