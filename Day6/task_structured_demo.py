"""Day 6 Task: Strict structured output demo."""

import json

from task_robust_agent import client, MODEL, SYSTEM_PROMPT


STUDY_PLAN_SCHEMA = {
    "type": "object",
    "properties": {
        "subject": {
            "type": "string",
            "enum": ["Python", "DSA", "DBMS", "AI"],
        },
        "hours": {
            "type": "integer",
        },
        "priority": {
            "type": "string",
            "enum": ["low", "medium", "high"],
        },
        "reason": {
            "type": "string",
        },
    },
    "required": [
        "subject",
        "hours",
        "priority",
        "reason",
    ],
    "additionalProperties": False,
}


def validate_study_plan(data):
    """Validate the structured study-plan object."""

    if not isinstance(data, dict):
        return "Output must be a JSON object."

    required = STUDY_PLAN_SCHEMA["required"]

    for key in required:
        if key not in data:
            return f"Missing required field: {key}"

    if set(data) != set(required):
        extra = set(data) - set(required)
        return f"Unexpected field(s): {', '.join(extra)}"

    if data["subject"] not in ["Python", "DSA", "DBMS", "AI"]:
        return "Invalid subject."

    if not isinstance(data["hours"], int):
        return "hours must be an integer."

    if data["priority"] not in ["low", "medium", "high"]:
        return "Invalid priority."

    if not isinstance(data["reason"], str):
        return "reason must be a string."

    return None


def create_study_plan(subject):
    """Ask the model for a strict JSON study plan."""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "Return ONLY valid JSON. "
                    "Do not use markdown. "
                    "Follow the supplied study-plan schema."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Create a study plan for {subject}. "
                    "Recommend realistic study hours and priority."
                ),
            },
        ],
        temperature=0,
        max_tokens=300,
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "study_plan",
                "strict": True,
                "schema": STUDY_PLAN_SCHEMA,
            },
        },
    )

    content = response.choices[0].message.content

    try:
        data = json.loads(content)
    except json.JSONDecodeError as error:
        return None, f"Invalid JSON: {error}"

    problem = validate_study_plan(data)

    if problem:
        return None, problem

    return data, None


if __name__ == "__main__":

    print("=" * 80)
    print("DAY 6 TASK - STRICT STRUCTURED OUTPUT")
    print("=" * 80)

    subject = "DSA"

    print(f"\nRequesting structured study plan for: {subject}")

    try:
        plan, error = create_study_plan(subject)

        if error:
            print("\nValidation failed:")
            print(error)

        else:
            print("\nValidated structured output:")
            print(json.dumps(plan, indent=2))

            print("\nRequired fields present:")
            for field in STUDY_PLAN_SCHEMA["required"]:
                print(f"  ✓ {field}")

    except Exception as error:
        print(
            "\nStructured-output error:",
            type(error).__name__,
            error,
        )