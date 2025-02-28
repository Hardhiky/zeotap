# app/app.py
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../data_processing'))  # Add data_processing directory to path
from vector_store import VectorStore
from flask import Flask, request, render_template

app = Flask(__name__)
cdps = ["Segment", "mParticle", "Lytics"]
vs = VectorStore(cdps)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        query = request.form['query']
        results = vs.search(query)
        response = "\n\n".join([f"CDP: {res[0]}\nChunk: {res[1]}" for res in results])
        return render_template('index.html', response=response)
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
