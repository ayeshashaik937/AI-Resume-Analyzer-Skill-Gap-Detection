# AI Resume Analyzer with Skill Gap Detection

A Generative AI-powered web application that analyzes resumes against job descriptions, identifies matching and missing skills, calculates an ATS-style score, and provides personalized improvement suggestions using Google Gemini.

## 📌 About the Project

The AI Resume Analyzer with Skill Gap Detection helps students and freshers understand how well their resumes match specific job requirements. It extracts skills from resumes and job descriptions, identifies skill gaps, calculates a weighted matching score, and uses Generative AI to provide suggestions for improvement.

## ✨ Features

- Resume upload in PDF format
- Resume text extraction using PyMuPDF
- Skill extraction from resumes and job descriptions
- Identification of matched and missing skills
- ATS-style weighted matching score
- Skill gap detection
- AI-generated resume improvement suggestions using Google Gemini
- Simple and user-friendly web interface

## 🔄 Project Workflow

1. Upload a resume in PDF format.
2. Enter the target job description.
3. Extract text from the resume.
4. Identify relevant skills from both inputs.
5. Compare the skills and identify matches.
6. Calculate the ATS-style matching score.
7. Detect missing skills and skill gaps.
8. Generate personalized suggestions using Gemini.
9. Display the analysis results.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Flask | Web application framework |
| PyMuPDF | PDF text extraction |
| Google Gemini API | AI-generated suggestions |
| Google Gen AI SDK | Gemini API integration |
| HTML | Web page structure |
| CSS | User interface styling |
| python-dotenv | Environment variable management |

## 📂 Project Structure

```text
AI-Resume-Analyzer-Skill-Gap-Detection/
│
├── app.py
├── skills.py
├── requirements.txt
├── .gitignore
├── templates/
│   └── index.html
├── static/
│   └── styles.css
└── README.md
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/ayeshashaik937/AI-Resume-Analyzer-Skill-Gap-Detection.git
```

### 2. Navigate to the project directory

```bash
cd AI-Resume-Analyzer-Skill-Gap-Detection
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

**Windows:**

```bash
venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure Gemini API key

Create a `.env` file in the project root directory and add:

```env
GEMINI_API_KEY=your_gemini_api_key
```

Replace `your_gemini_api_key` with your actual Gemini API key.

### 7. Run the application

```bash
python app.py
```

Open the application in your browser:

```text
http://127.0.0.1:5000
```

## 📊 ATS-Style Score

The application calculates an ATS-style matching score using weighted skill matching. Skills are assigned different weights based on their priority, and the score represents the percentage of weighted job skills matched by the resume.

This score is an illustrative project metric and is not an official score from any commercial ATS platform.

## 🤖 Generative AI Integration

Google Gemini is used to generate personalized suggestions based on the resume analysis and identified skill gaps.

The project uses direct prompting with an LLM and does not implement Retrieval-Augmented Generation (RAG).

## 🎯 Project Objective

To help students and freshers understand job requirements, identify missing skills, evaluate resume relevance, and improve their resumes for internship and entry-level job applications.

## 🚀 Future Enhancements

- Semantic skill matching
- Support for additional resume formats
- Resume improvement and rewriting
- Job-role recommendations
- Integration with job platforms
- Enhanced skill extraction techniques

## 👩‍💻 Author

**Shaik Ayesha**  
B.Tech – CSE (Artificial Intelligence & Machine Learning)

## 📜 Disclaimer

This project is developed for educational purposes and career guidance. The ATS-style score is an approximate skill-matching indicator and should not be considered a guarantee of recruitment or selection.
