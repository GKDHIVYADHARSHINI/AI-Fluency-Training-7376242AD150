"""Day 6 Task: Validate tool arguments before execution."""

from task_tools import SCHEMAS


TYPES = {
    "string": str,
    "number": (int, float),
    "integer": int,
    "boolean": bool,
    "array": list,
    "object": dict,
}


def validate_arguments(arguments, schema):
    """Return None if valid, otherwise return a useful error message."""

    # 1. Arguments must be a JSON object
    if not isinstance(arguments, dict):
        return "Arguments must be a JSON object."

    properties = schema.get("properties", {})

    # 2. Check required arguments
    for name in schema.get("required", []):
        if name not in arguments:
            return (
                f"Missing required argument '{name}'. "
                f"Expected: {', '.join(properties)}."
            )

    # 3. Reject invented arguments
    if schema.get("additionalProperties") is False:
        extra = [key for key in arguments if key not in properties]

        if extra:
            return (
                f"Unexpected argument(s): {', '.join(extra)}. "
                f"Allowed: {', '.join(properties)}."
            )

    # 4. Check types and enum values
    for name, value in arguments.items():
        rule = properties.get(name, {})

        expected = TYPES.get(rule.get("type"))

        if expected and not isinstance(value, expected):
            return (
                f"Argument '{name}' must be a {rule['type']}, "
                f"but got {type(value).__name__}: {value!r}."
            )

        if "enum" in rule and value not in rule["enum"]:
            return (
                f"Argument '{name}' must be one of "
                f"{rule['enum']}, got {value!r}."
            )

    return None


if __name__ == "__main__":

    schema = SCHEMAS["get_subject_hours"]

    test_cases = [
        # Valid
        {"subject": "DSA"},

        # Valid with enum
        {"subject": "Python", "difficulty": "hard"},

        # Missing required argument
        {},

        # Wrong type
        {"subject": 123},

        # Invalid enum
        {"subject": "JavaScript"},

        # Invalid difficulty enum
        {"subject": "AI", "difficulty": "medium"},

        # Invented extra argument
        {"subject": "DBMS", "year": 2026},
    ]

    for case in test_cases:
        result = validate_arguments(case, schema)

        print(
            f"{str(case):<55} -> "
            f"{result if result else 'OK'}"
        )