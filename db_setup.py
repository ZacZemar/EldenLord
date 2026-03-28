import sqlite3

conn = sqlite3.connect('build.db')
cursor_obj = conn.cursor()
tables_to_drop = ["WEAPON_INCANTATIONS", "WEAPONS", "TALISMANS", "INCANTATIONS"]

# Drop each table safely
for table in tables_to_drop:
    cursor_obj.execute(f"DROP TABLE IF EXISTS {table}")

table_creation_query = """
    CREATE TABLE WEAPONS (
        weapon_id INTEGER PRIMARY KEY,
        Name VARCHAR(255) NOT NULL UNIQUE,
        Scaling CHAR(25),
        Damage CHAR(25),
        Passive CHAR(25),
        Infusable BOOL,
        Ash of War TEXT
    );
    CREATE TABLE TALISMANS (
        talisman_id INTEGER PRIMARY KEY,
        Name VARCHAR(255) NOT NULL UNIQUE,
        Effect TEXT
    );
    CREATE TABLE INCANTATIONS (
        incantation_id INTEGER PRIMARY KEY,
        Name VARCHAR(255) NOT NULL UNIQUE,
        Effects TEXT,
        Requirements Text
    );
    CREATE TABLE WEAPON_INCANTATIONS (
        weapon_id INTEGER,
        incantation_id INTEGER,
        PRIMARY KEY (weapon_id, incantation_id)
        FOREIGN KEY (weapon_id) REFERENCES WEAPONS(weapon_id),
        FOREIGN KEY (incantation_id) REFERENCES INCANTATIONS(incantation_id)
    );
"""

# Execute the table creation query
cursor_obj.executescript(table_creation_query)

cursor_obj.close()