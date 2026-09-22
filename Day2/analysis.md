# Day 2 – Reasoning and Acting Comparison

## 1. Objective

The objective of this task is to compare three prompting approaches:

1. Direct Prompting
2. Chain-of-Thought (CoT)
3. ReAct (Reasoning + Acting)

The comparison is based on reasoning ability, tool usage, reliability, transparency, speed/cost, and consistency.

---

## 2. Direct Prompting

Direct prompting asks the model to provide the final answer without showing detailed reasoning.

### Characteristics

- Produces a direct final answer.
- Does not explicitly show the reasoning process.
- Does not use external tools.
- It is generally faster and uses fewer tokens.
- It can be suitable for simple questions.

### Limitation

For multi-step mathematical or logical problems, the final answer may be less transparent because the reasoning is not shown.

---

## 3. Chain-of-Thought (CoT)

Chain-of-Thought prompting asks the model to solve a problem step by step before giving the final answer.

### Characteristics

- Breaks a problem into smaller steps.
- Shows the intermediate reasoning used to reach the answer.
- Does not use external tools in this experiment.
- Helps with multi-step calculations and logical reasoning.
- Uses more output tokens than direct prompting.

### Results from the Experiment

### Question 1

A student takes three courses costing Rs. 12,000, Rs. 18,000 and Rs. 15,000. She gets a 15% scholarship and pays the remaining amount in 4 equal installments.

The CoT output calculated:

- Total = Rs. 45,000
- Scholarship = Rs. 6,750
- Amount after scholarship = Rs. 38,250
- Each installment = Rs. 9,562.50

**Final Answer: Rs. 9,562.50 per installment.**

### Question 2

There are 18 computers. Each computer is shared by 2 students in the morning and 3 students in the afternoon.

The CoT output calculated:

- Morning = 18 × 2 = 36 sittings
- Afternoon = 18 × 3 = 54 sittings
- Total = 36 + 54 = 90 sittings

**Final Answer: 90 student sittings.**

### Question 3

Ravi is taller than Kumar, Kumar is taller than Arun, and Priya is shorter than Arun.

The CoT output formed the relationship:

Ravi > Kumar > Arun > Priya

**Final Answer: Ravi is the tallest and Priya is the shortest.**

---

## 4. ReAct

ReAct combines reasoning with actions performed through tools.

The basic flow is:

**Thought → Action → Observation → Thought → Action → Observation → Final Answer**

In this experiment, the available tools are:

- `get_course_fee(course_code)` – retrieves the fee of a course.
- `calculator(expression)` – performs calculations.

### Characteristics

- Can interact with tools.
- Can obtain information that is not already known.
- Uses observations from tools before continuing the reasoning.
- Makes the process more traceable because actions and observations can be inspected.
- Usually takes more steps than direct prompting.
- Can be useful when a problem requires external information or computation.

For the course-fee problem, the agent retrieves the course fees using the fee tool and uses the calculator to compare the scholarship options.

The correct comparison is:

- CS101 + AI202 with 10% scholarship = Rs. 27,000
- All three courses with 25% scholarship = Rs. 33,750
- Difference = Rs. 6,750

Therefore, the first option is cheaper by **Rs. 6,750**.

---

## 5. Comparison

| Feature | Direct Prompting | Chain-of-Thought | ReAct |
|---|---|---|---|
| Reasoning | Minimal visible reasoning | Step-by-step reasoning | Reasoning combined with actions |
| Tool usage | No | No | Yes |
| External information | Cannot retrieve it directly | Cannot retrieve it directly | Can retrieve information using tools |
| Transparency | Low | Higher | High because actions and observations can be traced |
| Speed | Generally fastest | Slower than direct prompting | Usually slower because of tool calls |
| Token usage | Lower | Higher | Higher because of reasoning and tool interactions |
| Multi-step problems | Can work, but may be less reliable | Useful | Useful when tools are required |
| Best suited for | Simple questions | Calculations and logical reasoning | Problems requiring information + reasoning + tools |

---

## 6. Self-Consistency Experiment

Self-consistency was tested by running the same CoT question five times with a non-zero temperature.

### Question

A student takes three courses costing Rs. 12,000, Rs. 18,000 and Rs. 15,000. She gets a 15% scholarship on the total and pays the remaining amount in 4 equal installments.

### Results

| Run | Answer |
|---|---|
| Run 1 | 9,562.50 |
| Run 2 | 9562.5 Rs. per installment |
| Run 3 | 9,562.5 Rs. per installment |
| Run 4 | 9,562.5 Rs. per installment |
| Run 5 | 9,562.5 rupees |

All five runs produced the same numerical result: **Rs. 9,562.50 per installment**, although the wording and formatting varied.

The program's exact-answer counting treated the differently formatted responses as different strings, so it displayed:

**Majority answer (1 of 5 runs): 9,562.50**

This shows that simple string matching can fail to recognize numerically equivalent answers when the wording or formatting changes.

---

## 7. Reliability and Consistency

The experiment shows that CoT can provide detailed reasoning for multi-step calculations and logical questions.

In the self-consistency experiment, all five runs produced the same numerical answer despite small differences in formatting. This indicates numerical consistency in the observed runs.

However, the majority calculation in the program was affected by answer formatting. A more robust implementation could normalize answers before counting them, for example by extracting the numerical value.

---

## 8. Suitability

### Direct Prompting

Direct prompting is suitable when:

- The question is simple.
- A short answer is sufficient.
- Detailed reasoning is not required.
- Fast responses are preferred.

### Chain-of-Thought

CoT is suitable when:

- The problem contains multiple calculation steps.
- Logical relationships must be followed.
- The reasoning process needs to be examined.
- A simple final answer may not be enough.

### ReAct

ReAct is suitable when:

- The problem requires external information.
- Tools or APIs are needed.
- Calculations need to be performed using a tool.
- The agent must interact with an environment before producing the final answer.

---

## 9. Conclusion

Direct Prompting, Chain-of-Thought, and ReAct are useful for different types of tasks.

Direct prompting is simple and fast. CoT provides a structured step-by-step approach for multi-step reasoning. ReAct extends reasoning by allowing the model to interact with tools and use observations during problem solving.

The experiments showed that CoT successfully solved the calculation and logic questions, while the ReAct approach was useful for the course-fee problem because it could retrieve course information and perform calculations through tools.

The self-consistency experiment also showed that multiple CoT runs produced the same numerical answer, although differences in formatting affected the program's exact string-based majority calculation.