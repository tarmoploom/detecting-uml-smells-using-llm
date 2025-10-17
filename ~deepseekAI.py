from openai import OpenAI
import os

API_key = os.getenv('DEEPSEEK_API_KEY')
if not API_key: 
    raise ValueError("❌ API Key not found!")

client = OpenAI(
    api_key=API_key, 
    base_url="https://api.deepseek.com/v1"  # Note: /v1 endpoint
)

response = client.chat.completions.create(
    model="deepseek-chat",  # Use "deepseek-chat" for latest model
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "Hello DeepSeek, whats new?"},
    ],
    stream=False
)

print(response.choices[0].message.content)
