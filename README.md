# Elden Lord — Bleed Build Optimizer

A command-line tool for optimizing bleed builds in Elden Ring. Query bleed-eligible weapons, view compatible incantations, and identify the best gear for maximizing blood loss buildup in the Lands Between.

---

## Overview

Elden Lord is a Python + SQLite CLI application that helps players identify and evaluate weapons suitable for bleed-focused builds. Rather than manually cross-referencing the wiki, the optimizer surfaces every bleed-viable weapon alongside its scaling, Ash of War, and compatible incantation buffs in a single query.

**v1 scope:** Bleed damage type only. Frost, Poison, and Lightning builds are planned for future releases.

---

## Features

- Query all bleed-eligible weapons from a local SQLite database
- Displays weapon scaling, Ash of War, and bleed eligibility source (innate, infusion, or incantation)
- Shows compatible bleed incantations per weapon via a normalized junction table
- Handles all three bleed eligibility paths:
  - Innate bleed passive
  - Blood infusion compatible
  - Can receive bleed incantations (e.g. Bloodflame Blade)

---

## Project Structure

```
Elden Lord/
├── migrations/
│   └── migrate_01_incantation_damage_type.py
├── data/
│   └── seed_data.py
├── db_setup.py
├── query.py
├── main.py
├── elden_lord.db
└── README.md
```

---

## Getting Started

### Prerequisites

- Python 3.8+
- No external dependencies — uses Python's built-in `sqlite3` module

### Setup

```bash
# Clone the repository
git clone git@github.com:ZacZemar/Elden-Lord.git
cd Elden-Lord

# Initialize the database schema
python db_setup.py

# Seed the database with weapon and incantation data
python seed_data.py

# Run the optimizer
python main.py
```

---

## Usage

```
=== ELDEN LORD BUILD OPTIMIZER ===
Your guide to optimizing builds in the Lands Between.

Select a damage type:
  1. Bleed
  2. Frost     (Coming Soon)
  3. Poison    (Coming Soon)
  4. Lightning (Coming Soon)

Enter choice (1-4):
```

Selecting **1** returns all bleed-eligible weapons:

```
=== BLEED ELIGIBLE WEAPONS ===

Weapon     : Hand of Malenia
Scaling    : STR E / DEX B
Ash of War : Waterfowl Dance
Bleed Via  : Innate Bleed
Incants    : No incantation buffs compatible
----------------------------------------
Weapon     : Bloodhound's Fang
Scaling    : STR D / DEX C
Ash of War : Bloodhound's Finesse
Bleed Via  : Innate Bleed, Bleed Incantation
Incants    : Bloodflame Blade
----------------------------------------
```

---

## Database Schema

```
WEAPONS
  weapon_id PK | Name | Scaling | Damage | Passive
  has_innate_bleed | can_blood_infuse | can_receive_bleed_incantation | Ash_of_War

INCANTATIONS
  incantation_id PK | Name | Description

TALISMANS
  talisman_id PK | Name | Effect

WEAPON_INCANTATIONS  (junction table)
  weapon_id FK | incantation_id FK
  PRIMARY KEY (weapon_id, incantation_id)
```

A weapon qualifies as bleed-eligible if it meets **any one** of the following:
- `has_innate_bleed = 1`
- `can_blood_infuse = 1`
- `can_receive_bleed_incantation = 1`

---

## Known Limitations (v1)

- **Ash of War bleed interactions not captured** — weapons that gain bleed through specific Ash of War applications (e.g. Seppuku + Occult infusion) are not modeled in v1
- **Seed data covers 4 edge-case weapons** — full weapon roster expansion planned for v2
- **No stat optimization** — scaling grades are stored as strings; numerical AR calculations are out of scope for v1

---

## Roadmap

| Version | Scope |
|---------|-------|
| v1 | Bleed weapons CLI — ships with 4 edge-case seed weapons |
| v2 | Full weapon roster, full stack web interface (Django + React) |
| v3+ | Frost, Poison, Lightning build support |

---

## Built With

- Python 3
- SQLite3 (via Python standard library)

---

*May the golden order shine through you, Tarnished.*

# Update for the README: Audit

## Build Response Contract

Every build query should return a dictionary with:

- build_type
- summary
- mechanic_notes
- weapons
- incantations
- sorceries
- talismans
- seals

### Build Response Contract

Bleed and Madness now return structured build data, but the expected build response shape is not yet formally documented. Before adding several more build types or moving to Django, the project should define a standard response contract so each build type returns predictable JSON-friendly data.

### Standard Shape

```python
{
    "build_type": "bleed",
    "summary": "...",
    "mechanic_notes": [...],
    "weapons": [...],
    "incantations": [...],
    "sorceries": [...],
    "talismans": [...],
    "seals": [...]
}

### CLI / Query Separation

The project currently keeps database query functions and CLI display functions close together. This is acceptable for the CLI proof of concept, but before converting to Django, query/build logic should be separated from terminal display logic so the same build responses can power both the CLI and future API endpoints.


### Frost V1 Scope

Frost V1 mirrors the Bleed eligibility model conceptually: a weapon can qualify for a build through more than one supported path.

For Frost, a weapon is eligible if it can access Frostbite through one or more modeled weapon-level paths:

- `has_innate_frost`
- `can_cold_infuse`
- `can_receive_frozen_grease`
- `can_receive_frozen_armament`

`has_innate_frost` already exists from the third migration. Issue #27 adds the remaining Frost eligibility columns:

- `can_cold_infuse`
- `can_receive_frozen_grease`
- `can_receive_frozen_armament`

These columns describe whether a weapon can access Frostbite through a specific weapon path. They do not model Frostbite buildup scaling.

Important mechanic note:

- INT can improve Cold-affinity weapon damage when Cold affinity adds INT scaling.
- INT does **not** increase Frostbite buildup rate.
- Frostbite buildup should not be modeled as scaling with INT or Arcane.

### Deferred Frost Sources

Frost V1 does not model Frost skills, Ashes of War, sorceries, or consumables as separate build sources yet.

Deferred examples include:

- Hoarfrost Stomp
- Chilling Mist
- Zamor Ice Storm
- Icecrag-style sorceries
- Freezing Mist-style sorceries
- Freezing Pot or other consumable projectile sources

These are valid Frost tools, but they are not the same as the weapon eligibility paths above. Some are skill-based, some are spell-based, and some depend on separate compatibility rules.

For now:

- `Ash_of_War` is treated as a display field.
- Frost eligibility comes from explicit eligibility flags.
- Skill-source Frost is deferred.


### Local Development Environment

This project uses a local virtual environment for development.

Create the environment:

```bash
./scripts/setup_dev_env.sh

Then you can manually make a venv:

./scripts/setup_dev_env.sh
source .venv/bin/activate 

If you want to automate it:

./scripts/setup_dev_env.sh
cp .envrc.example .envrc
direnv allow

if you do not have direnv you can install with sudo apt install direnv