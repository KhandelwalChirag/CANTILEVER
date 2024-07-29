from flask import Flask, render_template, request
import pandas as pd
from fuzzywuzzy import process

app = Flask(__name__)

# Load the CSV file
df = pd.read_csv('lakme_products.csv')

def fuzzy_search(search_term, df, threshold=70):
    """
    Perform a fuzzy search on the dataframe.
    Returns a list of dictionaries containing matching products.
    """
    # Get all product names
    choices = df['Name'].tolist()
    
    # Find matches
    matches = process.extract(search_term, choices, limit=None)
    
    # Filter matches based on the similarity score
    good_matches = [match for match, score in matches if score >= threshold]
    
    # Return the rows that match
    return df[df['Name'].isin(good_matches)].to_dict('records')

@app.route('/', methods=['GET', 'POST'])
def index():
    search_performed = False
    results = []
    search_term = ''

    if request.method == 'POST':
        search_performed = True
        search_term = request.form['search']
        results = fuzzy_search(search_term, df)

    return render_template('index.html', 
                           results=results, 
                           search_performed=search_performed, 
                           search_term=search_term)

if __name__ == '__main__':
    app.run(debug=True)