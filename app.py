from flask import Flask, render_template, request, jsonify
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')

app = Flask(__name__)

# Load dataset
newsgroups = fetch_20newsgroups(subset='all')
documents = newsgroups.data  # List of text documents
stop_words = stopwords.words('english')

# Initialize TF-IDF Vectorizer
vectorizer = TfidfVectorizer(stop_words=stop_words)

# Fit the TF-IDF Vectorizer to the dataset
X_tfidf = vectorizer.fit_transform(documents)

# Initialize LSA (Truncated SVD)
lsa = TruncatedSVD(n_components=100)  # Using 100 components for dimensionality reduction
X_lsa = lsa.fit_transform(X_tfidf)

def search_engine(query):
    """
    Function to search for top 5 similar documents given a query.
    Input: query (str)
    Output: documents (list), similarities (list), indices (list)
    """
    # Transform the query into the same LSA space
    query_tfidf = vectorizer.transform([query])
    query_lsa = lsa.transform(query_tfidf)
    
    # Compute cosine similarity between the query and all documents
    similarities = cosine_similarity(query_lsa, X_lsa)
    
    # Get indices of the top 5 most similar documents
    top_indices = similarities.argsort()[0][-5:][::-1]  # Top 5 documents, sorted descending
    
    # Retrieve the corresponding documents and similarity scores
    top_documents = [documents[i] for i in top_indices]
    top_similarities = [similarities[0][i] for i in top_indices]
    
    return top_documents, top_similarities, top_indices.tolist()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    documents, similarities, indices = search_engine(query)
    return jsonify({'documents': documents, 'similarities': similarities, 'indices': indices})

if __name__ == '__main__':
    app.run(debug=True)

def test_example():
    assert 1 + 1 == 2

