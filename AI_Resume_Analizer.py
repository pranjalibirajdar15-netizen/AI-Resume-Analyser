import os
import re
from collections import Counter
from PyPDF2 import PdfReader
from docx import Document


# ============================================================
# AI RESUME ANALYZER
# Python Only Project
# ============================================================


# ------------------------------------------------------------
# 1. SKILLS DATABASE
# ------------------------------------------------------------

SKILLS_DATABASE = {

    "Programming Languages": [
        "python",
        "java",
        "c",
        "c++",
        "javascript",
        "typescript"
    ],

    "Web Development": [
        "html",
        "html5",
        "css",
        "css3",
        "javascript",
        "react",
        "react.js",
        "angular",
        "bootstrap",
        "node.js",
        "node",
        "django",
        "flask"
    ],

    "Database": [
        "sql",
        "mysql",
        "oracle",
        "postgresql",
        "mongodb",
        "sqlite"
    ],

    "Data Analytics": [
        "pandas",
        "numpy",
        "matplotlib",
        "seaborn",
        "power bi",
        "excel",
        "statistics",
        "data analysis",
        "data visualization"
    ],

    "Tools": [
        "git",
        "github",
        "vs code",
        "visual studio code",
        "jupyter",
        "google colab"
    ],

    "Other": [
        "machine learning",
        "artificial intelligence",
        "api",
        "rest api",
        "oops",
        "object oriented programming",
        "iot",
        "embedded systems"
    ]
}


# ------------------------------------------------------------
# 2. JOB ROLES
# ------------------------------------------------------------

JOB_ROLES = {

    "Python Developer": [
        "python",
        "oops",
        "sql",
        "git",
        "github",
        "django",
        "flask"
    ],

    "Data Analyst": [
        "python",
        "sql",
        "pandas",
        "numpy",
        "excel",
        "power bi",
        "statistics",
        "data visualization"
    ],

    "Frontend Developer": [
        "html",
        "css",
        "javascript",
        "react",
        "bootstrap",
        "git",
        "github"
    ],

    "Full Stack Developer": [
        "python",
        "html",
        "css",
        "javascript",
        "sql",
        "django",
        "react",
        "git"
    ],

    "Software Developer": [
        "python",
        "java",
        "sql",
        "oops",
        "git",
        "github"
    ]
}


# ------------------------------------------------------------
# 3. READ PDF
# ------------------------------------------------------------

def extract_pdf_text(file_path):

    text = ""

    try:

        reader = PdfReader(file_path)

        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    except Exception as e:

        print("Error reading PDF:", e)

    return text


# ------------------------------------------------------------
# 4. READ DOCX
# ------------------------------------------------------------

def extract_docx_text(file_path):

    text = ""

    try:

        document = Document(file_path)

        for paragraph in document.paragraphs:

            text += paragraph.text + "\n"

    except Exception as e:

        print("Error reading DOCX:", e)

    return text


# ------------------------------------------------------------
# 5. READ RESUME
# ------------------------------------------------------------

def extract_resume_text(file_path):

    extension = os.path.splitext(file_path)[1].lower()

    if extension == ".pdf":

        return extract_pdf_text(file_path)

    elif extension == ".docx":

        return extract_docx_text(file_path)

    else:

        print("Only PDF and DOCX files are supported.")

        return ""


# ------------------------------------------------------------
# 6. CLEAN TEXT
# ------------------------------------------------------------

def clean_text(text):

    text = text.lower()

    text = re.sub(r"\s+", " ", text)

    return text


# ------------------------------------------------------------
# 7. FIND SKILLS
# ------------------------------------------------------------

def find_skills(resume_text):

    resume_text = clean_text(resume_text)

    found_skills = []

    for category, skills in SKILLS_DATABASE.items():

        for skill in skills:

            skill_lower = skill.lower()

            if skill_lower in resume_text:

                if skill not in found_skills:

                    found_skills.append(skill)

    return found_skills


# ------------------------------------------------------------
# 8. GROUP SKILLS BY CATEGORY
# ------------------------------------------------------------

def group_skills(found_skills):

    result = {}

    for category, skills in SKILLS_DATABASE.items():

        category_skills = []

        for skill in skills:

            if skill in found_skills:

                category_skills.append(skill)

        if category_skills:

            result[category] = category_skills

    return result


# ------------------------------------------------------------
# 9. FIND EMAIL
# ------------------------------------------------------------

def find_email(text):

    pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"

    result = re.findall(pattern, text)

    if result:

        return result[0]

    return "Not Found"


# ------------------------------------------------------------
# 10. FIND PHONE NUMBER
# ------------------------------------------------------------

def find_phone(text):

    pattern = r"(?:\+91[\s-]?)?[6-9]\d{9}"

    result = re.findall(pattern, text)

    if result:

        return result[0]

    return "Not Found"


# ------------------------------------------------------------
# 11. FIND NAME
# ------------------------------------------------------------

def find_name(text):

    lines = text.strip().split("\n")

    for line in lines:

        line = line.strip()

        if line and len(line.split()) <= 4:

            if not any(char.isdigit() for char in line):

                if "@" not in line:

                    return line

    return "Not Found"


# ------------------------------------------------------------
# 12. FIND EDUCATION
# ------------------------------------------------------------

def analyze_education(text):

    text_lower = text.lower()

    education = []

    keywords = {

        "B.Tech": [
            "b.tech",
            "btech",
            "bachelor of technology"
        ],

        "B.E": [
            "b.e",
            "bachelor of engineering"
        ],

        "M.Tech": [
            "m.tech",
            "mtech",
            "master of technology"
        ],

        "M.E": [
            "m.e",
            "master of engineering"
        ],

        "B.Sc": [
            "b.sc",
            "bsc",
            "bachelor of science"
        ],

        "M.Sc": [
            "m.sc",
            "msc",
            "master of science"
        ],

        "MBA": [
            "mba",
            "master of business administration"
        ],

        "Diploma": [
            "diploma"
        ],

        "HSC": [
            "hsc",
            "12th",
            "higher secondary"
        ],

        "SSC": [
            "ssc",
            "10th",
            "secondary school"
        ]
    }

    for degree, words in keywords.items():

        for word in words:

            if word in text_lower:

                if degree not in education:

                    education.append(degree)

    return education


# ------------------------------------------------------------
# 13. FIND EXPERIENCE
# ------------------------------------------------------------

def analyze_experience(text):

    text_lower = text.lower()

    experience_keywords = [
        "experience",
        "internship",
        "intern",
        "work experience",
        "professional experience",
        "fresher"
    ]

    found = []

    for keyword in experience_keywords:

        if keyword in text_lower:

            found.append(keyword)

    return found


# ------------------------------------------------------------
# 14. FIND PROJECTS
# ------------------------------------------------------------

def analyze_projects(text):

    text_lower = text.lower()

    project_keywords = [
        "project",
        "projects",
        "ai resume analyzer",
        "library management system",
        "amazon clone",
        "netflix clone",
        "spotify clone",
        "sales dashboard",
        "student data analysis"
    ]

    found = []

    for project in project_keywords:

        if project in text_lower:

            found.append(project)

    return found


# ------------------------------------------------------------
# 15. JOB MATCHING
# ------------------------------------------------------------

def calculate_job_match(found_skills, required_skills):

    found = set(skill.lower() for skill in found_skills)

    required = set(skill.lower() for skill in required_skills)

    matched = found.intersection(required)

    missing = required - found

    if len(required) == 0:

        score = 0

    else:

        score = (len(matched) / len(required)) * 100

    return score, list(matched), list(missing)


# ------------------------------------------------------------
# 16. SKILL FREQUENCY
# ------------------------------------------------------------

def skill_frequency(text, found_skills):

    text = clean_text(text)

    frequency = {}

    for skill in found_skills:

        count = text.count(skill.lower())

        frequency[skill] = count

    return frequency


# ------------------------------------------------------------
# 17. RESUME STATISTICS
# ------------------------------------------------------------

def resume_statistics(text):

    words = text.split()

    characters = len(text)

    sentences = len(re.findall(r"[.!?]", text))

    return {
        "Words": len(words),
        "Characters": characters,
        "Sentences": sentences
    }


# ------------------------------------------------------------
# 18. RESUME QUALITY CHECK
# ------------------------------------------------------------

def quality_check(text, found_skills, education, projects):

    suggestions = []

    text_lower = text.lower()

    if len(text.split()) < 100:

        suggestions.append(
            "Resume contains very little content."
        )

    if "summary" not in text_lower and \
       "objective" not in text_lower:

        suggestions.append(
            "Add a professional summary or career objective."
        )

    if not education:

        suggestions.append(
            "Add your education details."
        )

    if not projects:

        suggestions.append(
            "Add relevant projects."
        )

    if len(found_skills) < 5:

        suggestions.append(
            "Add more relevant technical skills."
        )

    if "experience" not in text_lower and \
       "internship" not in text_lower:

        suggestions.append(
            "Add internship or experience details if applicable."
        )

    if not suggestions:

        suggestions.append(
            "Resume contains the major sections detected by the analyzer."
        )

    return suggestions


# ------------------------------------------------------------
# 19. ATS SCORE
# ------------------------------------------------------------

def calculate_ats_score(
        skill_score,
        education,
        projects,
        experience,
        resume_text):

    score = 0

    # Skills = 50 marks
    score += skill_score * 0.50

    # Education = 15 marks
    if education:

        score += 15

    # Projects = 15 marks
    if projects:

        score += 15

    # Experience = 10 marks
    if experience:

        score += 10

    # Resume length/content = 10 marks
    word_count = len(resume_text.split())

    if word_count >= 300:

        score += 10

    elif word_count >= 150:

        score += 7

    elif word_count >= 100:

        score += 5

    return min(score, 100)


# ------------------------------------------------------------
# 20. DISPLAY HEADER
# ------------------------------------------------------------

def print_header():

    print("\n")
    print("=" * 70)
    print("                 AI RESUME ANALYZER")
    print("=" * 70)


# ------------------------------------------------------------
# 21. DISPLAY SKILLS
# ------------------------------------------------------------

def display_skills(found_skills):

    print("\n" + "-" * 70)

    print("SKILLS DETECTED")

    print("-" * 70)

    if not found_skills:

        print("No technical skills detected.")

        return

    grouped = group_skills(found_skills)

    for category, skills in grouped.items():

        print(f"\n{category}:")

        for skill in skills:

            print("  ✓", skill)


# ------------------------------------------------------------
# 22. DISPLAY JOB MATCH
# ------------------------------------------------------------

def display_job_match(found_skills):

    print("\n" + "-" * 70)

    print("JOB ROLE MATCHING")

    print("-" * 70)

    for role, required_skills in JOB_ROLES.items():

        score, matched, missing = calculate_job_match(
            found_skills,
            required_skills
        )

        print(f"\n{role}")

        print(f"Match Score: {score:.2f}%")

        print("Matched Skills:")

        if matched:

            print("  ", ", ".join(matched))

        else:

            print("   None")

        print("Missing Skills:")

        if missing:

            print("  ", ", ".join(missing))

        else:

            print("   None")


# ------------------------------------------------------------
# 23. DISPLAY CONTACT INFORMATION
# ------------------------------------------------------------

def display_contact_information(text):

    print("\n" + "-" * 70)

    print("PERSONAL INFORMATION")

    print("-" * 70)

    name = find_name(text)

    email = find_email(text)

    phone = find_phone(text)

    print("Name  :", name)

    print("Email :", email)

    print("Phone :", phone)


# ------------------------------------------------------------
# 24. DISPLAY EDUCATION
# ------------------------------------------------------------

def display_education(education):

    print("\n" + "-" * 70)

    print("EDUCATION")

    print("-" * 70)

    if education:

        for item in education:

            print("✓", item)

    else:

        print("Education details not detected.")


# ------------------------------------------------------------
# 25. DISPLAY EXPERIENCE
# ------------------------------------------------------------

def display_experience(experience):

    print("\n" + "-" * 70)

    print("EXPERIENCE / INTERNSHIP")

    print("-" * 70)

    if experience:

        for item in experience:

            print("✓", item)

    else:

        print("Experience details not detected.")


# ------------------------------------------------------------
# 26. DISPLAY PROJECTS
# ------------------------------------------------------------

def display_projects(projects):

    print("\n" + "-" * 70)

    print("PROJECTS")

    print("-" * 70)

    if projects:

        for item in projects:

            print("✓", item)

    else:

        print("Projects not detected.")


# ------------------------------------------------------------
# 27. DISPLAY STATISTICS
# ------------------------------------------------------------

def display_statistics(text):

    stats = resume_statistics(text)

    print("\n" + "-" * 70)

    print("RESUME STATISTICS")

    print("-" * 70)

    print("Words      :", stats["Words"])

    print("Characters :", stats["Characters"])

    print("Sentences  :", stats["Sentences"])


# ------------------------------------------------------------
# 28. DISPLAY SKILL FREQUENCY
# ------------------------------------------------------------

def display_skill_frequency(text, found_skills):

    frequency = skill_frequency(
        text,
        found_skills
    )

    print("\n" + "-" * 70)

    print("SKILL FREQUENCY")

    print("-" * 70)

    sorted_frequency = sorted(
        frequency.items(),
        key=lambda x: x[1],
        reverse=True
    )

    for skill, count in sorted_frequency:

        print(f"{skill:25} : {count}")


# ------------------------------------------------------------
# 29. DISPLAY ATS SCORE
# ------------------------------------------------------------

def display_ats_score(
        skill_score,
        education,
        projects,
        experience,
        text):

    ats_score = calculate_ats_score(
        skill_score,
        education,
        projects,
        experience,
        text
    )

    print("\n" + "=" * 70)

    print("                 ATS RESUME SCORE")

    print("=" * 70)

    print(f"\nATS Score: {ats_score:.2f}%")

    if ats_score >= 80:

        print("Resume contains strong matching content.")

    elif ats_score >= 60:

        print("Resume has moderate matching content.")

    elif ats_score >= 40:

        print("Resume needs improvement for the selected job.")

    else:

        print("Resume needs significant improvement.")


# ------------------------------------------------------------
# 30. DISPLAY SUGGESTIONS
# ------------------------------------------------------------

def display_suggestions(
        text,
        found_skills,
        education,
        projects):

    experience = analyze_experience(text)

    suggestions = quality_check(
        text,
        found_skills,
        education,
        projects
    )

    print("\n" + "-" * 70)

    print("RESUME IMPROVEMENT SUGGESTIONS")

    print("-" * 70)

    for suggestion in suggestions:

        print("•", suggestion)


# ------------------------------------------------------------
# 31. GENERATE REPORT
# ------------------------------------------------------------

def generate_report(
        text,
        found_skills,
        education,
        experience,
        projects):

    report_folder = "reports"

    if not os.path.exists(report_folder):

        os.makedirs(report_folder)

    report_path = os.path.join(
        report_folder,
        "resume_analysis_report.txt"
    )

    with open(
        report_path,
        "w",
        encoding="utf-8"
    ) as file:

        file.write("=" * 70 + "\n")

        file.write(
            "                 AI RESUME ANALYZER REPORT\n"
        )

        file.write("=" * 70 + "\n\n")

        # Personal Information
        file.write("PERSONAL INFORMATION\n")
        file.write("-" * 70 + "\n")

        file.write(
            f"Name: {find_name(text)}\n"
        )

        file.write(
            f"Email: {find_email(text)}\n"
        )

        file.write(
            f"Phone: {find_phone(text)}\n\n"
        )

        # Skills
        file.write("SKILLS\n")
        file.write("-" * 70 + "\n")

        for skill in found_skills:

            file.write(f"- {skill}\n")

        file.write("\n")

        # Education
        file.write("EDUCATION\n")
        file.write("-" * 70 + "\n")

        for item in education:

            file.write(f"- {item}\n")

        file.write("\n")

        # Experience
        file.write("EXPERIENCE\n")
        file.write("-" * 70 + "\n")

        for item in experience:

            file.write(f"- {item}\n")

        file.write("\n")

        # Projects
        file.write("PROJECTS\n")
        file.write("-" * 70 + "\n")

        for item in projects:

            file.write(f"- {item}\n")

        file.write("\n")

        # Job matching
        file.write("JOB ROLE MATCHING\n")
        file.write("-" * 70 + "\n")

        for role, required_skills in JOB_ROLES.items():

            score, matched, missing = calculate_job_match(
                found_skills,
                required_skills
            )

            file.write(
                f"\n{role}: {score:.2f}%\n"
            )

            file.write(
                "Matched: " +
                ", ".join(matched) +
                "\n"
            )

            file.write(
                "Missing: " +
                ", ".join(missing) +
                "\n"
            )

        # Statistics
        stats = resume_statistics(text)

        file.write("\n")

        file.write("RESUME STATISTICS\n")
        file.write("-" * 70 + "\n")

        file.write(
            f"Words: {stats['Words']}\n"
        )

        file.write(
            f"Characters: {stats['Characters']}\n"
        )

        file.write(
            f"Sentences: {stats['Sentences']}\n"
        )

    return report_path


# ------------------------------------------------------------
# 32. SELECT RESUME
# ------------------------------------------------------------

def select_resume():

    print("\nAvailable resume files:")

    folder = "resumes"

    if not os.path.exists(folder):

        os.makedirs(folder)

    files = os.listdir(folder)

    resume_files = []

    for file in files:

        if file.lower().endswith(
            (".pdf", ".docx")
        ):

            resume_files.append(file)

    if not resume_files:

        print("\nNo resume found.")

        print(
            "Please put your PDF or DOCX resume inside:"
        )

        print("resumes/")

        return None

    for index, file in enumerate(
        resume_files,
        start=1
    ):

        print(
            f"{index}. {file}"
        )

    while True:

        try:

            choice = int(
                input("\nSelect resume number: ")
            )

            if 1 <= choice <= len(resume_files):

                selected_file = resume_files[
                    choice - 1
                ]

                return os.path.join(
                    folder,
                    selected_file
                )

            else:

                print("Invalid choice.")

        except ValueError:

            print("Please enter a number.")


# ------------------------------------------------------------
# 33. MAIN PROGRAM
# ------------------------------------------------------------

def main():

    print_header()

    print("\n1. Analyze Resume")
    print("2. Exit")

    choice = input(
        "\nEnter your choice: "
    )

    if choice == "2":

        print("\nThank you!")

        return

    if choice != "1":

        print("\nInvalid choice.")

        return

    resume_path = select_resume()

    if resume_path is None:

        return

    print("\nReading resume...")

    resume_text = extract_resume_text(
        resume_path
    )

    if not resume_text.strip():

        print(
            "\nCould not extract text from resume."
        )

        return

    print(
        "\nResume successfully analyzed."
    )

    # Detect information
    found_skills = find_skills(
        resume_text
    )

    education = analyze_education(
        resume_text
    )

    experience = analyze_experience(
        resume_text
    )

    projects = analyze_projects(
        resume_text
    )

    # Display results
    display_contact_information(
        resume_text
    )

    display_skills(
        found_skills
    )

    display_education(
        education
    )

    display_experience(
        experience
    )

    display_projects(
        projects
    )

    display_statistics(
        resume_text
    )

    display_skill_frequency(
        resume_text,
        found_skills
    )

    display_job_match(
        found_skills
    )

    # Data Analyst ATS score
    data_analyst_skills = JOB_ROLES[
        "Data Analyst"
    ]

    data_score, matched, missing = calculate_job_match(
        found_skills,
        data_analyst_skills
    )

    display_ats_score(
        data_score,
        education,
        projects,
        experience,
        resume_text
    )

    display_suggestions(
        resume_text,
        found_skills,
        education,
        projects
    )

    # Generate report
    report_path = generate_report(
        resume_text,
        found_skills,
        education,
        experience,
        projects
    )

    print("\n" + "=" * 70)

    print(
        "Analysis completed successfully!"
    )

    print(
        f"\nReport saved at: {report_path}"
    )

    print("=" * 70)


# ------------------------------------------------------------
# 34. RUN PROGRAM
# ------------------------------------------------------------

if __name__ == "__main__":

    main()