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

*May the guidance of grace light your path, Tarnished.*
