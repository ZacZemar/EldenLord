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


if __name__ == "__main__":
    unittest.main()
