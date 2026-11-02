import os
from pathlib import Path
from groq import Groq
from dotenv import load_dotenv
  

load_dotenv()

my_api_key=os.getenv("groq_API_keys")


client=Groq(api_key=my_api_key)
if not my_api_key:
    raise ValueError("API key not found")


model="openai/gpt-oss-120b"

##structured output

from pydantic import BaseModel
class Ticket:
    name:str
    email:str
    issue:str

schema=Ticket.model_json_schema()
response_format={"type":" json_object"}


system_prompt="extract personal information from it strictly based on this schema. {schema}"

message_sys={
    "role":"system",
    "content":system_prompt
}

message={
    "role":"user",
    "content":"hi, my name is prem kishan yesterday i bought a smartphone from your shop and it stopped working, please contact me on this email-prem123@gmail.com, or my phon no is 9693577140"
    
    
}

messages=[message_sys,message]

response=client.chat.completions.create(model=model,messages=messages,response_format=response_format)
print(response.choices[0].message.content)