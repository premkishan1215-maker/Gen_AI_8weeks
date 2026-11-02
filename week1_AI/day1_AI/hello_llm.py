import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

My_api_key=os.getenv("groq_API_keys")

if not My_api_key:
    raise ValueError("API key is not found")

client=Groq(api_key=My_api_key)

model = "openai/gpt-oss-120b"



messages=[{
    "role":"user",
    "content":"Do you know about Bihar museum world ranking among all the museums"
}]


response=client.chat.completions.create(model=model,messages=messages)
print(response.choices[0].message.content)