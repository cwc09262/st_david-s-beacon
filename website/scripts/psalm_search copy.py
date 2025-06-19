
import sys
import os
import pickle
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from data_pipeline import TextPreprocessingPipeline
from flask import render_template_string
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import numpy as np


def retrieve_psalms(psalms_info):
    # Confirmation of the Psalm info
    # print(f"Psalm Information: \n{psalms_info}")
    
    # accessing psalms text via CSV
    psalms = pd.read_csv("../Data/clean_psalm_verses.csv")

    # container for the text, has tø be outside of the loop. 
    target_psalm = []
    # Looping through each result in the dictionary 
    for psalm in psalms_info: 
        # print debug statement
        '''print(f"In Retrieve Psalm FUnction{psalm}")'''

        # assigning the specific doc and psalm number of the specific psalm
        doc = psalm['doc']
        psalm_num = psalm['psalm_num']
        metric = psalm['similarity']

        # Confirming the variables are correct
        #print(f"    Text: {doc}")
        #print(f"    Psalm Number: {psalm_num}\n")
        
        # Retrieve and format the verse text as a paragraph
        matching_verses = psalms.loc[(psalms['text'] == doc) & (psalms['psalm_num'] == psalm_num), 'verse']

        if matching_verses.empty:
            return render_template_string("""
                <html>
                    <body>
                        <h1>No matching Psalm found.</h1>
                    </body>
                </html>
            """)
        # Removing trailing spaces
        verse_text = " ".join(matching_verses.tolist()).strip()

        # Not using the code any more as I am going to handle the amount display within the html code
            # that is displaying the results.
        # Ensure the last full word is displayed within the first 200 characters
        #if len(verse_text) > 200:
        #   verse_text = verse_text[:200]  # Slice to the first 200 characters
        #  last_space = verse_text.rfind(' ')  # Find the last space in the first 200 characters
        #   verse_text = verse_text[:last_space]  # Trim to the last full word

        
        # adding the text to the results array
        target_psalm.append({"doc": doc, "psalm_num":psalm_num, "psalm":verse_text, "similarity":metric})

    # Debug statement
    '''print(f"Target Psalms at the end of retrieval: {target_psalm}")'''

    # Returning the full results of the query
    return target_psalm



def search_psalms(query):
    # Get the current working directory and construct the cleaning path
    current_dir = os.getcwd()
    cleaning_dir = os.path.abspath(os.path.join(current_dir, "../cleaning"))

    # Add the directory to sys.path
    sys.path.append(cleaning_dir)

    # Define the directory where pickled files are stored
    load_dir = "../Data/pickles"

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
    
    # Print the top 5 results
    #print(f"Filtered Top Result metrics: {(filtered_similarities)}")

    # Get indices where similarity ≥ threshold
    filtered_indices = np.where(cosine_similarities >= threshold)[0]


    # Reporting the number of results
    # print(f"Top {len(filtered_similarities)} results.")
    # print(filtered_similarities)


    # Get the indices of the top_n most similar Psalms
    # top_indices = cosine_similarities.argsort()[-num_results:][::-1]

    # printing the head of the top results
    # print(f"Top Result metrics: {top_indices[:5]}")
    

    # For the ranking of the results
    n = 1
    
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



def main():
    # Get the current working directory and construct the cleaning path
    current_dir = os.getcwd()
    cleaning_dir = os.path.abspath(os.path.join(current_dir, "../cleaning"))

    # Add the directory to sys.path
    sys.path.append(cleaning_dir)

    # Define the directory where pickled files are stored
    load_dir = "../pickles"

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
        tf_idf_psalms = pickle.load(file)

    # accessing psalms via CSV
    psalms = pd.read_csv("../Data/clean_psalm_verses.csv")

    # Prompt user for search input
    query = input("Enter text to search the Psalms: ")

    # Perform the search with the given query
    search_psalms(query, pipeline, psalm_vectorizer, tf_idf_psalms, psalms, num_results=6)


# Run the script only if executed directly
if __name__ == "__main__":
    graph_pca("Illimine Our Hearts", [(4, "Psalter"), (23, "Psalter"), (51, "Psalter"), (100, "Bible")])
