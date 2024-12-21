from flask import Flask, render_template, request
import pickle
import numpy as np
import pandas as pd

# Load pre-processed data
popular_df = pickle.load(open('C:\\Users\\ASUS\\Downloads\\recomendation-system\\recomendation-system\\python\\popular.pkl', 'rb'))
pt_df = pickle.load(open('C:\\Users\\ASUS\\Downloads\\recomendation-system\\recomendation-system\\python\\pt.pkl', 'rb'))
books_df = pickle.load(open('C:\\Users\\ASUS\\Downloads\\recomendation-system\\recomendation-system\\python\\books.pkl', 'rb'))
similarity_scores = pickle.load(open('C:\\Users\\ASUS\\Downloads\\recomendation-system\\recomendation-system\\python\\similarity_scores.pkl', 'rb'))

# Initialize Flask app
app = Flask(__name__)

@app.route('/')
def index():
    # Render homepage with popular books
    return render_template(
        'index.html',
        book_name=list(popular_df['Book-Title'].values),
        author=list(popular_df['Book-Author'].values),
        image=list(popular_df['Image-URL-M'].values),
        votes=list(popular_df['num_ratings'].values),
        rating=list(popular_df['avg_rating'].values)
    )

@app.route('/recommend')
def recommend_ui():
    # Render the recommendation input page
    return render_template('recommend.html')

@app.route('/recommend_books', methods=['POST'])
def recommend():
    # Handle book recommendation requests
    user_input = request.form.get('user_input')
    index = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]

    index = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates("Book-Title")['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates("Book-Title")['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates("Book-Title")['Image-URL-M'].values))


        data.append(item)
        print(data)

    return render_template('recommend.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
