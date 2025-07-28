from flask import Flask, render_template, request, redirect, url_for, jsonify
import pandas as pd
import numpy as np
from fuzzywuzzy import fuzz
import os

app = Flask(__name__)

# Load the cleaned movie data
try:
    df = pd.read_csv('data/cleaned_data.csv')
    print(f"Loaded {len(df)} movies from dataset")
except FileNotFoundError:
    print("Error: Could not find cleaned_data.csv file")
    df = pd.DataFrame()

# Load similarity matrix
try:
    cosine_sim = np.load('similarity_matrix.npy')
    print("Similarity matrix loaded successfully")
except FileNotFoundError:
    print("Error: Could not find similarity_matrix.npy file")
    cosine_sim = None

@app.route('/', methods=['GET', 'POST'])
def index():
    """Main route for movie search and recommendations"""
    movie_title = None
    movie_information = None
    recommended_movies = []
    error_message = None
    
    if request.method == 'POST':
        movie_title = request.form.get('movie_title', '').strip()
        
        if not movie_title:
            error_message = "Please enter a movie title"
        elif df.empty:
            error_message = "Movie database is not available"
        else:
            # Check if movie exists in database
            if movie_title.lower() in df['Title'].str.lower().values:
                try:
                    recommended_movies, movie_information = recommend_movies(movie_title)
                except Exception as e:
                    error_message = f"Error getting recommendations: {str(e)}"
            else:
                error_message = "Movie not found. Please check the spelling or try a different movie."
    
    return render_template('index.html', 
                         movie_title=movie_title, 
                         movie_information=movie_information, 
                         recommended_movies=recommended_movies,
                         error_message=error_message)

# When suggested movie is clicked
@app.route('/recommend', methods=['POST', 'GET'])
def recommend():
    """Route for handling recommended movie clicks"""
    movie_title = request.args.get('movie_title', '').strip()
    error_message = None
    
    if not movie_title:
        error_message = "No movie title provided"
        return render_template('index.html', error_message=error_message)
    
    try:
        recommended_movies, movie_information = recommend_movies(movie_title)
        return render_template('index.html', 
                             movie_title=movie_title,
                             movie_information=movie_information, 
                             recommended_movies=recommended_movies)
    except Exception as e:
        error_message = f"Error getting recommendations: {str(e)}"
        return render_template('index.html', error_message=error_message)

@app.route('/search/', methods=['GET', 'POST'])
def search():
    """API endpoint for autocomplete suggestions"""
    query = request.args.get('query', '').strip()
    
    if not query or len(query) < 2:
        return jsonify({"suggestions": []})
    
    try:
        suggestions = name_suggestion(query).tolist()
        return jsonify({"suggestions": suggestions})
    except Exception as e:
        return jsonify({"suggestions": [], "error": str(e)})

def recommend_movies(movie_title):
    """Generate movie recommendations based on similarity"""
    if df.empty or cosine_sim is None:
        raise Exception("Movie database or similarity matrix not available")
    
    # Find the movie index
    try:
        idx = df[df["Title"].str.lower() == movie_title.lower().strip()].index[0]
    except IndexError:
        raise Exception("Movie not found in database")
    
    # Get similarity scores
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]  # Top 10 similar movies (excluding itself)
    movie_indices = [i[0] for i in sim_scores]

    # Get recommended movies data
    recommended_movies_title = df["Title"].iloc[movie_indices].values
    poster_urls = df['poster_url'].iloc[movie_indices].values

    recommended_movies = []
    for title, poster_url in zip(recommended_movies_title, poster_urls):
        recommended_movies.append({
            'Title': title,
            'poster_url': poster_url if poster_url and str(poster_url) != 'nan' else '/static/no-image.png'
        })

    # Get movie information
    movie_information = df.iloc[idx].to_dict()
    
    return recommended_movies, movie_information



def name_suggestion(query):
    """Return top 3 similar movie name suggestions for autocomplete"""
    if df.empty:
        return pd.Series([])
    
    query = query.lower().strip()
    df_titles = pd.DataFrame(df['Title'])
    df_titles['similarity'] = df_titles['Title'].str.lower().apply(
        lambda x: fuzz.ratio(x, query)
    )
    
    suggestions = df_titles.sort_values(
        by='similarity', ascending=False
    )[:3]['Title'].values
    
    return suggestions


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
