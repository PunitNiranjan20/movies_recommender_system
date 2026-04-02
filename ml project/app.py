import streamlit as st
import pickle as pkl
import pandas as pd
import requests
import time

PLACEHOLDER_POSTER = "https://via.placeholder.com/500x750?text=Poster+Unavailable"
POSTER_FETCH_DELAY_SECONDS = 0.4

similarity = pkl.load(open("similarity.pkl","rb"))
movies_dict = pkl.load(open("movies_dict.pkl","rb"))
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
