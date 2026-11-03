
import os
from dotenv import load_dotenv
from groq import Groq
import json

from schemas import ResumeEvaluation
from prompts import SYSTEM_PROMPT

load_dotenv()

my_api_key = os.getenv("groq_API_keys")

if not my_api_key:
    raise ValueError("API key not found")

client = Groq(api_key=my_api_key)

model = "openai/gpt-oss-120b"

schema = ResumeEvaluation.model_json_schema()
def evaluate_resume(resume_text, job_description):

    message_sys = {
    "role": "system",
    "content": f"""
    {SYSTEM_PROMPT}

    Follow this JSON schema strictly:

    {json.dumps(schema, indent=2)}

    Return only valid JSON.
    Include all required fields.
    Do not add extra fields.
    """
    }

    message = {
        "role": "user",
        "content": f"""
        RESUME:
        {resume_text}

        JOB DESCRIPTION:
        {job_description}
        """
    }


    messages = [message_sys, message]

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        response_format={"type": "json_object"},
        temperature=0.1
    )

    result = response.choices[0].message.content

    evaluation = ResumeEvaluation.model_validate_json(result)

    return evaluation
