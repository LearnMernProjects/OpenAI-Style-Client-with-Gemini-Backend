from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# ZERO-SHOT PROMPTING
# SYSTEM_PROMPT="you must only answer coding related question and do not answer any question out of coding and your name is viraj , if someone ask irrelevant question just say sorry"

# few-SHOT PROMPTING
# SYSTEM_PROMPT=""" you must only answer coding related question and do not answer any question out of coding and your name is viraj , if someone ask irrelevant question just say sorry
# Examples:
# q1)who invented Neuman Model
# q2)What is transformer model
# q3)what is star in solar system
# answer from your side must be :- I can't answer such questions
# """

# CHAIN OF THOUGHT PROMPTING
SYSTEM_PROMPT = """You are a AI Assistant and answer the question in terms of Chain-of-thought
STRICTLY FOLLOW JSON FORMAT
ONLY RUN ONE STEP AT A TIME
OUTPUT JSON Format
{"step" : "START" | "PLAN" | "OUTPUT", "content":"string"}
"""

messageHistory = [
    {"role": "system", "content": SYSTEM_PROMPT}
]

inp = input("Enter your Question bhai: ")
messageHistory.append({"role": "user", "content": inp})

while True:
    response = client.chat.completions.create(
        model="gemini-2.5-flash",
        response_format={"type": "json_object"},
        messages=messageHistory
    )

    rawans = response.choices[0].message.content
    messageHistory.append({"role": "assistant", "content": rawans})

    parseans = json.loads(rawans)

    if parseans.get("step") == "START":
        print("⚡", parseans.get("content"))
        continue

    if parseans.get("step") == "PLAN":
        print("🧠", parseans.get("content"))
        continue

    if parseans.get("step") == "OUTPUT":
        print("🧠", parseans.get("content"))
        break


"""
SYSTEM_PROMPT = \"\"\"You are a AI Assistant and answer the question in terms of Chain-of-thought
STRICTLY FOLLOW JSON FORMAT
ONLY RUN ONE STEP AT A TIME
OUTPUT JSON Format
{"step" : "START" | "PLAN" | "OUTPUT", "content":"string"}

Example,
START:"what is a apple"
PLAN:{"STEP":"START" : "content":"from where does apple word is derived?"}
PLAN:{"STEP":"PLAN" : "content":"It's a fruit in red colour"}
OUTPUT:{"STEP":"OUTPUT" : "content":"Its structure along with its details inherited from PLAN"}
\"\"\"

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": "What is an apple"}
    ]
)

print(response.choices[0].message.content)
"""