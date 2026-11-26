import re

# Technical and professional skills
SKILLS = [
    # Programming Languages
    "python", "java", "c", "c++", "c#", "javascript", "typescript",
    "php", "ruby", "go", "rust",

    # Web Development
    "html", "css", "react", "angular", "vue", "node.js", "express",
    "flask", "django", "bootstrap", "tailwind",

    # Databases
    "sql", "mysql", "postgresql", "mongodb", "oracle", "sqlite",
    "redis",

    # Data Science
    "data science", "data analysis", "pandas", "numpy", "matplotlib",
    "seaborn", "scipy", "statistics", "excel",

    # Machine Learning / AI
    "machine learning", "deep learning", "artificial intelligence",
    "ai", "scikit-learn", "tensorflow", "pytorch", "keras",
    "computer vision", "nlp",
    "natural language processing",

    # Generative AI
    "generative ai", "llm", "large language models",
    "prompt engineering", "chatgpt", "transformers",
    "hugging face",

    # Cloud / DevOps
    "aws", "azure", "google cloud", "docker", "kubernetes",
    "linux", "git", "github", "gitlab",

    # Data Visualization
    "power bi", "tableau",

    # Professional Skills
    "communication", "problem solving", "leadership",
    "teamwork", "time management", "critical thinking"
]


def extract_skills(text):
    """
    Extract skills from resume or job description.
    """

    text = text.lower()

    found_skills = []

    for skill in SKILLS:

        # Escape special characters such as + and .
        pattern = r'(?<!\w)' + re.escape(skill.lower()) + r'(?!\w)'

        if re.search(pattern, text):
            found_skills.append(skill)

    return sorted(found_skills)