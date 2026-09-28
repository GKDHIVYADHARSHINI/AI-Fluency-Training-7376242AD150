# Day 3 – ReAct Agent from Scratch

## Overview

This project is part of the Agentic AI: Foundations and Open-Source Practice training.

The Day 3 task focuses on building a ReAct agent from scratch using plain Python.

## Tools

The agent uses two tools:

- calculator – performs safe arithmetic calculations.
- ead_webpage – reads web pages and local HTML/text files.

## ReAct Cycle

The agent follows:

**Reason ? Act ? Observe ? Final Answer**

## Failure Modes

Three failure modes were deliberately tested:

1. Repeating tool-call loop
2. Hallucinated / unknown tool call
3. Context overflow and runaway cost

## Fixes

The fixed agent includes:

- Repeat-call detection
- Tool-output truncation
- Character-budget protection

## Files

| File | Purpose |
|---|---|
| my_tools.py | Calculator and webpage-reader tools |
| my_agent.py | ReAct agent without the additional guards |
| my_agent_fixed.py | ReAct agent with safety guards |
| make_big_page.py | Creates the large HTML file for testing |
| 
otice.html | Fee notice used for testing |
| ig.html | Large HTML file used for context testing |
| nalysis.md | Detailed analysis and observations |
| equirements.txt | Python dependencies |
| Screenshots/ | Screenshots of the experiments |

## Main Result

The agent successfully used the webpage reader and calculator together and was then tested against deliberate failure cases. Safety guards were added to make the agent stop repeated calls and limit excessive context.

