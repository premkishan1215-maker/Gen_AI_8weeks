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

message_system={
    "role":"system",
    "content":"you are a brand manager who suggest the brand name, suggest only one name"
}

message={
    "role":"user",
    "content":"suggest me a name for my clothing company"
}

messages=[message_system,message]

response=client.chat.completions.create(model=model,messages=messages,temperature=2)
print(response.choices[0].message.content)