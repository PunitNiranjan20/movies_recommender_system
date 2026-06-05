import streamlit as st
import pickle
import pandas as pd
import requests
import time
import os
import gdown
FILE_ID = "1z3qAnXX7g4tHdBAl387gliO6mceYsgNf"

if not os.path.exists("similarity.pkl"):
    gdown.download(
        f"https://drive.google.com/uc?id={FILE_ID}",
        "similarity.pkl",
        quiet=False
    )

movies_dict = pickle.load(open('movies_dict.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))
movies = pd.DataFrame(movies_dict)

st.title('Movie Recommender System')

@st.cache_data(show_spinner=False)
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=a60aee69ba7f3e4bc90f6ab14f28ae55&language=en-US"

    for _ in range(3):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            break
        except requests.RequestException:
            time.sleep(0.5)
    else:
        return None

    poster_path = data.get('poster_path')
    if not poster_path:
        return None

    return "https://image.tmdb.org/t/p/w500/" + poster_path

def show_movie(column, name, poster):
    with column:
        st.text(name)
        if poster:
            st.image(poster, use_container_width=True)

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse = True,key = lambda x:x[1])[1:6]
    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
        time.sleep(0.2)
    return recommended_movies, recommended_movies_posters

selected_movie_name = st.selectbox(
    'Select a movie from the dropdown',
    movies['title'].values
)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    show_movie(col1, names[0], posters[0])
    show_movie(col2, names[1], posters[1])
    show_movie(col3, names[2], posters[2])
    show_movie(col4, names[3], posters[3])
    show_movie(col5, names[4], posters[4])
