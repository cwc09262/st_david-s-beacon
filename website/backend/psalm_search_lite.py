
import sys
import os
import pickle
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from backend.data_pipeline import TextPreprocessingPipeline
from flask import render_template_string
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import numpy as np

def retrieve_psalms(psalms_info, psalms_file="../data/clean_psalm_verses.csv"):
    # Get the absolute path of the current script (inside scripts/)
    SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))

    # Move up one level to the app directory, then access models/
    BASE_DIR = os.path.dirname(SCRIPT_DIR)
    data_dir = os.path.join(BASE_DIR, "data")


     # Load the pickled files: pipeline, vectorizer, and model
    with open(os.path.join(data_dir, "clean_psalm_verses.csv"), "rb") as f:
        psalms = pd.read_csv(f)

    # Use list comprehension for better performance and cleaner code
    target_psalm = [
        {
            "doc": psalm['doc'],
            "psalm_num": psalm['psalm_num'],
            "psalm": " ".join(psalms.loc[(psalms['text'] == psalm['doc']) & 
                                         (psalms['psalm_num'] == psalm['psalm_num']), 'verse'].tolist()).strip(),
            "similarity": psalm['similarity']
        }
        for psalm in psalms_info
    ]
    
    return target_psalm


def search_psalms(query, threshold=0.05):
    # Load the required resources only once, passing paths as arguments
    pipeline = load_pipeline()
    psalm_vectorizer = load_vectorizer()
    model = load_model()
    
    # Running the query through the data pipeline and vectorizer
    clean_query = pipeline.pipeline(query)
    vector = psalm_vectorizer.transform([clean_query])

    # Calculate cosine similarities
    cosine_similarities = cosine_similarity(vector, model).flatten()

    # Get filtered indices where similarity ≥ threshold
    filtered_indices = np.where(cosine_similarities >= threshold)[0]
    
    # Sort indices based on similarity values in descending order
    sorted_indices = filtered_indices[np.argsort(cosine_similarities[filtered_indices])[::-1]]
    
    # Prepare results
    results = [
        {"doc": model.index[index][0], "psalm_num": model.index[index][1], "similarity": round(cosine_similarities[index] * 100, 2)}
        for index in sorted_indices
    ]
    
    # Return sorted results
    return results


def load_pipeline():
     # Get the absolute path of the current script (inside scripts/)
    SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))

    # Move up one level to the app directory, then access models/
    BASE_DIR = os.path.dirname(SCRIPT_DIR)
    MODELS_DIR = os.path.join(BASE_DIR, "data/models")
    
    # Load the pickled files: pipeline, vectorizer, and model
    with open(os.path.join(MODELS_DIR, "pipeline.pickle"), "rb") as f:
        pipeline = pickle.load(f)
    
    # Returning the Pickles
    return pipeline


def load_vectorizer():
     # Get the absolute path of the current script (inside scripts/)
    SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))

    # Move up one level to the app directory, then access models/
    BASE_DIR = os.path.dirname(SCRIPT_DIR)
    MODELS_DIR = os.path.join(BASE_DIR, "data/models")
    
    
    with open(os.path.join(MODELS_DIR, "psalms_tfidf_vectorizer.pickle"), "rb") as file:
        vectorizer = pickle.load(file)

    
    # Returning the Pickle
    return vectorizer


def load_model():
     # Get the absolute path of the current script (inside scripts/)
    SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))

    # Move up one level to the app directory, then access models/
    BASE_DIR = os.path.dirname(SCRIPT_DIR)
    MODELS_DIR = os.path.join(BASE_DIR, "data/models")
    
    with open(os.path.join(MODELS_DIR, "psalms_tfidf_matrix.pickle"), "rb") as file:
        model = pickle.load(file)
    
    # Returning the Pickles
    return model


'''
def search_psalms_old(query):
   
    # Define the directory where pickled files are stored
    load_dir = "../models"

    # Load the preprocessed text pipeline
    with open(os.path.join(load_dir, "pipeline.pickle"), "rb") as f:
        pipeline = pickle.load(f)

    # Load the pickled vectorizer
    vectorizer_path = os.path.join(load_dir, "psalms_tfidf_vectorizer.pickle")
    with open(vectorizer_path, "rb") as file:
        psalm_vectorizer = pickle.load(file)

    # Load the pickled TF-IDF matrix (optional, if you need to load the transformed matrix)
    matrix_path = os.path.join(load_dir, "psalms_tfidf_matrix.pickle")
    with open(matrix_path, "rb") as file:
        model = pickle.load(file)

    # Displaying the query
    print(f"\033[1mSearching for:\033[0m {query}.\n")
    
    
    # Running the query through the data pipeline
    clean_query = pipeline.pipeline(query)

    # Transform the query using the loaded vectorizer
    clean_vec = psalm_vectorizer.transform([clean_query])

    # Calculate the cosine similarity between the query vector and the TF-IDF matrix
    cosine_similarities = cosine_similarity(clean_vec, model).flatten()

    # Define a similarity threshold valid results need to have some similarity to be printed
    threshold = 0.05

    # Filter values above threshold
    filtered_similarities = cosine_similarities[cosine_similarities >= threshold]

     # Reporting the number of results
    print(f"Top {len(filtered_similarities)} results.")
    
    # Get indices where similarity ≥ threshold
    filtered_indices = np.where(cosine_similarities >= threshold)[0]

    # Sort indices based on similarity values in descending order
    sorted_indices = filtered_indices[np.argsort(filtered_similarities)[::-1]]

    # Container for the results
    results = []

    # Looping through the indices to store results with similarity scores
    for index in sorted_indices:
        # Ensure you have access to both the document name and psalm number from your model
        doc, num = model.index[index]  # Adjust this part based on your data structure
        # converting the similarity to a percentage
        metric = round(cosine_similarities[index]*100, 2) 
        # Adding the results to a dictionary
        results.append({"doc": doc, "psalm_num": num, "similarity": metric})

    # Returning the results dictionary
    return results


# Run the script only if executed directly
if __name__ == "__main__":
    graph_pca("Illimine Our Hearts", [(4, "Psalter"), (23, "Psalter"), (51, "Psalter"), (100, "Bible")])
'''
