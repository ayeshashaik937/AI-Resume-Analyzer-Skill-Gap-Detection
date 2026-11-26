from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
import time
import pymupdf

from dotenv import load_dotenv
from google import genai
from google.genai import types

from skills import extract_skills


# ==========================================
# LOAD ENVIRONMENT VARIABLES
# ==========================================

load_dotenv()

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {"pdf"}


# ==========================================
# GEMINI AI SETUP
# ==========================================

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("WARNING: GEMINI_API_KEY was not found in .env")
    client = None
else:
    print("Gemini API key loaded successfully.")
    client = genai.Client(api_key=api_key)


# ==========================================
# GEMINI MODELS
# ==========================================

# The application will try these models one by one.
# If one is temporarily unavailable, it tries the next one.

GEMINI_MODELS = [
    "gemini-3.8-flash",
    "gemini-3.6-flash",
    "gemini-3.5-flash-lite"
]


# ==========================================
# CHECK FILE TYPE
# ==========================================

def allowed_file(filename):

    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )


# ==========================================
# EXTRACT TEXT FROM PDF
# ==========================================

def extract_text_from_pdf(pdf_path):

    text = ""

    try:

        document = pymupdf.open(pdf_path)

        for page in document:
            text += page.get_text()

        document.close()

    except Exception as e:

        print("PDF ERROR:", repr(e))

        return ""

    return text


# ==========================================
# CALCULATE ATS SCORE
# ==========================================

def calculate_ats_score(resume_skills, job_skills):

    if not job_skills:
        return 0

    high_priority = {
        "python",
        "java",
        "c++",
        "javascript",
        "machine learning",
        "deep learning",
        "artificial intelligence",
        "data science",
        "data analysis",
        "sql",
        "scikit-learn",
        "tensorflow",
        "pytorch",
        "nlp",
        "natural language processing",
        "generative ai",
        "llm",
        "large language models"
    }

    medium_priority = {
        "pandas",
        "numpy",
        "matplotlib",
        "react",
        "node.js",
        "flask",
        "django",
        "mongodb",
        "mysql",
        "git",
        "github",
        "docker",
        "aws",
        "azure",
        "power bi",
        "tableau"
    }

    resume_skills = set(resume_skills)
    job_skills = set(job_skills)

    total_weight = 0
    matched_weight = 0

    for skill in job_skills:

        if skill in high_priority:
            weight = 3

        elif skill in medium_priority:
            weight = 2

        else:
            weight = 1

        total_weight += weight

        if skill in resume_skills:
            matched_weight += weight

    if total_weight == 0:
        return 0

    score = (matched_weight / total_weight) * 100

    return round(score, 2)


# ==========================================
# GEMINI AI ANALYSIS
# ==========================================

def generate_ai_suggestions(
    resume_text,
    job_description,
    resume_skills,
    job_skills,
    matched_skills,
    missing_skills,
    ats_score
):

    if client is None:

        return (
            "Gemini AI is not configured. "
            "Please check your GEMINI_API_KEY in the .env file."
        )


    # ======================================
    # SHORTER PROMPT
    # ======================================

    prompt = f"""
You are an AI career assistant.

Analyze this resume against the job description.

Do not invent skills, education, projects, or experience.

ATS SCORE:
{ats_score}%

RESUME SKILLS:
{", ".join(resume_skills)}

JOB SKILLS:
{", ".join(job_skills)}

MATCHED SKILLS:
{", ".join(matched_skills)}

MISSING SKILLS:
{", ".join(missing_skills)}

RESUME:
{resume_text[:7000]}

JOB DESCRIPTION:
{job_description[:4000]}

Give a concise professional response with exactly these sections:

1. Overall Assessment
Briefly explain the resume-job match.

2. Resume Improvement Suggestions
Give 4 practical suggestions.

3. Skill Gap Recommendations
Explain the most important missing skills to learn.

4. Important Resume Keywords
List useful job-description keywords that the candidate can genuinely use.

5. Suitable Job Roles
Suggest suitable entry-level roles based only on the resume.

Keep the response concise and useful for a student.
"""


    # ======================================
    # TRY MULTIPLE GEMINI MODELS
    # ======================================

    for model_name in GEMINI_MODELS:

        print("--------------------------------")
        print("Trying Gemini model:", model_name)
        print("--------------------------------")


        # Retry each model up to 2 times

        for attempt in range(2):

            try:

                print(
                    f"Gemini attempt {attempt + 1}/2 "
                    f"using {model_name}"
                )


                response = client.models.generate_content(

                    model=model_name,

                    contents=prompt,

                    config=types.GenerateContentConfig(

                        thinking_config=types.ThinkingConfig(
                            thinking_level="low"
                        )

                    )

                )


                print(
                    "Gemini response received from:",
                    model_name
                )


                if response is not None and response.text:

                    return response.text


                print(
                    "Gemini returned an empty response."
                )


            except Exception as e:

                error_text = str(e)

                print(
                    f"GEMINI ERROR "
                    f"({model_name}, attempt {attempt + 1}):",
                    repr(e)
                )


                # If the model is temporarily unavailable,
                # wait and retry.

                if "503" in error_text or "UNAVAILABLE" in error_text:

                    if attempt < 1:

                        print(
                            "Gemini is temporarily busy."
                        )

                        print(
                            "Waiting 3 seconds before retry..."
                        )

                        time.sleep(3)

                        continue

                    else:

                        print(
                            "Model still unavailable."
                        )

                        print(
                            "Moving to next Gemini model..."
                        )

                        break


                # For other errors, move to the next model.

                break


    # ======================================
    # ALL MODELS FAILED
    # ======================================

    return (
        "Gemini AI is temporarily unavailable. "
        "However, the ATS score and skill analysis "
        "were completed successfully. Please try "
        "the AI analysis again later."
    )


# ==========================================
# HOME PAGE
# ==========================================

@app.route("/")
def home():

    return render_template("index.html")


# ==========================================
# ANALYZE RESUME
# ==========================================

@app.route("/analyze", methods=["POST"])
def analyze():

    print("\n================================")
    print("NEW RESUME ANALYSIS REQUEST")
    print("================================")


    # --------------------------------------
    # GET RESUME
    # --------------------------------------

    resume = request.files.get("resume")


    # --------------------------------------
    # GET JOB DESCRIPTION
    # --------------------------------------

    job_description = request.form.get(
        "job_description",
        ""
    )


    # --------------------------------------
    # CHECK RESUME
    # --------------------------------------

    if not resume or resume.filename == "":

        return render_template(
            "index.html",
            error="Please upload a resume PDF."
        )


    # --------------------------------------
    # CHECK FILE TYPE
    # --------------------------------------

    if not allowed_file(resume.filename):

        return render_template(
            "index.html",
            error="Only PDF files are allowed."
        )


    # --------------------------------------
    # CHECK JOB DESCRIPTION
    # --------------------------------------

    if not job_description.strip():

        return render_template(
            "index.html",
            error="Please enter a job description."
        )


    # --------------------------------------
    # CREATE UPLOAD FOLDER
    # --------------------------------------

    os.makedirs(
        UPLOAD_FOLDER,
        exist_ok=True
    )


    # --------------------------------------
    # SAVE RESUME
    # --------------------------------------

    filename = secure_filename(
        resume.filename
    )

    pdf_path = os.path.join(
        UPLOAD_FOLDER,
        filename
    )

    resume.save(pdf_path)

    print("Resume saved:", filename)


    # --------------------------------------
    # EXTRACT RESUME TEXT
    # --------------------------------------

    resume_text = extract_text_from_pdf(
        pdf_path
    )

    print(
        "Resume text length:",
        len(resume_text)
    )


    if not resume_text.strip():

        return render_template(
            "index.html",
            error=(
                "Could not extract text from the PDF. "
                "Please upload a text-based resume PDF."
            )
        )


    # --------------------------------------
    # EXTRACT SKILLS
    # --------------------------------------

    resume_skills = extract_skills(
        resume_text
    )

    job_skills = extract_skills(
        job_description
    )


    print(
        "Resume skills:",
        resume_skills
    )

    print(
        "Job skills:",
        job_skills
    )


    # --------------------------------------
    # MATCHED SKILLS
    # --------------------------------------

    matched_skills = sorted(
        set(resume_skills)
        .intersection(
            set(job_skills)
        )
    )


    # --------------------------------------
    # MISSING SKILLS
    # --------------------------------------

    missing_skills = sorted(
        set(job_skills)
        .difference(
            set(resume_skills)
        )
    )


    # --------------------------------------
    # ATS SCORE
    # --------------------------------------

    ats_score = calculate_ats_score(
        resume_skills,
        job_skills
    )


    print(
        "ATS Score:",
        ats_score
    )

    print(
        "Matched skills:",
        matched_skills
    )

    print(
        "Missing skills:",
        missing_skills
    )


    # --------------------------------------
    # GEMINI AI
    # --------------------------------------

    print(
        "Starting Gemini analysis..."
    )

    ai_suggestions = generate_ai_suggestions(

        resume_text,

        job_description,

        resume_skills,

        job_skills,

        matched_skills,

        missing_skills,

        ats_score
    )


    print(
        "Gemini analysis completed."
    )


    # --------------------------------------
    # SKILL GAP
    # --------------------------------------

    skill_gap = len(
        missing_skills
    )


    # --------------------------------------
    # SHOW RESULTS
    # --------------------------------------

    return render_template(

        "index.html",

        ats_score=ats_score,

        resume_skills=resume_skills,

        job_skills=job_skills,

        matched_skills=matched_skills,

        missing_skills=missing_skills,

        skill_gap=skill_gap,

        ai_suggestions=ai_suggestions

    )


# ==========================================
# RUN APPLICATION
# ==========================================

if __name__ == "__main__":

    app.run(
        debug=True
    )