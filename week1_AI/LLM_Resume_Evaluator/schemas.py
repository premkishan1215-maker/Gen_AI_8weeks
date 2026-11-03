
from pydantic import BaseModel, Field
from typing import List


class ResumeEvaluation(BaseModel):

    match_score: int = Field(
        description="Resume match score between 0 and 100"
    )

    matched_skills: List[str] = Field(
        description="Skills from the job description supported by the resume"
    )

    missing_skills: List[str] = Field(
        description="Relevant job skills not evidenced in the resume"
    )

    strengths: List[str]

    weaknesses: List[str]

    suggestions: List[str]

    summary: str
