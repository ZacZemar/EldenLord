import sys
import os
from pathlib import Path
import sqlite3
import tempfile
import unittest

# Add the parent directory (..) to the Python path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from query import (
    build_bleed_sources,
    get_bleed_weapons,
    get_bleed_incantations,
    get_bleed_talismans,
    get_bleed_build,
)


class TestBleedBuildQueryLogic(unittest.TestCase):
    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False)
        self.db_path = self.temp_db.name
        self.temp_db.close()

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.executescript("""
            CREATE TABLE WEAPONS (
                weapon_id INTEGER PRIMARY KEY,
                Name VARCHAR(255) NOT NULL UNIQUE,
                Scaling CHAR(25),
                Damage CHAR(25),
                Passive CHAR(25),
                has_innate_bleed BOOL,
                can_blood_infuse BOOL,
                can_receive_bleed_incantation BOOL,
                Ash_of_War TEXT,
                has_innate_madness BOOL DEFAULT 0,
                has_innate_frost BOOL DEFAULT 0,
                has_innate_poison BOOL DEFAULT 0,
                has_innate_scarlet_rot BOOL DEFAULT 0,
                has_innate_sleep BOOL DEFAULT 0,
                has_innate_death_blight BOOL DEFAULT 0
            );

            CREATE TABLE INCANTATIONS (
                incantation_id INTEGER PRIMARY KEY,
                Name VARCHAR(255) NOT NULL UNIQUE,
                Description TEXT,
                damage_type TEXT
            );

            CREATE TABLE TALISMANS (
                talisman_id INTEGER PRIMARY KEY,
                Name VARCHAR(255) NOT NULL UNIQUE,
                Effect TEXT
            );

            CREATE TABLE WEAPON_INCANTATIONS (
                weapon_id INTEGER,
                incantation_id INTEGER,
                PRIMARY KEY (weapon_id, incantation_id),
                FOREIGN KEY (weapon_id) REFERENCES WEAPONS(weapon_id),
                FOREIGN KEY (incantation_id) REFERENCES INCANTATIONS(incantation_id)
            );
        """)

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
                    has_innate_death_blight
                )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, [
            (
                1,
                "Bloodhound's Fang",
                "STR D / DEX C",
                "Physical",
                "Bleed",
                1,
                0,
                1,
                "Bloodhound's Finesse",
                0,
                0,
                0,
                0,
                0,
                0,
            ),
            (
                2,
                "Noble Slender Sword",
                "STR E / DEX C",
                "Physical",
                None,
                0,
                1,
                1,
                "Square Off",
                0,
                0,
                0,
                0,
                0,
                0,
            ),
            (
                3,
                "Vyke's War Spear",
                "STR D / DEX B / FAI C",
                "Physical / Fire",
                "Madness",
                0,
                0,
                0,
                "Frenzyflame Thrust",
                1,
                0,
                0,
                0,
                0,
                0,
            ),
        ])

        cursor.executemany("""
            INSERT INTO INCANTATIONS
                (incantation_id, Name, Description, damage_type)
            VALUES (?, ?, ?, ?)
        """, [
            (
                1,
                "Bloodflame Blade",
                "Coats weapon in bloodflame, adding fire damage and bleed buildup.",
                "bleed",
            ),
            (
                2,
                "Bloodflame Talons",
                "Rakes bloodflame claws forward, dealing fire and bleed damage.",
                "bleed",
            ),
            (
                3,
                "Frenzied Burst",
                "Fires a concentrated beam of frenzied flame.",
                "madness",
            ),
        ])

        cursor.executemany("""
            INSERT INTO TALISMANS
                (talisman_id, Name, Effect)
            VALUES (?, ?, ?)
        """, [
            (
                1,
                "Lord of Blood's Exultation",
                "Raises attack power when blood loss occurs nearby.",
            ),
            (
                2,
                "Rotten Winged Sword Insignia",
                "Greatly raises attack power with successive attacks.",
            ),
            (
                3,
                "Aged One's Exultation",
                "Raises attack power when Madness is triggered nearby.",
            ),
        ])

        cursor.executemany("""
            INSERT INTO WEAPON_INCANTATIONS
                (weapon_id, incantation_id)
            VALUES (?, ?)
        """, [
            (1, 1),
            (2, 1),
        ])

        conn.commit()
        conn.close()

    def tearDown(self):
        os.remove(self.db_path)

    def test_build_bleed_sources_for_innate_bleed(self):
        sources = build_bleed_sources(
            has_innate_bleed=1,
            can_blood_infuse=0,
            can_receive_bleed_incantation=0,
        )

        self.assertEqual(sources, ["Innate Bleed"])

    def test_build_bleed_sources_for_blood_infusion(self):
        sources = build_bleed_sources(
            has_innate_bleed=0,
            can_blood_infuse=1,
            can_receive_bleed_incantation=0,
        )

        self.assertEqual(sources, ["Blood Infusion"])

    def test_build_bleed_sources_for_bleed_incantation(self):
        sources = build_bleed_sources(
            has_innate_bleed=0,
            can_blood_infuse=0,
            can_receive_bleed_incantation=1,
        )

        self.assertEqual(sources, ["Bleed Incantation"])

    def test_build_bleed_sources_returns_all_applicable_sources(self):
        sources = build_bleed_sources(
            has_innate_bleed=1,
            can_blood_infuse=1,
            can_receive_bleed_incantation=1,
        )

        self.assertEqual(sources, [
            "Innate Bleed",
            "Blood Infusion",
            "Bleed Incantation",
        ])

    def test_get_bleed_weapons_returns_only_bleed_eligible_weapons(self):
        weapons = get_bleed_weapons(self.db_path)
        weapon_names = [weapon["name"] for weapon in weapons]

        self.assertEqual(len(weapons), 2)
        self.assertIn("Bloodhound's Fang", weapon_names)
        self.assertIn("Noble Slender Sword", weapon_names)
        self.assertNotIn("Vyke's War Spear", weapon_names)

    def test_get_bleed_weapons_includes_eligibility_reasons(self):
        weapons = get_bleed_weapons(self.db_path)

        bloodhound = next(
            weapon for weapon in weapons
            if weapon["name"] == "Bloodhound's Fang"
        )

        noble = next(
            weapon for weapon in weapons
            if weapon["name"] == "Noble Slender Sword"
        )

        self.assertIn("Innate Bleed", bloodhound["status_effect_sources"])
        self.assertIn("Bleed Incantation", bloodhound["status_effect_sources"])

        self.assertIn("Blood Infusion", noble["status_effect_sources"])
        self.assertIn("Bleed Incantation", noble["status_effect_sources"])

    def test_get_bleed_incantations_returns_only_bleed_damage_type(self):
        incantations = get_bleed_incantations(self.db_path)
        incantation_names = [incantation["name"] for incantation in incantations]

        self.assertEqual(len(incantations), 2)
        self.assertIn("Bloodflame Blade", incantation_names)
        self.assertIn("Bloodflame Talons", incantation_names)
        self.assertNotIn("Frenzied Burst", incantation_names)

    def test_get_bleed_talismans_returns_known_bleed_talismans(self):
        talismans = get_bleed_talismans(self.db_path)
        talisman_names = [talisman["name"] for talisman in talismans]

        self.assertEqual(len(talismans), 2)
        self.assertIn("Lord of Blood's Exultation", talisman_names)
        self.assertIn("Rotten Winged Sword Insignia", talisman_names)
        self.assertNotIn("Aged One's Exultation", talisman_names)

    def test_get_bleed_build_returns_structured_build_data(self):
        build = get_bleed_build(self.db_path)

        self.assertEqual(build["build_type"], "bleed")
        self.assertIsInstance(build["summary"], str)
        self.assertIsInstance(build["mechanic_notes"], list)
        self.assertGreater(len(build["mechanic_notes"]), 0)

        self.assertIsInstance(build["weapons"], list)
        self.assertIsInstance(build["incantations"], list)
        self.assertIsInstance(build["talismans"], list)

        self.assertEqual(len(build["weapons"]), 2)
        self.assertEqual(len(build["incantations"]), 2)
        self.assertEqual(len(build["talismans"]), 2)

    def test_get_bleed_build_shape_is_json_friendly(self):
        build = get_bleed_build(self.db_path)

        expected_keys = {
            "build_type",
            "summary",
            "mechanic_notes",
            "weapons",
            "incantations",
            "talismans",
        }

        self.assertEqual(set(build.keys()), expected_keys)

        for section in ["weapons", "incantations", "talismans"]:
            self.assertIsInstance(build[section], list)
            for item in build[section]:
                self.assertIsInstance(item, dict)


if __name__ == "__main__":
    unittest.main()
