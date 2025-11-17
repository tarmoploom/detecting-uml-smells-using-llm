import anthropic
import os

API_key = os.getenv('ANTHROPIC_API_KEY')
if not API_key: raise ValueError("❌ Key has no value!")

client = anthropic.Anthropic(api_key=API_key)

message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": "Hey, whats up?"
        }
    ]
)

# Print the response
print(message.content[0].text)
