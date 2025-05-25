import pickle
import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def download_file_from_google_drive(file_id, destination):
    URL = "https://drive.google.com/uc?export=download"
    session = requests.Session()
    response = session.get(URL, params={'id': file_id}, stream=True)
    token = None
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            token = value
    if token:
        params = {'id': file_id, 'confirm': token}
        response = session.get(URL, params=params, stream=True)
    with open(destination, "wb") as f:
        for chunk in response.iter_content(32768):
            if chunk:
                f.write(chunk)
    # Check if the file is actually an HTML warning page (not a pickle)
    with open(destination, 'rb') as f:
        start = f.read(100)
        if b'<!DOCTYPE html>' in start or b'<html>' in start:
            os.remove(destination)
            raise RuntimeError("Downloaded file is not a valid pickle. Check Google Drive sharing settings and file ID.")

def fetch_poster(movie_id):
    api_key = os.getenv('TMDB_API_KEY')
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    try:
        data = requests.get(url, timeout=5)
        data.raise_for_status()
        data = data.json()
        poster_path = data.get('poster_path')
        if poster_path:
            full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
            return full_path
        else:
            # Return a placeholder image if poster_path is missing
            return "https://via.placeholder.com/500x750?text=No+Image"
    except Exception as e:
        # Return a placeholder image if any error occurs
        return "https://via.placeholder.com/500x750?text=No+Image"

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters

st.header('Movie Recommender System')

# Download similarity.pkl from Google Drive if not present
SIMILARITY_PATH = 'similarity.pkl'
GOOGLE_DRIVE_FILE_ID = os.getenv('GOOGLE_DRIVE_FILE_ID')

# Extract file ID if a full URL is provided
if GOOGLE_DRIVE_FILE_ID and 'drive.google.com' in GOOGLE_DRIVE_FILE_ID:
    import re
    match = re.search(r'/d/([\w-]+)', GOOGLE_DRIVE_FILE_ID)
    if match:
        GOOGLE_DRIVE_FILE_ID = match.group(1)

if not os.path.exists(SIMILARITY_PATH):
    with st.spinner('Downloading similarity.pkl from Google Drive...'):
        try:
            download_file_from_google_drive(GOOGLE_DRIVE_FILE_ID, SIMILARITY_PATH)
            st.success('Downloaded similarity.pkl!')
        except Exception as e:
            st.error(f"Failed to download similarity.pkl: {e}")
            st.stop()

movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open(SIMILARITY_PATH, 'rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])
    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])