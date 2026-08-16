import json


# tests/test_frost_query.py

import sqlite3
import sys

from pathlib import Path

# Add the parent directory (..) to the Python path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from query import build_frost_sources, get_frost_weapons, get_frost_build


def create_test_db(tmp_path):
    db_path = tmp_path / "test_elden_lord.db"

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE WEAPONS (
            weapon_id INTEGER PRIMARY KEY,
            Name TEXT NOT NULL,
            Scaling TEXT,
            Damage TEXT,
            Passive TEXT,
            Ash_of_War TEXT,
            has_innate_frost INTEGER DEFAULT 0,
            can_cold_infuse INTEGER DEFAULT 0,
            can_receive_frozen_armament INTEGER DEFAULT 0,
            can_receive_frozen_grease INTEGER DEFAULT 0
        )
    """)

    conn.commit()
    conn.close()

    return db_path


def insert_weapon(
    db_path,
    weapon_id,
    name,
    scaling="STR D / DEX B",
    damage="Physical",
    passive=None,
    ash_of_war="Unsheathe",
    has_innate_frost=0,
    can_cold_infuse=0,
    can_receive_frozen_armament=0,
    can_receive_frozen_grease=0,
):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO WEAPONS (
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
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
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
    ))

    conn.commit()
    conn.close()


def test_build_frost_sources_for_innate_frost():
    sources = build_frost_sources(
        has_innate_frost=1,
        can_cold_infuse=0,
        can_receive_frozen_armament=0,
        can_receive_frozen_grease=0,
    )

    assert sources == ["Innate Frostbite"]


def test_build_frost_sources_for_non_innate_frost_paths():
    sources = build_frost_sources(
        has_innate_frost=0,
        can_cold_infuse=1,
        can_receive_frozen_armament=1,
        can_receive_frozen_grease=1,
    )

    assert sources == [
        "Cold Affinity",
        "Frozen Armament",
        "Frozen Grease",
    ]


def test_build_frost_sources_returns_all_applicable_sources():
    sources = build_frost_sources(
        has_innate_frost=1,
        can_cold_infuse=1,
        can_receive_frozen_armament=1,
        can_receive_frozen_grease=1,
    )

    assert sources == [
        "Innate Frostbite",
        "Cold Affinity",
        "Frozen Armament",
        "Frozen Grease",
    ]


def test_get_frost_weapons_includes_only_frost_eligible_weapons(tmp_path):
    db_path = create_test_db(tmp_path)

    insert_weapon(
        db_path,
        weapon_id=1,
        name="Frozen Needle",
        passive="Frost (60)",
        ash_of_war="Impaling Thrust",
        has_innate_frost=1,
    )

    insert_weapon(
        db_path,
        weapon_id=2,
        name="Nagakiba",
        passive="Bleed (45)",
        ash_of_war="Unsheathe",
        can_cold_infuse=1,
        can_receive_frozen_armament=1,
        can_receive_frozen_grease=1,
    )

    insert_weapon(
        db_path,
        weapon_id=3,
        name="Plain Longsword",
        passive=None,
        ash_of_war="Square Off",
    )

    weapons = get_frost_weapons(db_path)

    weapon_names = [weapon["name"] for weapon in weapons]

    assert weapon_names == [
        "Frozen Needle",
        "Nagakiba",
    ]


def test_get_frost_weapons_returns_frost_sources_for_each_weapon(tmp_path):
    db_path = create_test_db(tmp_path)

    insert_weapon(
        db_path,
        weapon_id=1,
        name="Frozen Needle",
        passive="Frost (60)",
        has_innate_frost=1,
    )

    insert_weapon(
        db_path,
        weapon_id=2,
        name="Nagakiba",
        passive="Bleed (45)",
        can_cold_infuse=1,
        can_receive_frozen_armament=1,
        can_receive_frozen_grease=1,
    )

    weapons = get_frost_weapons(db_path)

    frozen_needle = weapons[0]
    nagakiba = weapons[1]

    assert frozen_needle["status_effect_sources"] == ["Innate Frostbite"]

    assert nagakiba["status_effect_sources"] == [
        "Cold Affinity",
        "Frozen Armament",
        "Frozen Grease",
    ]


def test_get_frost_weapons_returns_expected_weapon_shape(tmp_path):
    db_path = create_test_db(tmp_path)

    insert_weapon(
        db_path,
        weapon_id=1,
        name="Frozen Needle",
        scaling="STR D / DEX B",
        damage="Standard/Pierce",
        passive="Frost (60)",
        ash_of_war="Impaling Thrust",
        has_innate_frost=1,
    )

    weapons = get_frost_weapons(db_path)

    assert weapons == [
        {
            "weapon_id": 1,
            "name": "Frozen Needle",
            "scaling": "STR D / DEX B",
            "damage": "Standard/Pierce",
            "passive": "Frost (60)",
            "ash_of_war": "Impaling Thrust",
            "status_effect_sources": ["Innate Frostbite"],
        }
    ]


def test_get_frost_build_returns_structured_build_contract(tmp_path):
    db_path = create_test_db(tmp_path)

    insert_weapon(
        db_path,
        weapon_id=1,
        name="Frozen Needle",
        passive="Frost (60)",
        has_innate_frost=1,
    )

    build = get_frost_build(db_path)

    required_keys = {
        "build_type",
        "summary",
        "mechanic_notes",
        "weapons",
        "incantations",
        "sorceries",
        "talismans",
        "seals",
    }

    assert required_keys.issubset(build.keys())

    assert build["build_type"] == "frost"
    assert isinstance(build["summary"], str)
    assert isinstance(build["mechanic_notes"], list)
    assert len(build["mechanic_notes"]) > 0

    assert build["weapons"][0]["name"] == "Frozen Needle"
    assert build["weapons"][0]["status_effect_sources"] == ["Innate Frostbite"]

    assert build["incantations"] == []
    assert build["sorceries"] == []
    assert build["talismans"] == []
    assert build["seals"] == []


def test_get_frost_build_is_json_round_trip_safe(tmp_path):
    db_path = create_test_db(tmp_path)

    insert_weapon(
        db_path,
        weapon_id=1,
        name="Nagakiba",
        passive="Bleed (45)",
        can_cold_infuse=1,
        can_receive_frozen_grease=1,
        can_receive_frozen_armament=1,
    )

    build = get_frost_build(db_path)

    serialized_build = json.dumps(build)
    deserialized_build = json.loads(serialized_build)

    assert deserialized_build == build


def test_frost_weapon_status_sources_have_contract_shape(tmp_path):
    db_path = create_test_db(tmp_path)

    insert_weapon(
        db_path,
        weapon_id=1,
        name="Nagakiba",
        passive="Bleed (45)",
        can_cold_infuse=1,
        can_receive_frozen_grease=1,
        can_receive_frozen_armament=1,
    )

    weapon = get_frost_build(db_path)["weapons"][0]

    assert isinstance(weapon["name"], str)
    assert isinstance(weapon["status_effect_sources"], list)
    assert all(isinstance(source, str) for source in weapon["status_effect_sources"])
