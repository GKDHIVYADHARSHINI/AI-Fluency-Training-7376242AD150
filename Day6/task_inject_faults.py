"""Day 6 Task: Fault injection for the Student Study Assistant.

This script tests the tool handler without calling the model.
"""

import json

from task_robust_agent import handle_tool_call


class FakeFunction:
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments


class FakeCall:
    """Looks like a model-generated tool call."""

    def __init__(self, name, arguments, call_id="test_call"):
        self.id = call_id
        self.type = "function"
        self.function = FakeFunction(name, arguments)


# ============================================================
# At least 8 deliberately broken calls
# ============================================================

FAULTS = [

    # Good call - control case
    (
        "good call",
        FakeCall(
            "get_subject_hours",
            '{"subject": "DSA"}'
        )
    ),

    # 1. Invalid JSON
    (
        "invalid JSON",
        FakeCall(
            "get_subject_hours",
            '{"subject": "DSA"'
        )
    ),

    # 2. Unknown tool
    (
        "unknown tool",
        FakeCall(
            "send_email",
            '{"to": "student@example.com"}'
        )
    ),

    # 3. Missing required argument
    (
        "missing argument",
        FakeCall(
            "get_subject_hours",
            '{}'
        )
    ),

    # 4. Wrong data type
    (
        "wrong type",
        FakeCall(
            "get_subject_hours",
            '{"subject": 123}'
        )
    ),

    # 5. Value outside enum
    (
        "value outside enum",
        FakeCall(
            "get_subject_hours",
            '{"subject": "JavaScript"}'
        )
    ),

    # 6. Invented / extra argument
    (
        "invented argument",
        FakeCall(
            "get_subject_hours",
            '{"subject": "DSA", "year": 2026}'
        )
    ),

    # 7. Own fault: JSON array instead of object
    (
        "JSON array instead of object",
        FakeCall(
            "get_subject_hours",
            '["DSA"]'
        )
    ),

    # 8. Own fault: invalid difficulty enum
    (
        "invalid difficulty",
        FakeCall(
            "get_subject_hours",
            '{"subject": "AI", "difficulty": "medium"}'
        )
    ),
]


if __name__ == "__main__":

    print("=" * 90)
    print("DAY 6 TASK - FAULT INJECTION")
    print("=" * 90)

    for number, (label, call) in enumerate(FAULTS, start=1):

        result = handle_tool_call(
            call,
            log=False
        )

        print(
            f"{number}. {label:<28} -> {result}"
        )

    print("=" * 90)
    print("All faults were handled as strings.")
    print("No model was used.")
    print("No exception should crash the program.")
    print("=" * 90)