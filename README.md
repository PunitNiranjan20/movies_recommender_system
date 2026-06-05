# 🎬 Movie Recommender System

A content-based movie recommendation system built using Machine Learning, Python, and Streamlit. The application recommends movies similar to the one selected by the user and displays movie posters using the TMDB API.

## 🚀 Live Demo

**Web App:** https://moviesrecommendersystem-xesa6vpfvbrz2kd9qjvxmv.streamlit.app/

---

## 📌 Features

* Recommend 5 similar movies instantly
* Display movie posters using TMDB API
* Interactive Streamlit user interface
* Content-based filtering using cosine similarity
* Fast and responsive recommendations

---

## 🛠️ Technologies Used

* Python
* Pandas
* NumPy
* Scikit-Learn
* Streamlit
* Pickle
* TMDB API

---

## 📂 Project Structure

```text
Movie-Recommender-System/
│
├── app.py
├── movies.pkl
├── similarity.pkl
├── requirements.txt
├── .gitignore
└── README.md
```

---

## ⚙️ How It Works

1. Movie metadata is processed and cleaned.
2. Features such as genres, keywords, cast, and crew are combined.
3. Text data is vectorized using CountVectorizer.
4. Cosine similarity is calculated between movies.
5. When a user selects a movie, the system recommends the most similar movies.
6. Posters are fetched dynamically from the TMDB API.

---

## 🎥 Dataset

The project uses the TMDB Movies Dataset and metadata for generating recommendations.

---

## 🔑 API Used

TMDB (The Movie Database)

https://www.themoviedb.org/

Movie posters are fetched dynamically using the TMDB API.

---

## 🌟 Future Improvements

* Hybrid recommendation system
* User authentication
* Personalized recommendations
* Movie trailers integration
* Watchlist feature
* Deployment using Docker


