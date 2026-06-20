# CareerCompassAI 🧭

An AI-powered career guidance web app that analyzes your skills and suggests the best tech career path for you — along with a personalized roadmap to get there.

## 🌐 Live Demo
[https://career-ai-1-jkpo.onrender.com](https://career-ai-1-jkpo.onrender.com)

## ✨ Features
- Enter your skills and background in plain text
- Instantly get matched to a tech career (Backend Dev, Frontend Dev, Data Scientist, and more)
- See a step-by-step roadmap tailored to your match
- Clean dark mode UI

## 🛠️ Built With
- **Python** + **Flask** — backend framework
- **SQLite** — stores user submissions
- **HTML/CSS/JS** — frontend with dark mode design
- **Deployed on** [Render](https://render.com)

## 🚀 Running Locally
1. Clone the repo
   ```bash
   git clone https://github.com/Sara-Elena-Saji/Career-AI
   cd Career-AI
   ```
2. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app
   ```bash
   python app.py
   ```
4. Open [http://localhost:5000](http://localhost:5000)

## 📁 Project Structure
```
├── app.py            # Main Flask app & career scoring engine
├── database.py       # DB helper functions
├── schema.sql        # Database schema
├── requirements.txt  # Python dependencies
├── render.yaml       # Render deployment config
├── static/
│   ├── style.css     # Dark mode styles
│   └── script.js     # Frontend logic
└── templates/
    ├── index.html    # Home page
    └── results.html  # Results page
```
