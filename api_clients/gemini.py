import google.generativeai as genai
import os

API_key = os.getenv('GEMINI_API_KEY')
if not API_key: raise ValueError("❌ Key has no value!")

genai.configure(api_key=API_key)

try:
    # Initialize the generative model with the specific Gemini 2.5 Pro ID
    model = genai.GenerativeModel('gemini-2.5-pro')

    # Define your prompt.
    prompt = "Hey, gemini 2.5 pro, how's it going?"

    # Generate content based on the prompt.
    response = model.generate_content(prompt)

    # Print the generated text.
    print(response.text)

except Exception as e:
    print(f"An error occurred: {e}")
