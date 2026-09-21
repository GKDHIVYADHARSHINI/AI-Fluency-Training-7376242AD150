
# AI Fluency Training – Day 1

## Lab: Chatbot vs Rule-Based Workflow vs AI Agent

### Overview
This project was completed as part of the Day 1 AI Fluency Training lab.

The objective is to set up a Python environment in VS Code, connect it to a Large Language Model (LLM), and implement and compare three systems:

1. A plain LLM chatbot
2. A rule-based workflow
3. A tool-using AI agent

The systems are tested using a college course-fee scenario to understand their accuracy, flexibility, and limitations.

## Problem Statement
A college has the following private course-fee data:

| Course Code | Fee |
|---|---:|
| CS101 | Rs. 12,000 |
| AI202 | Rs. 18,000 |
| DS303 | Rs. 15,000 |

The systems are tested on course-fee questions, scholarship calculations, fee comparisons, and a welcome-message task.

## Technologies Used
- Python
- Visual Studio Code
- OpenAI Python client
- python-dotenv
- Groq API
- Large Language Models (LLMs)

## Project Structure

```text
Day1/
├── agent.py
├── chatbot.py
├── workflow.py
├── tools.py
├── config.py
├── check_setup.py
├── challenge.py
├── requirements.txt
├── .gitignore
└── outputs/
    └── [output screenshots]
```

## System Description

### 1. Chatbot
Sends user questions directly to the LLM without access to the college's private fee data or external tools.

### 2. Rule-Based Workflow
Uses predefined Python rules and conditions to answer supported course-fee questions. It provides consistent results for programmed cases but may fail on unfamiliar questions or wording.

### 3. AI Agent
Uses an LLM, tools, and an execution loop. The agent can look up course fees, perform calculations, and use tool results to prepare an answer.

## Tools Used by the Agent
- `get_course_fee`: Retrieves the fee for a course.
- `calculator`: Performs arithmetic calculations.

## How to Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure the API key
Create a local `.env` file and configure your selected LLM provider and API key.

**Do not upload `.env` or any API key to GitHub.**

### 3. Run the setup check
```bash
python check_setup.py
```

### 4. Run the programs
```bash
python chatbot.py
python workflow.py
python agent.py
python challenge.py
```

## Challenge
The challenge asks which two courses can be taken together within a budget of Rs. 30,000.

The workflow may not handle this question because no specific rule was designed for it. The agent can use fee-lookup and calculator tools to evaluate possible combinations.

## Output Screenshots
Screenshots of the program outputs are included in the `outputs/` folder.

## Learning Outcomes
- Understood the differences between chatbots, rule-based workflows, and AI agents.
- Practiced connecting Python applications to an LLM.
- Learned how an AI agent uses tools and an execution loop.
- Observed hallucination, rule rigidity, and possible agent tool-use failures.
- Compared the strengths and limitations of different AI systems.
