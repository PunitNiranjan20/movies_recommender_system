import streamlit as st
import pickle as pkl
import pandas as pd
import requests
import time
import gdown
from pathlib import Path

PLACEHOLDER_POSTER = "https://via.placeholder.com/500x750?text=Poster+Unavailable"
POSTER_FETCH_DELAY_SECONDS = 0.4
SIMILARITY_FILE_URL = "https://drive.google.com/file/d/1C1nxZKKYLgzt6vfl0D7LLMfGvJnl6mU4/view?usp=sharing"
SIMILARITY_FILE_PATH = Path("similarity.pkl")


def similarity_file_is_valid(file_path):
    if not file_path.exists() or file_path.stat().st_size == 0:
        return False

    with file_path.open("rb") as file:
        header = file.read(32).lstrip()

    return not header.startswith(b"<")


def ensure_similarity_file():
    if similarity_file_is_valid(SIMILARITY_FILE_PATH):
        return

    with st.spinner("Downloading similarity file. This happens only once on first run..."):
        if SIMILARITY_FILE_PATH.exists():
            SIMILARITY_FILE_PATH.unlink()
        gdown.download(
            SIMILARITY_FILE_URL,
            str(SIMILARITY_FILE_PATH),
            quiet=False,
            fuzzy=True,
        )

    if not similarity_file_is_valid(SIMILARITY_FILE_PATH):
        if SIMILARITY_FILE_PATH.exists():
            SIMILARITY_FILE_PATH.unlink()
        raise RuntimeError(
            "Could not download a valid similarity file from Google Drive. "
            "Make sure the file is shared publicly and Google Drive has not blocked the download."
        )

try:
    ensure_similarity_file()

    with SIMILARITY_FILE_PATH.open("rb") as similarity_file:
        similarity = pkl.load(similarity_file)
except Exception as error:
    st.error(f"Failed to load similarity data: {error}")
    st.stop()

with open("movies_dict.pkl", "rb") as movies_file:
    movies_dict = pkl.load(movies_file)

movies = pd.DataFrame(movies_dict)

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    try:
        time.sleep(POSTER_FETCH_DELAY_SECONDS)
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        poster_path = data.get("poster_path")
        if not poster_path:
            return PLACEHOLDER_POSTER
        return "https://image.tmdb.org/t/p/w500/" + poster_path
    except requests.RequestException:
        return PLACEHOLDER_POSTER

def recommend(movie):
    movie_index = movies[movies["title"] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    movies_posters = []
    for i in movies_list:
        movies_id = movies.iloc[i[0]].id
        recommended_movies.append((movies.iloc[i[0]].title))
        movies_posters.append(fetch_poster(movies_id))
    return recommended_movies, movies_posters

st.title("Movie Recommender System")
selected_movie_name = st.selectbox("Select a movie:", movies["title"].values)
if st.button("Recommend"):
    recommended_movies, posters = recommend(selected_movie_name)
    st.write("Recommended Movies:")
    columns = st.columns(5)
    for column, movie, poster in zip(columns, recommended_movies, posters):
        with column:
            st.text(movie)
            st.image(poster)
