from groq import Groq
import os
from dotenv import load_dotenv
from tool import get_course_fee, calculator

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MODEL = "openai/gpt-oss-20b"


def agent(question):

    # 🔹 Fee lookup tool
    if "fee" in question.lower():
        course = question.split()[-1].replace("?", "").lower()
        result = get_course_fee(course)
        return f"Fee for {course.upper()} is {result}"

    # 🔹 Calculator tool
    elif any(op in question for op in ["+", "-", "*", "/"]):
        import re
        match = re.search(r"\d+\s*[\+\-\*/]\s*\d+", question)

        if match:
            expression = match.group()
            result = calculator(expression)
            return f"Result is {result}"
        else:
            return "Could not find valid calculation"

    # 🔹 Normal LLM response
    else:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": question}]
        )
        return response.choices[0].message.content


if __name__ == "__main__":
    while True:
        q = input("You: ")
        if q.lower() == "exit":
            break
        print("Agent:", agent(q))