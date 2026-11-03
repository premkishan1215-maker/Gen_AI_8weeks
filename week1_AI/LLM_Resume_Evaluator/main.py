from utils import extract_text
from evaluator import evaluate_resume

resume_text = extract_text("resume.pdf")

job_description = """
We are looking for a Machine Learning Engineer.

Required skills:
Python, Machine Learning, SQL, Deep Learning,
TensorFlow, Docker and AWS.

Experience:
Candidates should have experience in machine learning
projects and model deployment.
"""

result = evaluate_resume(resume_text, job_description)

print("\n========== RESUME EVALUATION ==========")
print("Match Score:", result.match_score)

print("\nMatched Skills:")
for skill in result.matched_skills:
    print("-", skill)

print("\nMissing Skills:")
for skill in result.missing_skills:
    print("-", skill)

print("\nSuggestions:")
for suggestion in result.suggestions:
    print("-", suggestion)

print("\nSummary:")
print(result.summary)