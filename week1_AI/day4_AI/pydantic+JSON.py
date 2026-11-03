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

##structured output

from pydantic import BaseModel
class Ticket(BaseModel):
    name:str
    email:str
    issue:str
    phone:str

schema=Ticket.model_json_schema()
response_format={"type": "json_object"}


system_prompt=f"""extract personal information from it strictly based on this schema and give me a json output. {schema}"""

message_sys={
    "role":"system",
    "content":system_prompt
}

message={
    "role":"user",
    "content":"hi, my name is prem kishan yesterday i bought a iphone from your shop and it stopped working, please contact me on this email-prem123@gmail.com, or my phon no is 96XXX71OORR0"
    
    
}

messages=[message_sys,message]

response=client.chat.completions.create(model=model,messages=messages,response_format=response_format)
answer=response.choices[0].message.content
print(answer)



## isko padhte kasie hain

import json
raw_json=answer
data_file=json.loads(raw_json)
ticket=Ticket(**data_file)

print(ticket.name)
print(ticket.email)
print(ticket.issue)