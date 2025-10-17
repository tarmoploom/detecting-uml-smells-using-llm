from openai import OpenAI
import os

API_key = os.getenv('OPENAI_API_KEY')
if not API_key: raise ValueError("❌ Key has no value!")

client = OpenAI(api_key=API_key)

response = client.responses.create(
  model="gpt-4.1-nano",
  input="say hello!",
  store=False,
)

print(response.output_text);
