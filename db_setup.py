import sqlite3

# Scaling values reflect standard affinity at max upgrade level.
# Somber weapons reflect their fixed scaling at +10.
# Affinity-specific scaling is out of scope for v1/v2.

conn = sqlite3.connect('elden_lord.db')
cursor_obj = conn.cursor()

# Drop tables in correct order to respect foreign key dependencies
tables_to_drop = ["WEAPON_INCANTATIONS", "WEAPONS", "TALISMANS", "INCANTATIONS"]

for table in tables_to_drop:
    cursor_obj.execute(f"DROP TABLE IF EXISTS {table}")

table_creation_query = """
    CREATE TABLE WEAPONS (
        weapon_id INTEGER PRIMARY KEY,
        Name VARCHAR(255) NOT NULL UNIQUE,
        Scaling CHAR(25),
        Damage CHAR(25),
        Passive CHAR(25),
        has_innate_bleed BOOL,
        can_blood_infuse BOOL,
        can_receive_bleed_incantation BOOL,
        Ash_of_War TEXT
    );

    CREATE TABLE TALISMANS (
        talisman_id INTEGER PRIMARY KEY,
        Name VARCHAR(255) NOT NULL UNIQUE,
        Effect TEXT
    );

    CREATE TABLE INCANTATIONS (
        incantation_id INTEGER PRIMARY KEY,
        Name VARCHAR(255) NOT NULL UNIQUE,
        Description TEXT
    );

    CREATE TABLE WEAPON_INCANTATIONS (
        weapon_id INTEGER,
        incantation_id INTEGER,
        PRIMARY KEY (weapon_id, incantation_id),
        FOREIGN KEY (weapon_id) REFERENCES WEAPONS(weapon_id),
        FOREIGN KEY (incantation_id) REFERENCES INCANTATIONS(incantation_id)
    );
"""

cursor_obj.executescript(table_creation_query)

cursor_obj.close()
conn.commit()
conn.close()

print("Database setup complete.")