from flask import Flask, render_template, request, redirect, url_for
import subprocess
import shlex
import sys 
import os
from backend.psalm_search_lite import TextPreprocessingPipeline
from backend.psalm_search_lite import search_psalms, retrieve_psalms, load_pipeline, load_model, load_vectorizer
from backend.graph_search_lite import graph_pca


# Initialize Flask app
app = Flask(__name__)


app = Flask(__name__)

@app.route('/index')
def home():
    return render_template('index.html')


@app.route('/results', methods=['POST'])
def search_results():
    query = request.form.get('query')
    if not query:
        # If no legit results exists
        return render_template('no_results.html', query="No query was given")

    # Call search_psalms directly
    index_results = search_psalms(query)

    # Debug statement
    #print(f"Top Results: {index_results}")

    # Fetching the doc bnd psalm num separately for the graph. 
    psalms = [(entry["doc"], entry["psalm_num"]) for entry in index_results]

    # Confirming Psalms format
    #print(f"Top Psalms: {psalms}")

    # retrieving the targeted psalms
    full_results = retrieve_psalms(index_results)

    # Debug Statement
    # print(f"Psalms Text (after retrieve_psalms): {full_results}")
    # print("=" * 40)
    if full_results:
        print("Starting the Graphing!")
        visual_data = graph_pca(query, psalms)
        return render_template('results.html', query=query, results=full_results, visual=visual_data)
    
    # If no legit results exists
    return render_template('no_results.html', query=query)


if __name__ == '__main__':                                                                          
    app.run()
 