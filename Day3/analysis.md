# Day 3 Analysis – ReAct Agent from Scratch

## 1. Aim

The aim of this lab is to build a ReAct agent from scratch using plain Python.

The agent uses two tools:

1. `calculator` – safely performs arithmetic calculations.
2. `read_webpage` – reads a web page or local HTML/text file.

The agent follows the ReAct cycle:

**Reason → Act → Observe → Reason → ... → Final Answer**

The lab also deliberately triggers three failure modes:

- Repeating tool-call loop
- Hallucinated/unknown tool call
- Context overflow and runaway cost

Finally, guards are added to make the agent safer and more reliable.


## 2. What is a ReAct Agent?

ReAct means **Reasoning + Acting**.

Instead of only generating an answer, the agent can decide when it needs to use an external tool.

The basic flow is:

1. The user asks a question.
2. The model reasons about whether a tool is needed.
3. The model requests a tool call.
4. The program executes the requested tool.
5. The tool returns an observation.
6. The observation is given back to the model.
7. The model continues reasoning.
8. The process stops when the model gives a final answer.

In this lab, the agent can read the fee notice and then use the calculator to calculate the required amount.


## 3. Tools Used

### 3.1 Calculator

The `calculator(expression)` tool performs arithmetic operations.

Example:

```text
(12000 + 18000) * 0.9