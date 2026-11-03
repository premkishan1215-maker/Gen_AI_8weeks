
import streamlit as st
import csv
import io
import time

from utils import extract_text
from evaluator import evaluate_resume


# Page configuration
st.set_page_config(
    page_title="Bulk Resume Evaluator",
    page_icon="📄",
    layout="wide"
)

st.title("📄 AI Bulk Resume Evaluator")
st.write(
    "Upload multiple resumes and evaluate them against "
    "a single job description using AI."
)

st.divider()


# 1. Upload multiple resumes
st.subheader("1. Upload Resumes")

uploaded_files = st.file_uploader(
    "Select multiple PDF or DOCX resumes",
    type=["pdf", "docx"],
    accept_multiple_files=True
)

if uploaded_files:
    st.success(f"{len(uploaded_files)} resumes uploaded successfully.")


# 2. Job description
st.subheader("2. Enter Job Description")

job_description = st.text_area(
    "Paste the job description here",
    height=200,
    placeholder="Enter job requirements, skills and experience..."
)


# 3. Select top candidates
st.subheader("3. Select Top Candidates")

if uploaded_files:
    top_n = st.number_input(
        "How many top candidates do you want?",
        min_value=1,
        max_value=len(uploaded_files),
        value=min(5, len(uploaded_files)),
        step=1
    )
else:
    top_n = 1
    st.info("Upload resumes to select top candidates.")

st.divider()


# 4. Evaluate all resumes
if st.button("🚀 Evaluate All Resumes", type="primary"):

    if not uploaded_files:
        st.error("Please upload at least one resume.")

    elif not job_description.strip():
        st.error("Please enter a job description.")

    else:

        results = []
        errors = []

        progress_bar = st.progress(0)
        status_text = st.empty()

        total_files = len(uploaded_files)

        # Process each resume
        for index, uploaded_file in enumerate(uploaded_files):

            status_text.write(
                f"Analyzing {uploaded_file.name} "
                f"({index + 1}/{total_files})"
            )

            try:
                # Extract resume text
                resume_text = extract_text(uploaded_file)

                # Send request to Groq
                result = evaluate_resume(
                    resume_text,
                    job_description
                )

                results.append({
                    "filename": uploaded_file.name,
                    "match_score": result.match_score,
                    "matched_skills": result.matched_skills,
                    "missing_skills": result.missing_skills,
                    "strengths": result.strengths,
                    "weaknesses": result.weaknesses,
                    "suggestions": result.suggestions,
                    "summary": result.summary
                })

            except Exception as e:
                errors.append({
                    "filename": uploaded_file.name,
                    "error": str(e)
                })

            progress_bar.progress((index + 1) / total_files)

            # Wait 5 seconds before the next request
            if index < total_files - 1:
                status_text.info(
                    "Waiting 5 seconds before next request..."
                )
                time.sleep(5)

        # Evaluation completed
        status_text.write("Evaluation completed!")

        st.divider()

        # 5. Display summary
        st.subheader("4. Resume Evaluation Results")

        st.write(f"Successfully evaluated: {len(results)}")
        st.write(f"Failed evaluations: {len(errors)}")

        if results:

            # Sort candidates by match score
            results.sort(
                key=lambda x: x["match_score"],
                reverse=True
            )

            # Select top N candidates
            top_candidates = results[:int(top_n)]

            # Create summary table
            summary_data = []

            for rank, item in enumerate(top_candidates, start=1):
                summary_data.append({
                    "Rank": rank,
                    "Resume": item["filename"],
                    "Match Score": item["match_score"]
                })

            st.dataframe(
                summary_data,
                use_container_width=True,
                hide_index=True
            )

            st.divider()

            # 6. Detailed candidate results
            st.subheader("5. Detailed Candidate Analysis")

            for rank, item in enumerate(top_candidates, start=1):

                with st.expander(
                    f"Rank {rank}: {item['filename']} "
                    f"— {item['match_score']}/100"
                ):

                    st.metric(
                        "Resume Match Score",
                        f"{item['match_score']}/100"
                    )

                    st.progress(
                        max(0, min(100, item["match_score"])) / 100
                    )

                    col1, col2 = st.columns(2)

                    with col1:
                        st.markdown("### ✅ Matched Skills")

                        for skill in item["matched_skills"]:
                            st.write(f"• {skill}")

                    with col2:
                        st.markdown("### ❌ Missing Skills")

                        for skill in item["missing_skills"]:
                            st.write(f"• {skill}")

                    col3, col4 = st.columns(2)

                    with col3:
                        st.markdown("### 💪 Strengths")

                        for strength in item["strengths"]:
                            st.write(f"• {strength}")

                    with col4:
                        st.markdown("### ⚠️ Weaknesses")

                        for weakness in item["weaknesses"]:
                            st.write(f"• {weakness}")

                    st.markdown("### 💡 Suggestions")

                    for suggestion in item["suggestions"]:
                        st.write(f"• {suggestion}")

                    st.markdown("### 📝 Overall Summary")
                    st.write(item["summary"])

            # 7. Download results as CSV
            st.divider()

            st.subheader("6. Download Results")

            output = io.StringIO()

            fieldnames = [
                "Rank",
                "Resume",
                "Match Score",
                "Matched Skills",
                "Missing Skills",
                "Strengths",
                "Weaknesses",
                "Suggestions",
                "Summary"
            ]

            writer = csv.DictWriter(
                output,
                fieldnames=fieldnames
            )

            writer.writeheader()

            for rank, item in enumerate(top_candidates, start=1):

                writer.writerow({
                    "Rank": rank,
                    "Resume": item["filename"],
                    "Match Score": item["match_score"],
                    "Matched Skills": ", ".join(item["matched_skills"]),
                    "Missing Skills": ", ".join(item["missing_skills"]),
                    "Strengths": ", ".join(item["strengths"]),
                    "Weaknesses": ", ".join(item["weaknesses"]),
                    "Suggestions": ", ".join(item["suggestions"]),
                    "Summary": item["summary"]
                })

            st.download_button(
                label="📥 Download Top Candidates (CSV)",
                data=output.getvalue().encode("utf-8-sig"),
                file_name="resume_evaluation_results.csv",
                mime="text/csv"
            )

        # 8. Show failed files
        if errors:

            st.divider()
            st.subheader("Files That Could Not Be Evaluated")

            for error in errors:
                st.error(
                    f"{error['filename']}: {error['error']}"
                )
