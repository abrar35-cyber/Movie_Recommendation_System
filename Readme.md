# 🎬 Movie Recommendation System

A full-stack movie recommendation web application built with a modern Next.js frontend and a Python machine learning engine powered by content-based filtering.

---

## 📌 Project Overview

The system recommends movies by analyzing metadata such as genres, keywords, cast, and crew. It computes semantic similarity between titles using vectorization techniques to provide accurate recommendations in real time.

---

## 🛠️ Tech Stack

* **Frontend:** Next.js (React), Tailwind CSS
* **Backend:** Python, Flask / FastAPI
* **Machine Learning:** Scikit-learn (CountVectorizer / TF-IDF, Cosine Similarity)
* **Data Handling:** Pandas, NumPy

---

## 📂 Repository Structure

```text
Movie_Recommendation_System/
├── Backend/               # Python API & recommendation model logic
│   ├── main.py            # Backend API server
│   ├── movies.pkl         # Processed movie metadata
│   └── requirements.txt   # Python dependencies
│
├── frontend/              # Next.js web application
│   ├── app/               # Application routes & layouts
│   ├── components/        # Reusable UI components
│   └── package.json       # Node dependencies
│
├── .gitignore             # Excluded artifacts (caches, heavy files)
└── README.md              # Project documentation

⚙️ Installation & Setup
1. Backend Setup
Bash
cd Backend
python -m venv venv

# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
python main.py
2. Frontend Setup
Bash
cd frontend
npm install
npm run dev
Open http://localhost:3000 in your browser to view the application.

🧠 Recommendation Methodology
Feature Engineering: Combines genre, cast, and overview tags into a unified metadata string.

Vector Space Modeling: Transforms text features into vector representations using Scikit-learn.

Similarity Matrix: Applies Cosine Similarity to compute geometric closeness across movie vectors and returns top ranked recommendations.

📄 License
This project is open-source and available under the MIT License.