# Day 6 Task – Reliable Tool Calling and Structured Outputs

## 1. Scenario

For this task, I built a Student Study Assistant.

The assistant has two tools:

1. `get_subject_hours` – returns recommended study hours for Python, DSA, DBMS, or AI.
2. `calculate_study_time` – evaluates a basic arithmetic expression for study-time calculations.

The scenario is intentionally simple so that the focus remains on reliable tool calling, validation, fault handling, and structured outputs.

---

## 2. Important Concepts

### 2.1 Parallel tool calls

A model can return more than one tool call in a single response.

When this happens, the agent loop must process every tool call and return exactly one tool message for every `tool_call_id`.

If one tool call is left unanswered, the conversation can become invalid or the model may not be able to continue correctly.

In my Student Study Assistant, a question asking for study hours for multiple subjects can require multiple calls to `get_subject_hours`.

---

### 2.2 Tool calls are generated text

A model-generated tool call cannot automatically be trusted.

The following failures are possible:

- Invalid JSON
- Unknown tool
- Missing required argument
- Wrong argument type
- Value outside an allowed enum
- Invented extra argument
- Truncated response
- Repeated identical calls

My agent handles these failures before executing a tool.

The four main stages are:

1. Parse the JSON arguments.
2. Look up the requested tool.
3. Validate the arguments against the schema.
4. Execute the tool.

Failures are returned as strings instead of allowing the program to crash.

---

### 2.3 Repair pattern

Every tool call passes through the same guarded pipeline.

Invalid JSON is detected during parsing.

An unknown tool is detected during tool lookup.

Missing arguments, wrong types, invalid enum values, and extra arguments are detected by the validator.

Only valid arguments reach the actual tool function.

A response with `finish_reason = length` is treated differently because the model response was truncated. In that case, the agent retries with a larger token limit.

Repeated identical calls are detected using a call signature and stopped after the configured limit.

The agent also has a maximum number of steps so that it cannot loop forever.

---

### 2.4 Fault injection

Fault injection means deliberately giving the agent handler broken inputs instead of waiting for a real model to generate them.

My `task_inject_faults.py` script does not use a model or internet connection.

This makes the tests fast, deterministic, and repeatable.

It also shows that many agent reliability problems occur in the application layer around the model, especially parsing, validation, tool lookup, and execution.

---

# 3. Tool Calling vs Structured Outputs

| Basis for comparison | Tool calling | Structured outputs |
|---|---|---|
| What the model is asked to do | Request an action by selecting a tool and providing arguments | Return data in a specified structure |
| Who performs the action or produces the final data | My Python tool function performs the action | The model produces the structured data |
| How the shape of the result is controlled | Tool arguments are controlled by a JSON Schema | The response is controlled by JSON mode or a strict JSON Schema |
| What can still go wrong | Invalid JSON, wrong tool, missing arguments, wrong type, invalid values, repeated calls, truncation | Unsupported schema mode, wrong shape, invalid JSON, or provider/model limitations |
| How my code guards against it | Parsing, schema validation, tool lookup, execution errors, repeat detection, and maximum-step limit | JSON parsing and validation of required fields, types, enums, and extra fields |
| Support across servers and models | Generally available through OpenAI-compatible tool calling, but exact behavior varies | JSON mode and strict schema support can vary by provider and model |
| My choice if the task is to fetch or calculate something | **Tool calling** – the Python function should perform the calculation or lookup | Not my first choice because structured output does not itself perform the action |
| My choice if the task is to pull fields out of a sentence | **Structured outputs** – the required fields can be returned directly in a predictable format | Best choice because the model only needs to extract and format information |

---

# 4. Fault Injection Results

The fault-injection script tests deliberately broken tool calls.

| Injected fault | Message returned | Did the run continue? |
|---|---|---|
| Good control call | Valid tool result | Y |
| Invalid JSON | Argument error describing invalid JSON | Y |
| Unknown tool | Unknown tool message | Y |
| Missing required argument | Missing required argument message | Y |
| Wrong type | Argument must be a string message | Y |
| Value outside enum | Value must be one of the allowed subjects | Y |
| Invented extra argument | Unexpected argument message | Y |
| JSON array instead of object | Arguments must be a JSON object | Y |
| Invalid difficulty | Difficulty must be one of the allowed enum values | Y |

All failures are converted into messages rather than crashing the program.

---

# 5. Agent Behaviour

## Question 1 – Single tool

**Question:**  
"How many hours should I study DSA?"

**Observed behaviour:**

- Steps: 1
- Tool call: `get_subject_hours({"subject": "DSA"})`
- Tool result: 3
- Final answer: The assistant recommended 3 hours.
- Parallel calls: No
- `finish_reason = length`: No

This demonstrates a normal single-tool interaction.

---

## Question 2 – Multiple subjects

**Question:**  
"How many hours should I study Python and DSA in total?"

**Observed behaviour:**

- The model called `get_subject_hours` for Python.
- The model then called `get_subject_hours` for DSA.
- Python returned 2 hours.
- DSA returned 3 hours.
- The final answer reported a total of 5 hours.
- `finish_reason = length`: No.

In my first run, the two calls arrived in separate agent steps rather than in the same response. Therefore, I did not count this particular run as a true same-response parallel call.

The important implementation requirement is still supported because the loop processes every tool call in a response and creates one tool message for each `tool_call_id`.

---

## Question 3 – Invalid subject

**Question:**  
"How many hours should I study JavaScript?"

The assistant recognized that JavaScript was not one of the supported subjects.

The response did not crash and did not execute a tool with an unsupported subject.

This demonstrates safe handling of an invalid requested value.

---

## Question 4 – No tool required

**Question:**  
"Give me a one-line study motivation message."

The model answered directly without calling a tool.

This shows that tools should only be used when an external action or calculation is actually required.

---

# 6. Before and After Guards

For a tool-calling system, guards are important because the model's generated arguments are not automatically trustworthy.

### Unguarded behaviour

Without validation and safety guards, malformed JSON, unknown tools, missing arguments, wrong types, or invented fields could reach the execution layer.

This could result in exceptions or incorrect tool execution.

### Guarded behaviour

My guarded agent:

1. Parses JSON.
2. Checks whether the tool exists.
3. Validates arguments.
4. Executes only valid calls.
5. Converts failures into strings.
6. Detects repeated calls.
7. Limits the number of steps.
8. Retries truncated responses with more tokens.

The guarded version is therefore safer and more predictable.

---

# 7. Structured Outputs

The structured-output experiment compares three response formats:

### Case 1 – No constraint

The model is free to return normal text.

This format is easy for a human to read, but parsing the exact fields is less reliable because the output shape is not guaranteed.

### Case 2 – JSON mode

JSON mode requires valid JSON but does not necessarily enforce the exact application-specific fields.

This is better for machine parsing than free text, but the application still needs to validate the resulting structure.

### Case 3 – Strict JSON Schema

Strict schema mode requests a specific JSON structure containing:

- `subject`
- `hours`
- `priority`
- `reason`

My program then parses the response and validates the required fields and types.

Provider support for strict schema output can vary. If the provider rejects the schema request, that is recorded as a provider capability limitation rather than treating it as a Python program crash.

---

# 8. Suitability and Conclusion

The Student Study Assistant is a suitable example for demonstrating reliable tool calling because the model must decide when to request a calculation or recommendation from a Python function.

Some failures can occur naturally from model behaviour, such as choosing an unsupported subject or making multiple tool calls. Other failures, such as malformed JSON, invented arguments, or deliberately invalid types, are easier to test through fault injection.

The most important guard in this task is schema validation. It prevents malformed or unexpected arguments from reaching the tool functions. The maximum-step and repeated-call guards are also important because they prevent the agent from running indefinitely.

I would use a tool when the model needs to perform an action, calculate something, or retrieve information through application code. For example, calculating the total study time is better handled by a Python tool.

I would use structured output when the main requirement is to extract information into a predictable format. For example, extracting a subject, number of hours, priority, and reason from a student's request is suitable for structured output.

A model's tool call can never be trusted simply because it was generated by the model. Every reply must be parsed, checked, validated, and safely executed. A schema can prevent many argument-level problems, such as missing fields, invalid types, invalid enum values, and extra properties. However, a schema cannot prevent every problem, such as an unknown business condition, an incorrect decision by the model, provider limitations, or an infinite reasoning loop.

Deliberate fault injection provides a reliable way to test these protections because the developer can supply known failures directly to the handler. Waiting for a model to randomly produce every possible failure would be slower and unreliable. Fault injection therefore makes agent reliability testing repeatable and easier to automate.

Overall, this task showed that reliable agents are not only about getting the model to call tools. The application must treat every model response as untrusted input and surround the model with validation, error handling, retry logic, and limits.