# Movie Recommender System

A web-based movie recommender system built with Streamlit. It suggests movies based on your selection and displays their posters using The Movie Database (TMDB) API.

## Features
- Movie recommendations based on similarity.
- Movie posters fetched from TMDB.
- Large similarity matrix (`similarity.pkl`) is downloaded automatically from Google Drive on first run.

## Demo
Deployed on Streamlit Cloud: [Your Streamlit App URL](https://share.streamlit.io/)

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/Divyansh2992/movie-recommender-system.git
cd movie-recommender-system
```

### 2. Install Requirements
```bash
pip install -r requirements.txt
```

### 3. Environment Variables
Create a `.env` file in the project root with the following content:
```env
GOOGLE_DRIVE_FILE_ID=https://drive.google.com/file/d/1kZs3b1cVcx-fnJUn3Sh3w9KvdhKcAsv2/view?usp=sharing
TMDB_API_KEY=your_tmdb_api_key_here
```
- Replace `your_tmdb_api_key_here` with your TMDB API key.
- The Google Drive link should be set to "Anyone with the link can view".

### 4. Run the App
```bash
streamlit run app.py
```

## Notes
- On first run, the app will download `similarity.pkl` from Google Drive. If the download fails, check your sharing settings and file link.
- Do **not** commit your real `.env` file to public repositories. Use `.env.example` for sharing config structure.

## File Structure
- `app.py` - Main Streamlit app
- `movies.pkl` - Movie metadata
- `similarity.pkl` - Similarity matrix (downloaded at runtime)
- `requirements.txt` - Python dependencies

## Troubleshooting
- If you see an error about `similarity.pkl` not being a valid pickle, the file may not have downloaded correctly. Check the debug output in the app and verify your Google Drive link and permissions.
