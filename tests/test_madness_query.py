import sys
import os
from pathlib import Path
import sqlite3
import tempfile
import unittest

# Add the parent directory (..) to the Python path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from query import (
    get_madness_weapons,
    get_madness_incantations,
    get_madness_seals,
    get_madness_talismans,
    get_madness_build,
    build_madness_sources
)


class TestMadnessQueryLogic(unittest.TestCase):
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

            CREATE TABLE SEALS (
                seal_id INTEGER PRIMARY KEY,
                Name VARCHAR(255) NOT NULL UNIQUE,
                primary_scaling TEXT,
                incant_category TEXT,
                bonus_pct INTEGER,
                build_type TEXT,
                notes TEXT
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
                "Vyke's War Spear",
                "STR D / DEX B / FAI C",
                "Physical / Fire",
                "Madness (65)",
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
        ])

        cursor.executemany("""
            INSERT INTO INCANTATIONS
                (incantation_id, Name, Description, damage_type)
            VALUES (?, ?, ?, ?)
        """, [
            (
                1,
                "Frenzied Burst",
                "Fires a concentrated beam of frenzied flame.",
                "madness",
            ),
            (
                2,
                "Bloodflame Blade",
                "Coats weapon in bloodflame.",
                "bleed",
            ),
        ])

        cursor.executemany("""
            INSERT INTO SEALS
                (seal_id, Name, primary_scaling, incant_category, bonus_pct, build_type, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, [
            (
                1,
                "Frenzied Flame Seal",
                "STR / DEX / INT / Faith",
                "Frenzied Flame Incantations",
                20,
                "madness",
                "Boosts Frenzied Flame incantations while equipped.",
            ),
            (
                2,
                "Clawmark Seal",
                "STR / Faith",
                "Bestial Incantations",
                10,
                "beast",
                "Boosts Bestial incantations.",
            ),
        ])

        cursor.executemany("""
            INSERT INTO TALISMANS
                (talisman_id, Name, Effect)
            VALUES (?, ?, ?)
        """, [
            (
                1,
                "Aged One's Exultation",
                "Raises attack power when Madness is triggered nearby.",
            ),
            (
                2,
                "Fire Scorpion Charm",
                "Raises fire damage, but increases physical damage taken.",
            ),
            (
                3,
                "Shard of Alexander",
                "Greatly boosts the attack power of skills.",
            ),
            (
                4,
                "Lord of Blood's Exultation",
                "Raises attack power when blood loss occurs nearby.",
            ),
        ])

        conn.commit()
        conn.close()

    def tearDown(self):
        os.remove(self.db_path)

    def test_build_madness_sources_for_innate_madness(self):
        sources = build_madness_sources(
            has_innate_madness=1,
        )

        assert sources == ["Innate Madness"]

    def test_get_madness_weapons_returns_only_innate_madness_weapons(self):
        weapons = get_madness_weapons(self.db_path)

        self.assertEqual(len(weapons), 1)
        self.assertEqual(weapons[0]["name"], "Vyke's War Spear")
        self.assertEqual(weapons[0]["passive"], "Madness (65)")
        self.assertNotEqual(weapons[0]["name"], "Noble Slender Sword")

    def test_get_madness_incantations_returns_only_madness_damage_type(self):
        incantations = get_madness_incantations(self.db_path)

        self.assertEqual(len(incantations), 1)
        self.assertEqual(incantations[0]["name"], "Frenzied Burst")
        self.assertNotEqual(incantations[0]["name"], "Bloodflame Blade")

    def test_get_madness_seals_returns_only_madness_build_type(self):
        seals = get_madness_seals(self.db_path)

        self.assertEqual(len(seals), 1)
        self.assertEqual(seals[0]["name"], "Frenzied Flame Seal")
        self.assertEqual(seals[0]["bonus_pct"], 20)
        self.assertNotEqual(seals[0]["name"], "Clawmark Seal")

    def test_get_madness_talismans_returns_known_madness_talismans(self):
        talismans = get_madness_talismans(self.db_path)
        talisman_names = [talisman["name"] for talisman in talismans]

        self.assertEqual(len(talismans), 3)
        self.assertIn("Aged One's Exultation", talisman_names)
        self.assertIn("Fire Scorpion Charm", talisman_names)
        self.assertIn("Shard of Alexander", talisman_names)
        self.assertNotIn("Lord of Blood's Exultation", talisman_names)

    def test_get_madness_build_returns_structured_build_data(self):
        build = get_madness_build(self.db_path)

        self.assertEqual(build["build_type"], "madness")
        self.assertIsInstance(build["summary"], str)
        self.assertIsInstance(build["mechanic_notes"], list)
        self.assertGreater(len(build["mechanic_notes"]), 0)

        self.assertIsInstance(build["weapons"], list)
        self.assertIsInstance(build["incantations"], list)
        self.assertIsInstance(build["seals"], list)
        self.assertIsInstance(build["talismans"], list)

        self.assertEqual(build["weapons"][0]["name"], "Vyke's War Spear")
        self.assertEqual(build["incantations"][0]["name"], "Frenzied Burst")
        self.assertEqual(build["seals"][0]["name"], "Frenzied Flame Seal")

    def test_get_madness_build_shape_is_json_friendly(self):
        build = get_madness_build(self.db_path)

        expected_keys = {
            "build_type",
            "summary",
            "mechanic_notes",
            "weapons",
            "incantations",
            "seals",
            "talismans",
        }

        self.assertEqual(set(build.keys()), expected_keys)

        for section in ["weapons", "incantations", "seals", "talismans"]:
            self.assertIsInstance(build[section], list)
            for item in build[section]:
                self.assertIsInstance(item, dict)


if __name__ == "__main__":
    unittest.main()