"""Day 6 Task: Robust Student Study Assistant agent."""

import sys
from pathlib import Path
import json


# ============================================================
# Use the existing Day1 configuration
# ============================================================

DAY1_PATH = Path(__file__).resolve().parent.parent / "Day1"
sys.path.insert(0, str(DAY1_PATH))


# ============================================================
# Imports
# ============================================================

from config import client, MODEL, banner

from task_tools import (
    TOOLS,
    TOOL_FUNCTIONS,
    SCHEMAS,
)

from task_validate import validate_arguments


# ============================================================
# System prompt
# ============================================================

SYSTEM_PROMPT = (
    "You are a student study assistant. "
    "Use get_subject_hours whenever the user asks about "
    "recommended study time for a subject. "
    "Use calculate_study_time for arithmetic calculations. "
    "Valid subjects are Python, DSA, DBMS and AI. "
    "If no tool is needed, answer directly."
)


# ============================================================
# Settings
# ============================================================

MAX_TOKENS = 500
REPEAT_LIMIT = 3
MAX_STEPS = 6


# ============================================================
# Tool-call handler
# ============================================================

def handle_tool_call(call, log=True):
    """
    Safely process one model-generated tool call.

    Four stages:
    1. Parse JSON
    2. Look up the tool
    3. Validate arguments
    4. Execute the tool
    """

    name = call.function.name
    raw = call.function.arguments or "{}"

    # --------------------------------------------------------
    # Stage 1: Parse JSON
    # --------------------------------------------------------

    try:
        arguments = json.loads(raw)

    except json.JSONDecodeError as error:

        return (
            f"Argument error: invalid JSON ({error}). "
            f"Send valid JSON for '{name}'."
        )

    # --------------------------------------------------------
    # Stage 2: Look up the tool
    # --------------------------------------------------------

    function = TOOL_FUNCTIONS.get(name)

    if function is None:

        return (
            f"Unknown tool: {name}. "
            f"Available tools: {', '.join(TOOL_FUNCTIONS)}."
        )

    # --------------------------------------------------------
    # Stage 3: Validate arguments
    # --------------------------------------------------------

    problem = validate_arguments(
        arguments,
        SCHEMAS[name]
    )

    if problem:

        return f"Argument error: {problem}"

    # --------------------------------------------------------
    # Stage 4: Execute the tool
    # --------------------------------------------------------

    try:

        result = str(
            function(**arguments)
        )

    except Exception as error:

        result = (
            f"Tool error in {name}: "
            f"{type(error).__name__}: {error}"
        )

    if log:

        print(
            f"   {name}({arguments}) -> "
            f"{result[:100]}"
        )

    return result


# ============================================================
# Robust agent
# ============================================================

def agent(
    question,
    max_steps=MAX_STEPS,
    verbose=True
):
    """Run the robust Student Study Assistant agent."""

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        },
        {
            "role": "user",
            "content": question,
        },
    ]

    # Track repeated tool calls
    seen = {}

    # Initial token limit
    max_tokens = MAX_TOKENS

    # --------------------------------------------------------
    # Agent loop
    # --------------------------------------------------------

    for step in range(1, max_steps + 1):

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
            temperature=0,
            max_tokens=max_tokens,
        )

        choice = response.choices[0]
        message = choice.message

        # ----------------------------------------------------
        # Guard 1: truncated response
        # ----------------------------------------------------

        if choice.finish_reason == "length":

            if max_tokens >= 2000:

                return (
                    "Stopped: the reply was still truncated "
                    "at 2000 tokens."
                )

            max_tokens *= 2

            if verbose:

                print(
                    f" step {step}: truncated, "
                    f"retrying with max_tokens={max_tokens}"
                )

            continue

        # ----------------------------------------------------
        # No tool call = final answer
        # ----------------------------------------------------

        if not message.tool_calls:

            return (
                message.content or ""
            ).strip()

        # ----------------------------------------------------
        # Add assistant message containing tool calls
        # ----------------------------------------------------

        messages.append(
            {
                "role": "assistant",
                "content": message.content or "",
                "tool_calls": [
                    {
                        "id": call.id,
                        "type": "function",
                        "function": {
                            "name": call.function.name,
                            "arguments": call.function.arguments,
                        },
                    }
                    for call in message.tool_calls
                ],
            }
        )

        if verbose:

            print(
                f" step {step}: "
                f"{len(message.tool_calls)} tool call(s)"
            )

        # ----------------------------------------------------
        # Handle ALL tool calls
        # ----------------------------------------------------

        for call in message.tool_calls:

            signature = (
                call.function.name,
                call.function.arguments,
            )

            seen[signature] = (
                seen.get(signature, 0) + 1
            )

            # ------------------------------------------------
            # Guard 2: repeated identical calls
            # ------------------------------------------------

            if seen[signature] >= REPEAT_LIMIT:

                return (
                    f"Stopped: {call.function.name} "
                    f"was called {REPEAT_LIMIT} times "
                    "with the same arguments and made no progress."
                )

            # ------------------------------------------------
            # Process tool call
            # ------------------------------------------------

            result = handle_tool_call(
                call,
                log=verbose
            )

            # ------------------------------------------------
            # Exactly one tool message per tool_call_id
            # ------------------------------------------------

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": call.id,
                    "content": result,
                }
            )

    # --------------------------------------------------------
    # Guard 3: maximum steps
    # --------------------------------------------------------

    return (
        "Stopped: maximum steps reached "
        "without a final answer."
    )


# ============================================================
# Main program
# ============================================================

if __name__ == "__main__":

    banner(
        "DAY 6 TASK - STUDENT STUDY ASSISTANT"
    )

    questions = [

        # 1. Single tool
        "How many hours should I study DSA?",

        # 2. Possible parallel tool calls
        "How many hours should I study Python and DSA in total?",

        # 3. Invalid subject
        "How many hours should I study JavaScript?",

        # 4. No tool needed
        "Give me a one-line study motivation message.",
    ]

    for question in questions:

        print("\nQ:", question)

        try:

            answer = agent(question)

            print("A:", answer)

        except Exception as error:

            print(
                "Agent error:",
                type(error).__name__,
                error
            )