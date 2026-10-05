"""Day 6 Task: Student Study Assistant tools."""

import ast
import operator


SUBJECT_HOURS = {
    "Python": 2,
    "DSA": 3,
    "DBMS": 2,
    "AI": 4,
}


def get_subject_hours(subject: str, difficulty: str = "normal") -> str:
    """Return recommended study hours for a subject."""

    subject = subject.strip()

    if subject not in SUBJECT_HOURS:
        return (
            f"Unknown subject: {subject}. "
            f"Valid subjects: {', '.join(SUBJECT_HOURS)}"
        )

    hours = SUBJECT_HOURS[subject]

    if difficulty == "easy":
        hours -= 1
    elif difficulty == "hard":
        hours += 1

    return str(max(hours, 1))


_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}


def _evaluate(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value

    if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](
            _evaluate(node.left),
            _evaluate(node.right),
        )

    raise ValueError("Unsupported expression")


def calculate_study_time(expression: str) -> str:
    """Calculate a basic study-time expression."""

    try:
        result = _evaluate(ast.parse(expression, mode="eval").body)
        return str(result)
    except Exception as error:
        return (
            f"Calculator error: {error}. "
            "Use only numbers and + - * /."
        )


TOOL_FUNCTIONS = {
    "get_subject_hours": get_subject_hours,
    "calculate_study_time": calculate_study_time,
}


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_subject_hours",
            "description": (
                "Get recommended study hours for one subject. "
                "Valid subjects: Python, DSA, DBMS, AI."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "subject": {
                        "type": "string",
                        "enum": ["Python", "DSA", "DBMS", "AI"],
                        "description": "The subject to study.",
                    },
                    "difficulty": {
                        "type": "string",
                        "enum": ["easy", "normal", "hard"],
                        "description": "Study difficulty level.",
                    },
                },
                "required": ["subject"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_study_time",
            "description": (
                "Calculate a basic arithmetic expression for study time."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": (
                            "Arithmetic expression using numbers and + - * /."
                        ),
                    }
                },
                "required": ["expression"],
                "additionalProperties": False,
            },
        },
    },
]


# Same schemas are sent to the model and used by the validator.
SCHEMAS = {
    tool["function"]["name"]: tool["function"]["parameters"]
    for tool in TOOLS
}


if __name__ == "__main__":
    print("Available subjects:", ", ".join(SUBJECT_HOURS))
    print("Python:", get_subject_hours("Python"))
    print("DSA:", get_subject_hours("DSA"))
    print("Hard AI:", get_subject_hours("AI", "hard"))
    print("Calculation:", calculate_study_time("(2 + 3) * 2"))