from flask import Flask, render_template, request, redirect, url_for
from database import init_db, save_submission

app = Flask(__name__)

# ── Scoring Engine ────────────────────────────────────────────────────────────
CAREER_RULES = {
    "Backend Developer": {
        "keywords": {
            "python": 40, "django": 35, "flask": 35, "node": 30, "java": 30,
            "go": 30, "ruby": 25, "php": 20, "api": 20, "backend": 50,
            "server": 20, "rest": 20, "microservices": 25, "sql": 15,
        },
        "reason": "Your backend skills translate directly into building robust server-side systems and APIs.",
        "roadmap": [
            ("Master a backend framework", "Django, FastAPI, or Express"),
            ("Learn databases deeply", "PostgreSQL, Redis, MongoDB"),
            ("Study system design", "Scalability, caching, queues"),
            ("Build REST / GraphQL APIs", "Deploy to AWS or GCP"),
        ]
    },
    "Frontend Developer": {
        "keywords": {
            "html": 50, "css": 50, "javascript": 50, "js": 50, "react": 45,
            "vue": 45, "angular": 40, "typescript": 35, "frontend": 50,
            "web design": 40, "ui": 30, "sass": 25, "tailwind": 30,
        },
        "reason": "Your UI and web skills are the foundation of great user experiences on the web.",
        "roadmap": [
            ("Deepen HTML/CSS/JS", "Master the fundamentals"),
            ("Learn React or Vue", "Component-based architecture"),
            ("Add TypeScript", "Type safety at scale"),
            ("Deploy projects", "Vercel, Netlify, GitHub Pages"),
        ]
    },
    "AI / ML Engineer": {
        "keywords": {
            "ai": 50, "machine learning": 50, "ml": 50, "deep learning": 50,
            "nlp": 45, "data science": 45, "tensorflow": 40, "pytorch": 40,
            "neural": 40, "python": 20, "statistics": 30, "math": 20,
            "llm": 45, "computer vision": 40, "kaggle": 30,
        },
        "reason": "Your passion for AI positions you perfectly for one of the fastest-growing tech fields.",
        "roadmap": [
            ("Solidify Python & math", "NumPy, Pandas, linear algebra"),
            ("Learn ML fundamentals", "scikit-learn, regression, classification"),
            ("Deep learning frameworks", "PyTorch or TensorFlow"),
            ("Build & publish models", "Hugging Face, Kaggle competitions"),
        ]
    },
    "UX / UI Designer": {
        "keywords": {
            "design": 50, "figma": 50, "ux": 50, "ui": 50, "sketch": 45,
            "adobe": 40, "photoshop": 35, "illustrator": 35, "prototyping": 40,
            "user research": 40, "wireframe": 40, "creative": 25, "visual": 25,
        },
        "reason": "Your design instincts are invaluable for crafting products people love to use.",
        "roadmap": [
            ("Master Figma", "Components, auto-layout, prototypes"),
            ("Study UX principles", "Nielsen heuristics, accessibility"),
            ("Build a portfolio", "3–5 case studies with process"),
            ("Learn basic HTML/CSS", "Bridge the design-dev gap"),
        ]
    },
    "Data Analyst": {
        "keywords": {
            "sql": 50, "data": 40, "analytics": 50, "excel": 40, "tableau": 45,
            "power bi": 45, "statistics": 40, "python": 20, "r": 30,
            "database": 30, "visualization": 35, "reporting": 30, "bi": 30,
        },
        "reason": "Your analytical mindset and data skills drive smarter business decisions.",
        "roadmap": [
            ("Master SQL", "Complex queries, window functions"),
            ("Learn Python for data", "Pandas, Matplotlib, Seaborn"),
            ("Pick a BI tool", "Tableau or Power BI"),
            ("Build dashboards", "Tell stories with data"),
        ]
    },
    "DevOps / Cloud Engineer": {
        "keywords": {
            "devops": 50, "docker": 45, "kubernetes": 45, "aws": 45, "gcp": 40,
            "azure": 40, "linux": 40, "cloud": 45, "ci": 35, "cd": 35,
            "terraform": 40, "ansible": 35, "network": 30, "security": 30,
            "bash": 30, "infrastructure": 40,
        },
        "reason": "Infrastructure and automation skills are mission-critical for every modern software team.",
        "roadmap": [
            ("Learn Linux & bash", "Shell scripting, permissions, processes"),
            ("Containerise everything", "Docker, then Kubernetes"),
            ("Cloud certification", "AWS Solutions Architect or GCP ACE"),
            ("Implement CI/CD", "GitHub Actions, ArgoCD"),
        ]
    },
    "Mobile App Developer": {
        "keywords": {
            "mobile": 50, "android": 50, "ios": 50, "swift": 50, "kotlin": 50,
            "flutter": 45, "react native": 45, "dart": 40, "xcode": 35,
            "app": 25, "app development": 45,
        },
        "reason": "Mobile dev skills let you build apps used daily by billions of people worldwide.",
        "roadmap": [
            ("Choose your stack", "Flutter (cross-platform) or native Swift/Kotlin"),
            ("Learn the platform", "Navigation, state, storage"),
            ("Publish an app", "App Store or Google Play"),
            ("Study mobile UX patterns", "Material Design, HIG"),
        ]
    },
    "Cybersecurity Analyst": {
        "keywords": {
            "security": 50, "cyber": 50, "hacking": 40, "pentesting": 50,
            "ctf": 45, "linux": 30, "network": 35, "vulnerability": 45,
            "encryption": 40, "firewall": 35, "soc": 45, "threat": 40,
        },
        "reason": "Security skills are in massive demand as organisations race to protect their data.",
        "roadmap": [
            ("Learn networking basics", "TCP/IP, DNS, firewalls"),
            ("Earn CompTIA Security+", "Widely recognised entry cert"),
            ("Practice on platforms", "TryHackMe, HackTheBox, CTFs"),
            ("Specialise", "Penetration testing, SOC, cloud security"),
        ]
    },
}

DEFAULT_FALLBACK = [
    {
        "title": "Software Developer",
        "score": 60,
        "reason": "A broad technical foundation opens doors across every engineering discipline.",
        "roadmap": [
            ("Pick one language", "Python or JavaScript are great starts"),
            ("Build small projects", "A todo app, then something you care about"),
            ("Learn Git", "Version control is non-negotiable"),
            ("Study CS basics", "Algorithms, data structures, system design"),
        ]
    },
    {
        "title": "Technology Consultant",
        "score": 50,
        "reason": "General tech interest suits advisory roles bridging business and technology.",
        "roadmap": [
            ("Develop business acumen", "Understand how companies work"),
            ("Deepen one tech domain", "Become a subject matter expert"),
            ("Communication skills", "Writing, presenting, stakeholder management"),
            ("Get certified", "AWS, Google, or Microsoft cloud certs"),
        ]
    },
]


# ── AI Career Coach Advice ─────────────────────────────────────────────────
# Per-career advice templates. Each entry maps a career title to the
# core technologies/tools relevant to it, plus career-specific phrasing
# for project ideas, tools to practice, portfolio focus, and interview prep.
CAREER_ADVICE_DATA = {
    "Backend Developer": {
        "core_skills": ["python", "django", "flask", "node", "sql", "api", "rest", "microservices"],
        "projects": "Build a REST API with authentication, then a microservices project with two services talking to each other",
        "tools": "Postman, Docker, and a relational database like PostgreSQL",
        "portfolio": "2–3 backend repos with clear READMEs, API docs, and one deployed live demo",
        "interview": "system design basics, database schema design, and common API design questions",
    },
    "Frontend Developer": {
        "core_skills": ["html", "css", "javascript", "js", "react", "vue", "angular", "typescript"],
        "projects": "Build a multi-page responsive site, then a small React/Vue app with state management",
        "tools": "Chrome DevTools, Figma (for handoff), and a component library like shadcn/ui or MUI",
        "portfolio": "A polished personal site plus 2 live demo links showcasing responsive, accessible UI",
        "interview": "JavaScript fundamentals (closures, async/await), CSS layout problems, and component design",
    },
    "AI / ML Engineer": {
        "core_skills": ["ai", "machine learning", "ml", "deep learning", "tensorflow", "pytorch", "python", "nlp"],
        "projects": "Train a classifier on a public dataset, then fine-tune or build a small NLP/CV project end-to-end",
        "tools": "Jupyter, scikit-learn, PyTorch or TensorFlow, and Hugging Face",
        "portfolio": "A GitHub repo with notebooks, model metrics, and a short write-up of your approach",
        "interview": "ML fundamentals (bias-variance, overfitting), model evaluation metrics, and a coding round in Python",
    },
    "UX / UI Designer": {
        "core_skills": ["design", "figma", "ux", "ui", "sketch", "prototyping", "wireframe", "user research"],
        "projects": "Redesign an existing app's flow, then run a small usability test and document the findings",
        "tools": "Figma, Maze or UserTesting, and basic HTML/CSS to bridge design and dev",
        "portfolio": "3–5 case studies showing problem, process, iterations, and final outcome",
        "interview": "whiteboard design challenges, walking through your design process, and design critique questions",
    },
    "Data Analyst": {
        "core_skills": ["sql", "data", "analytics", "excel", "tableau", "power bi", "python", "statistics"],
        "projects": "Clean and analyze a public dataset, then build an interactive dashboard from it",
        "tools": "SQL, Excel/Google Sheets, and Tableau or Power BI",
        "portfolio": "2–3 dashboards or analysis write-ups with clear business takeaways, not just charts",
        "interview": "SQL query challenges, case-study style 'how would you analyze X' questions, and stats basics",
    },
    "DevOps / Cloud Engineer": {
        "core_skills": ["devops", "docker", "kubernetes", "aws", "gcp", "azure", "linux", "ci", "terraform"],
        "projects": "Containerize an app with Docker, then set up a CI/CD pipeline that deploys it automatically",
        "tools": "Docker, GitHub Actions, and one cloud provider (AWS, GCP, or Azure)",
        "portfolio": "A repo showing your pipeline config plus a short README explaining the architecture",
        "interview": "Linux fundamentals, CI/CD concepts, and basic cloud architecture / troubleshooting scenarios",
    },
    "Mobile App Developer": {
        "core_skills": ["mobile", "android", "ios", "swift", "kotlin", "flutter", "react native", "dart"],
        "projects": "Build a small utility app end-to-end, then publish it (or a beta build) to a store",
        "tools": "Flutter or native Xcode/Android Studio, and Firebase for backend basics",
        "portfolio": "1–2 published or beta apps with screenshots, a demo video, and the source on GitHub",
        "interview": "mobile lifecycle questions, state management approaches, and platform-specific UI patterns",
    },
    "Cybersecurity Analyst": {
        "core_skills": ["security", "cyber", "pentesting", "ctf", "network", "vulnerability", "encryption", "soc"],
        "projects": "Complete a few TryHackMe rooms, then write up a vulnerability assessment of a test environment",
        "tools": "Wireshark, Nmap, and a home lab (TryHackMe or HackTheBox)",
        "portfolio": "A write-up blog of CTF solutions or a documented home-lab security assessment",
        "interview": "networking fundamentals, common attack types, and how you'd respond to a sample incident",
    },
    "Software Developer": {
        "core_skills": ["python", "javascript", "git", "programming", "coding"],
        "projects": "Build a todo app, then a slightly bigger project that solves a real problem you have",
        "tools": "Git/GitHub, VS Code, and a debugger you're comfortable with",
        "portfolio": "2–3 small but complete projects with clean commits and README files",
        "interview": "data structures & algorithms basics, and being able to explain your project decisions clearly",
    },
    "Technology Consultant": {
        "core_skills": ["business", "communication", "consulting", "presentation", "strategy"],
        "projects": "Write a short case study analyzing a real company's tech strategy, then present it concisely",
        "tools": "PowerPoint/Slides, and one cloud certification (AWS, Google, or Microsoft)",
        "portfolio": "1–2 case studies or strategy decks demonstrating structured problem-solving",
        "interview": "case-style business problems, structured communication, and a cloud fundamentals cert question",
    },
}


def generate_advice(career: str, user_skills: str) -> dict:
    """
    Generate personalized, career-specific AI Career Coach advice.

    career: the career title (must match a key in CAREER_ADVICE_DATA,
            falls back to the generic "Software Developer" profile otherwise)
    user_skills: the raw skills string the user submitted

    Returns a dict with keys: learn, projects, tools, portfolio, interview
    """
    data = CAREER_ADVICE_DATA.get(career, CAREER_ADVICE_DATA["Software Developer"])
    user_skills_lower = user_skills.lower()

    # Figure out which core skills the user already has vs. is missing
    missing = [s for s in data["core_skills"] if s not in user_skills_lower]
    have = [s for s in data["core_skills"] if s in user_skills_lower]

    if missing:
        # Cap at 4 to keep advice focused and readable
        learn_text = "Focus on: " + ", ".join(missing[:4]).title()
        if have:
            learn_text += f" (you already have a head start with {', '.join(have[:2]).title()})"
    else:
        learn_text = "You already cover the core skills — sharpen them with real-world, production-level projects"

    return {
        "learn": learn_text,
        "projects": data["projects"],
        "tools": data["tools"],
        "portfolio": data["portfolio"],
        "interview": data["interview"],
    }


# ── Skill Gap Analysis ──────────────────────────────────────────────────────
# Required skills per career, written as clean display names. Used to compare
# against what the user already listed and show what's still missing.
REQUIRED_SKILLS = {
    "Backend Developer": ["Python", "SQL", "REST APIs", "Git", "Django/Flask", "Docker"],
    "Frontend Developer": ["HTML", "CSS", "JavaScript", "React", "Git", "TypeScript"],
    "AI / ML Engineer": ["Python", "Statistics", "NumPy/Pandas", "Machine Learning", "PyTorch/TensorFlow", "SQL"],
    "UX / UI Designer": ["Figma", "Wireframing", "User Research", "Prototyping", "HTML/CSS", "Visual Design"],
    "Data Analyst": ["SQL", "Excel", "Python", "Statistics", "Tableau/Power BI", "Data Visualization"],
    "DevOps / Cloud Engineer": ["Linux", "Docker", "Kubernetes", "CI/CD", "Cloud (AWS/GCP/Azure)", "Terraform"],
    "Mobile App Developer": ["Git", "Flutter/React Native", "Swift/Kotlin", "REST APIs", "UI Design", "App Deployment"],
    "Cybersecurity Analyst": ["Networking", "Linux", "Security Fundamentals", "Encryption", "Vulnerability Assessment", "Incident Response"],
    "Software Developer": ["Python", "JavaScript", "Git", "Data Structures", "Problem Solving", "SQL"],
    "Technology Consultant": ["Communication", "Business Analysis", "Presentation Skills", "Cloud Fundamentals", "Project Management", "Strategy"],
}


def generate_skill_gap(career: str, user_skills: str) -> dict:
    """
    Compare a user's listed skills against a career's required skills.

    career: the career title (must match a key in REQUIRED_SKILLS,
            falls back to the generic "Software Developer" list otherwise)
    user_skills: the raw skills string the user submitted

    Returns a dict: { "current_skills": [...], "missing_skills": [...] }
    """
    required = REQUIRED_SKILLS.get(career, REQUIRED_SKILLS["Software Developer"])
    user_skills_lower = user_skills.lower()

    current_skills = []
    missing_skills = []

    for skill in required:
        # A required skill may have alternates separated by "/" (e.g. "Django/Flask").
        # It counts as "current" if ANY alternate appears in the user's input.
        alternates = [alt.strip().lower() for alt in skill.split("/")]
        if any(alt in user_skills_lower for alt in alternates):
            current_skills.append(skill)
        else:
            missing_skills.append(skill)

    return {
        "current_skills": current_skills,
        "missing_skills": missing_skills,
    }


def score_careers(skills: str, interests: str) -> list:
    combined = (skills + " " + interests).lower()
    scores: dict[str, int] = {}

    for career, data in CAREER_RULES.items():
        total = 0
        for keyword, points in data["keywords"].items():
            if keyword in combined:
                total += points
        if total > 0:
            scores[career] = total

    if not scores:
        fallback = []
        for item in DEFAULT_FALLBACK[:3]:
            item_copy = dict(item)
            item_copy["advice"] = generate_advice(item["title"], skills)
            item_copy["skill_gap"] = generate_skill_gap(item["title"], skills)
            fallback.append(item_copy)
        return fallback

    # Normalise to percentage (cap at 99)
    max_score = max(scores.values())
    results = []
    for career, raw in sorted(scores.items(), key=lambda x: x[1], reverse=True):
        pct = min(99, round((raw / max_score) * 95))
        results.append({
            "title": career,
            "score": pct,
            "reason": CAREER_RULES[career]["reason"],
            "roadmap": CAREER_RULES[career]["roadmap"],
            "advice": generate_advice(career, skills),
            "skill_gap": generate_skill_gap(career, skills),
        })

    return results[:3]


# ── Routes ────────────────────────────────────────────────────────────────────
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():
    name = request.form.get("name", "").strip()
    skills = request.form.get("skills", "").strip()
    interests = request.form.get("interests", "").strip()

    if not name or not skills or not interests:
        return redirect(url_for("home"))

    results = score_careers(skills, interests)

    # Persist to database
    save_submission(name, skills, interests, results)

    return render_template(
        "results.html",
        name=name,
        skills=skills,
        interests=interests,
        results=results,
    )


if __name__ == "__main__":
    app.run(debug=True)
