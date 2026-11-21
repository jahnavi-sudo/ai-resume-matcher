from flask import Flask, render_template, request, jsonify
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

app = Flask(__name__)

COMMON_SKILLS = [
    "python", "java", "c++", "c", "html", "css", "javascript", "react", "node",
    "sql", "mysql", "mongodb", "git", "github", "machine learning", "deep learning",
    "nlp", "pandas", "numpy", "scikit-learn", "tensorflow", "pytorch", "flask",
    "django", "data analysis", "excel", "power bi", "tableau", "linux", "aws",
    "api", "rest", "communication", "problem solving", "teamwork", "leadership"
]

def extract_skills(text):
    text_lower = text.lower()
    found = set()
    for skill in COMMON_SKILLS:
        if re.search(r'\b' + re.escape(skill) + r'\b', text_lower):
            found.add(skill)
    return found

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    resume_text = data.get("resume", "").strip()
    jd_text = data.get("jd", "").strip()

    if not resume_text or not jd_text:
        return jsonify({"error": "Please paste both your resume and job description."}), 400

    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform([resume_text, jd_text])
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    match_score = round(float(similarity) * 100, 1)

    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(jd_text)
    matched_skills = sorted(list(resume_skills.intersection(jd_skills)))
    missing_skills = sorted(list(jd_skills - resume_skills))

    return jsonify({
        "score": match_score,
        "matched": matched_skills,
        "missing": missing_skills
    })

if __name__ == "__main__":
    print("Starting AI Resume Matcher Server...")
    app.run(debug=True, port=5000)