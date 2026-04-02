# Movie Recommender System

This project is a Streamlit movie recommender app that downloads `similarity.pkl` from Google Drive at runtime.

## Files to keep in the repository

- `app.py`
- `requirements.txt`
- `movies_dict.pkl`
- `Dockerfile`

Do not commit `similarity.pkl` because it is downloaded when the app starts.

## Environment variables

- `SIMILARITY_FILE_URL`: public Google Drive link for `similarity.pkl`
- `TMDB_API_KEY`: TMDB API key used to fetch posters

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Build and run with Docker

```bash
docker build -t movie-recommender .
docker run -p 8501:8501 -e SIMILARITY_FILE_URL="https://drive.google.com/file/d/1C1nxZKKYLgzt6vfl0D7LLMfGvJnl6mU4/view?usp=sharing" movie-recommender
```
