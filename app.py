from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import numpy as np

app = Flask(__name__)
# Load the cleaned movie data (adjust the path as needed)
df = pd.read_csv('data/cleaned_data.csv')

@app.route('/', methods=['GET', 'POST'])
def index():
    movie_title = None
    movie_information=None
    recommended_movies = []
    
    if request.method == 'POST':
        movie_title = request.form.get('movie_title')

        if movie_title in df['Title'].values:
            recommended_movies,movie_information = recommend_movies(movie_title, df)
            
    return render_template('index.html',movie_title=movie_title, movie_information=movie_information, recommended_movies=recommended_movies)


def recommend_movies(movie_title, df):

    cosine_sim = np.load('similarity_matrix.npy')
    idx = df[df["Title"] == movie_title].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]  # Top 10 similar movies (excluding itself)
    movie_indices = [i[0] for i in sim_scores]

    recommended_movies_title=df["Title"].iloc[movie_indices].values
    poster_urls=df['poster_url'].iloc[movie_indices].values

    recommended_movies=[]
    for title,poster_url in zip(recommended_movies_title,poster_urls):
        recommended_movies.append({'Title':title,
                            'poster_url':poster_url})

    movie_information=df.iloc[idx].to_dict()
    return recommended_movies,movie_information


if __name__ == '__main__':
    
    app.run(debug=True)
