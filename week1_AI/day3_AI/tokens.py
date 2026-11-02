import os
from pathlib import Path
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

my_api_key=os.getenv("groq_API_keys")

if not my_api_key:
    raise ValueError("API key not found")

client=Groq(api_key=my_api_key)

model="openai/gpt-oss-120b"

prompt1="hi"
prompt2="Explain time travel in detail"
prompt3="write an 1000 essay on deep learning"
prompts=[prompt1,prompt2,prompt3]
for prompt in prompts:
    message={
        "role":"user",
        "content":prompt
    }
    messages=[message]

    response=client.chat.completions.create(model=model,messages=messages,max_tokens=500)
    usage=response.usage
    print(f"Prompt: {prompt} --> your_token: {usage.prompt_tokens} completion_token: {usage.completion_tokens} total_token: {usage.prompt_tokens+usage.completion_tokens} Finish reason: {response.choices[0].finish_reason}")
    ##print(response.choices[0].message.content)