import unittest

from validators.build_validator import (
    BuildResponseValidationError,
    validate_build_response,
)


def make_valid_build():
    return {
        "build_type": "frost",
        "summary": "A Frost build.",
        "mechanic_notes": [],
        "weapons": [
            {
                "name": "Frozen Needle",
                "status_effect_sources": ["Innate Frostbite"],
            }
        ],
        "incantations": [],
        "sorceries": [],
        "talismans": [],
        "seals": [],
    }


class TestBuildResponseValidator(unittest.TestCase):
    def test_valid_build_passes(self):
        self.assertIsNone(validate_build_response(make_valid_build()))

    def test_extra_top_level_keys_are_allowed(self):
        build = make_valid_build()
        build["future_field"] = "allowed"

        self.assertIsNone(validate_build_response(build))

    def test_missing_required_key_fails(self):
        build = make_valid_build()
        del build["seals"]

        with self.assertRaises(BuildResponseValidationError):
            validate_build_response(build)

    def test_wrong_collection_type_fails(self):
        build = make_valid_build()
        build["weapons"] = {}

        with self.assertRaises(BuildResponseValidationError):
            validate_build_response(build)

        build["weapons"] = None

        with self.assertRaises(BuildResponseValidationError):
            validate_build_response(build)

    def test_invalid_weapon_shape_fails(self):
        build = make_valid_build()
        build["weapons"][0]["status_effect_sources"] = ["Innate Frostbite", 60]

        with self.assertRaises(BuildResponseValidationError):
            validate_build_response(build)

    def test_optional_weapon_fields_can_be_absent_or_none(self):
        build = make_valid_build()
        build["weapons"][0].update({
            "scaling": None,
            "damage": None,
            "passive": None,
            "ash_of_war": None,
        })

        self.assertIsNone(validate_build_response(build))

    def test_optional_weapon_fields_accept_expected_types(self):
        build = make_valid_build()
        build["weapons"][0].update({
            "weapon_id": 13,
            "scaling": "STR D / DEX B",
            "damage": "Physical 115",
            "passive": "Blood Loss 45",
            "ash_of_war": "Kick",
            "incantations": ["Bloodflame Blade"],
        })

        self.assertIsNone(validate_build_response(build))

    def test_invalid_optional_weapon_field_types_fail(self):
        build = make_valid_build()
        build["weapons"][0]["weapon_id"] = True
        build["weapons"][0]["damage"] = 115
        build["weapons"][0]["incantations"] = ["Bloodflame Blade", 42]

        with self.assertRaises(BuildResponseValidationError):
            validate_build_response(build)


if __name__ == "__main__":
    unittest.main()
