
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


'''
Retrieves the text of Psalms based on provided Psalm metadata.

This function accesses a CSV file containing Psalm verses and extracts the text 
corresponding to the given document and Psalm number.

Parameters:
psalms_info (list of dict): A list of dictionaries where each dictionary contains:
    - "doc" (str): The document identifier.
    - "psalm_num" (int): The Psalm number.

Returns:
list of dict: A list of dictionaries, each containing:
    - "doc" (str): The document identifier.
    - "psalm_num" (int): The Psalm number.
    - "psalm" (str): The extracted Psalm text.

'''    
def retrieve_psalms(psalms_info):
    # Confirmation of the Psalm info
    print(f"Psalm Information: \n{psalms_info}")
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

'''
 Searches for Psalms based on a given query using a pre-trained TF-IDF model and cosine similarity.
    
    The function performs the following steps:
    1. Loads necessary preprocessing components (pipeline, vectorizer, and TF-IDF matrix) from pickled files.
    2. Preprocesses the query using the same pipeline as the training data.
    3. Transforms the processed query into a TF-IDF vector.
    4. Computes cosine similarity between the query vector and the stored TF-IDF matrix.
    5. Filters results based on a similarity threshold.
    6. Sorts the filtered results in descending order of similarity.
    7. Retrieves and returns metadata for the most relevant Psalms.
    
    Parameters:
    query (str): The input text to search for relevant Psalms.
    
    Returns:
    list of dict: A list of dictionaries containing metadata for the most relevant Psalms.
    Each dictionary includes:
        - "doc" (str): The document identifier.
        - "psalm_num" (int): The corresponding Psalm number.
    
'''

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

from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import numpy as np

def graph_pca(query, psalms):

    # Define the directory where pickled files are stored
    load_dir = "../Data/pickles"

    # Load the preprocessed text pipeline
    with open(os.path.join(load_dir, "pipeline.pickle"), "rb") as f:
        pipeline = pickle.load(f)

    # Apply PCA to reduce dimensions to 2D
    pca = PCA(n_components=2)
    reduced_matrix = pca.fit_transform(tfidf)

    # Assuming you have a list of documents corresponding to the rows in the TF-IDF matrix
    documents = tfidf.index

    # Define colors for Bible and Psalter
    bible_color = 'blue'
    psalter_color = 'red'

    # Plot the reduced 2D data with color based on the group (Bible/Psalter)
    plt.figure(figsize=(12, 6))

    # Plot Bible documents (first 151, color blue)
    plt.scatter(reduced_matrix[:151, 0], reduced_matrix[:151, 1], 
                color=bible_color, alpha=0.7, label='Bible', marker='o', 
                edgecolor='black', s=50)

    # Plot Psalter documents (last 150, color red)
    plt.scatter(reduced_matrix[151:, 0], reduced_matrix[151:, 1], 
                color=psalter_color, alpha=0.7, label='Psalter', marker='o', 
                edgecolor='black', s=50)
    
    # bin for the given Pslams to put in the graph title
    target_psalms = []
    
    try:
        for psalm, doc in psalms:
            # Recording the Psalm Number
            target_psalms.append(psalm)
            
            # Determining the docmunt of the given psalm
            if doc == "Bible":
                highlight_index = psalm - 1  
                color = 'green'
            elif doc == "Psalter":
                highlight_index = (psalm - 1) + 151 
                color = 'orange'

            if 0 <= highlight_index < len(reduced_matrix):  # Ensure valid index
                plt.scatter(reduced_matrix[highlight_index, 0], reduced_matrix[highlight_index, 1], 
                            color=color, edgecolor='black', 
                            s=350, label=f"{doc} Psalm {psalm}")

                # Adding the psalm number within the specific circle
                plt.text(reduced_matrix[highlight_index, 0], reduced_matrix[highlight_index, 1], 
                         str(psalm), fontsize=10, fontweight='bold', ha='center', va='center',
                         color='white' if color == 'green' else 'black')

            else:
                print(f"Index error for Psalm {psalm}: No corresponding Psalter Psalm.")

    except IndexError as e:
        print(f"Unexpected index error: {e}")


    # Add legend (avoid duplicate labels)
    bible_legend = mlines.Line2D([], [], color=bible_color, marker='o', markersize=10, label="Bible")
    psalter_legend = mlines.Line2D([], [], color=psalter_color, marker='o', markersize=10, label="Psalter")
    highlighted_bible_legend = mlines.Line2D([], [], color='green', marker='o', markersize=10, label="Highlighted Bible")
    highlighted_psalter_legend = mlines.Line2D([], [], color='orange', marker='o', markersize=10, label="Highlighted Psalter")

    # adding custom legend
    plt.legend(handles=[bible_legend, psalter_legend, highlighted_bible_legend, highlighted_psalter_legend])

    # Titles and labels
    plt.suptitle('2D Visualization of TF-IDF Matrix (PCA) - The Book of Psalms vs Psalter')

    # Fixed the string formatting for multi-line title
    plt.title(f"$\mathbf{{Searching\ for\:}}$ '{query}'.\nFocus on Psalms in Order of Results: {', '.join(map(str, target_psalms))}")

    plt.xlabel('Principal Component 1')
    plt.ylabel('Principal Component 2')

    # Show plot
    plt.show()


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
