###Dataset Link: https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata


import streamlit as st
import pickle
import requests
import pandas as pd

# Load the data
movies_dict = pickle.load(open('movie_list.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
movies_list = movies['title'].values
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Fetch poster using OMDb API
def fetch_poster(movie_title):
    api_key = "______"  # Replace with your OMDb API key
    url = f"http://www.omdbapi.com/?t={movie_title}&apikey={api_key}"
    response = requests.get(url)
    
    if response.status_code == 200:  # Check if the request was successful
        data = response.json()
        if 'Poster' in data and data['Poster'] != "N/A":  # Ensure poster data is available
            return data['Poster']
        else:
            return "https://via.placeholder.com/150?text=Poster+not+available"  # Placeholder for missing posters
    else:
        return "https://via.placeholder.com/150?text=Error+fetching+poster"  # Placeholder for errors

# Recommend movies
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    movies_list = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])[1:6]
    
    recommended_movies = []
    recommended_movie_posters = []
    for i in movies_list:
        movie_title = movies.iloc[i[0]].title
        recommended_movies.append(movie_title)
        recommended_movie_posters.append(fetch_poster(movie_title))
    
    return recommended_movies, recommended_movie_posters

# Streamlit app
st.title('Movie Recommender System')

# Dropdown to select a movie
selected_movie = st.selectbox(
    "Select a movie to get recommendations:",
    movies_list
)

# Display recommendations
if st.button('Show Recommendations'):
    recommended_movies, recommended_movie_posters = recommend(selected_movie)
    
    # Create columns to display movies and posters
    cols = st.columns(5)  # Adjust column count based on layout preference
    for col, name, poster in zip(cols, recommended_movies, recommended_movie_posters):
        with col:
            st.text(name)
            st.image(poster, use_column_width=True)
