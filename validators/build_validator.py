"""Validate the structure of BuildResponse dictionaries.

This module validates the shape of a response, not Elden Ring domain
correctness or database relationships.
"""


REQUIRED_BUILD_KEYS = frozenset({
    "build_type",
    "summary",
    "mechanic_notes",
    "weapons",
    "incantations",
    "sorceries",
    "talismans",
    "seals",
})

BUILD_COLLECTION_KEYS = frozenset({
    "mechanic_notes",
    "weapons",
    "incantations",
    "sorceries",
    "talismans",
    "seals",
})

OPTIONAL_WEAPON_STRING_KEYS = frozenset({
    "scaling",
    "damage",
    "passive",
    "ash_of_war",
})


class BuildResponseValidationError(ValueError):
    """Raised when a BuildResponse violates the shared contract."""


def validate_build_response(build):
    """Validate a BuildResponse and raise if its structure is invalid.

    Extra top-level keys are allowed so the contract can evolve additively.
    The function returns None for a valid response and raises
    BuildResponseValidationError for an invalid response.
    """
    errors = []

    if not isinstance(build, dict):
        raise BuildResponseValidationError(
            "BuildResponse must be a dictionary."
        )

    missing_keys = REQUIRED_BUILD_KEYS - build.keys()
    if missing_keys:
        errors.append(f"missing required keys: {sorted(missing_keys)}")

    if "build_type" in build and not isinstance(build["build_type"], str):
        errors.append("build_type must be a string")

    if "summary" in build and not isinstance(build["summary"], str):
        errors.append("summary must be a string")

    for key in BUILD_COLLECTION_KEYS:
        if key in build and not isinstance(build[key], list):
            errors.append(f"{key} must be a list")

    weapons = build.get("weapons")
    if isinstance(weapons, list):
        for index, weapon in enumerate(weapons):
            if not isinstance(weapon, dict):
                errors.append(f"weapons[{index}] must be a dictionary")
                continue

            if "name" not in weapon:
                errors.append(f"weapons[{index}] is missing required key: name")
            elif not isinstance(weapon["name"], str):
                errors.append(f"weapons[{index}].name must be a string")

            if "status_effect_sources" not in weapon:
                errors.append(
                    f"weapons[{index}] is missing required key: status_effect_sources"
                )
            elif not isinstance(weapon["status_effect_sources"], list):
                errors.append(
                    f"weapons[{index}].status_effect_sources must be a list"
                )
            elif not all(
                isinstance(source, str)
                for source in weapon["status_effect_sources"]
            ):
                errors.append(
                    f"weapons[{index}].status_effect_sources must contain only strings"
                )

            if "weapon_id" in weapon and (
                isinstance(weapon["weapon_id"], bool)
                or not isinstance(weapon["weapon_id"], int)
            ):
                errors.append(f"weapons[{index}].weapon_id must be an integer")

            for key in OPTIONAL_WEAPON_STRING_KEYS:
                if key in weapon and weapon[key] is not None and not isinstance(
                    weapon[key], str
                ):
                    errors.append(
                        f"weapons[{index}].{key} must be a string or None"
                    )

            if "incantations" in weapon:
                incantations = weapon["incantations"]
                if not isinstance(incantations, list):
                    errors.append(f"weapons[{index}].incantations must be a list")
                elif not all(isinstance(name, str) for name in incantations):
                    errors.append(
                        f"weapons[{index}].incantations must contain only strings"
                    )

    if errors:
        raise BuildResponseValidationError("; ".join(errors))

