import sys
import os
import pickle
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# Get the current working directory and construct the cleaning path
current_dir = os.getcwd()
cleaning_dir = os.path.abspath(os.path.join(current_dir, "../cleaning"))

# Add the directory to sys.path
sys.path.append(cleaning_dir)

# Now import the class
from data_pipeline import TextPreprocessingPipeline



def retrieve_psalm(index, psalms):
    # Ensure index is a tuple with (document_name, psalm_number)
    doc, psalm_num = index  

    print(f"    Text: {doc}")
    print(f"    Psalm Number: {psalm_num}\n")

    # Retrieve and format the verse text as a paragraph
    matching_verses = psalms.loc[(psalms['text'] == doc) & (psalms['psalm_num'] == psalm_num), 'verse']

    if matching_verses.empty:
        print("    No matching Psalm found.")
        return

    # Removing trailing spaces
    verse_text = " ".join(matching_verses.tolist()).strip()

    # Ensure the last full word is displayed within the first 200 characters
    if len(verse_text) > 200:
        verse_text = verse_text[:200]  # Slice to the first 200 characters
        last_space = verse_text.rfind(' ')  # Find the last space in the first 200 characters
        verse_text = verse_text[:last_space]  # Trim to the last full word

    # Print the first 200 characters (or last full word if it's too long)
    print("   " + verse_text + "...\n")

def search_psalms(query, pipeline, vectorizer, model, psalms, num_results=6):
    clean_query = pipeline.pipeline(query)
    clean_vec = vectorizer.transform([clean_query])
    cosine_similarities = cosine_similarity(clean_vec, model).flatten()
    top_indices = cosine_similarities.argsort()[-num_results:][::-1]

    results = []
    for index in top_indices:
        doc, psalm_num = model.index[index]  # or adjust based on your model's structure
        verse_text = retrieve_psalm((doc, psalm_num), psalms)
        results.append({'doc': doc, 'psalm_num': psalm_num, 'text': verse_text})
    
    return results


def main():
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
        tf_idf_psalms = pickle.load(file)

    # accessing psalms via CSV
    psalms = pd.read_csv("../Data/clean_psalm_verses.csv")

    # Prompt user for search input
    query = input("Enter text to search the Psalms: ")

    # Perform the search with the given query
    search_psalms(query, pipeline, psalm_vectorizer, tf_idf_psalms, psalms, num_results=6)


# Run the script only if executed directly
if __name__ == "__main__":
    main()

