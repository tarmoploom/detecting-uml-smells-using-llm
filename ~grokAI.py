# from xai_sdk import Client
import requests
import os

API_key = os.getenv('GROK_API_KEY')
if not API_key: raise ValueError("❌ Key has no value!")

# client = Client(api_key=API_key)

def grok_chat(prompt, model="grok-4-fast-reasoning", max_tokens=150):
    """WORKS 100% - Direct API call"""
    response = requests.post(
        "https://api.x.ai/v1/chat/completions",  # Official endpoint
        headers={
            "Authorization": f"Bearer {API_key}",
            "Content-Type": "application/json"
        },
        json={
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
            "temperature": 0.7
        }
    ).json()
    
    if 'error' in response:
        print(f"❌ API Error: {response['error']}")
        return None
    
    return response['choices'][0]['message']['content']


print(grok_chat(
    "Hey, whats cooking?", 
))


# Best Models for this project according to Grok:

# Best Model: grok-4-fast-reasoning
# Why it's the best for XMI/UML smell detection:

# Advanced reasoning needed to parse XMI structure, understand UML semantics, and identify design smells (e.g., "this class has 18 attributes → Data Class smell")
# 2M token context handles large XMI files easily (most UML models < 500K tokens)
# Fast & cost-efficient ($0.20/$0.50 per 1M tokens) for iterative analysis
# Structured output support for clean JSON smell reports

# Runner-up: grok-code-fast-1 if your XMI includes code generation artifacts.
