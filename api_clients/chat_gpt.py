from openai import OpenAI
import json
import os

API_key = os.getenv('OPENAI_API_KEY')
if not API_key: raise ValueError("❌ Key has no value!")

client = OpenAI(api_key=API_key)

# Load the smell reference JSON
with open("chatGPT Smell_Reference.json", "r") as f:
    smell_reference = json.load(f)

# Load your UML model (XMI)
with open("example_model.xmi", "r") as f:
    uml_xmi = f.read()

# Construct the prompt
messages = [
    {
        "role": "system",
        "content": (
            "You are a UML model quality analyzer. "
            "You detect UML model bad smells using the provided JSON definitions."
        )
    },
    {
        "role": "user",
        "content": (
            f"REFERENCE DEFINITIONS:\n{json.dumps(smell_reference, indent=2)}\n\n"
            f"UML MODEL (XMI):\n{uml_xmi}\n\n"
            "TASK:\n"
            "Analyze the UML model using the smell definitions. "
            "Return a structured JSON list with the following fields:\n"
            "[{id, name, evidence, severity, reasoning, confidence}].\n"
            "Focus on high-detectability smells first."
        )
    }
]

# basic request example:
# response = client.responses.create(
#   model="gpt-4.1-nano",
#   input="say hello!",
#   store=False,
# )

response = client.chat.completions.create(
    model="gpt-5",  # or "gpt-4.1-turbo", etc.
    messages=messages,
    temperature=0,
    response_format={"type": "json_object"}  # optional, if you want guaranteed JSON
)

print(response.choices[0].message["content"])

# basic response example:
# print(response.output_text);