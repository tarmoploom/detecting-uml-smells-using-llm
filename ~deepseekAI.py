from openai import OpenAI
import os

API_key = os.getenv('DEEPSEEK_API_KEY')
if not API_key: 
    raise ValueError("❌ API Key not found!")

client = OpenAI(
    api_key=API_key, 
    base_url="https://api.deepseek.com/v1"  # Note: /v1 endpoint
)

# Your XMI content - replace this with actual XMI file content
xmi_content = """<?xml version="1.0" encoding="UTF-8"?>
<uml:Model xmi:version="2.1" xmlns:xmi="http://www.omg.org/spec/XMI/2.1" xmlns:uml="http://www.eclipse.org/uml2/5.0.0/UML">
  <packagedElement xmi:type="uml:Class" xmi:id="_Class1" name="Manager"/>
  <packagedElement xmi:type="uml:Class" xmi:id="_Class2" name="DataProcessor"/>
</uml:Model>"""

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {
            "role": "user", 
            "content": f"""Analyze this UML XMI file for model quality issues. Detect these specific smells:

HIGH PRIORITY:
- G5: Unused model elements with no dependencies
- G6: Duplicate or redundant elements
- G9: High coupling between packages/classes
- G25: Poor attribute type choices
- N1: Vague or unclear naming
- N3: Naming convention violations
- N4: Encoded names with prefixes
- S1: Overly large diagrams
- S2: Long lines between distant elements
- S3: Modeling style violations
- S4: Using names for structure instead of packages

MODERATE PRIORITY:
- G2: Expired or deprecated elements
- G3: Obvious or redundant comments
- G7: Mixed abstraction levels
- G8: Inconsistent representation
- G10: Unfocused diagrams
- G17: Multi-task processes
- G18: Unnecessary decomposition
- G27: Negative conditionals

Format each finding as: [SmellID] ElementName - Brief explanation

XMI Content:
{xmi_content}"""
        }
    ],
    stream=False
)

print(response.choices[0].message.content)
