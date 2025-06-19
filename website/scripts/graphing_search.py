from sklearn.decomposition import PCA
import matplotlib 
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import numpy as np
import os
import pickle
from flask import send_file


def graph_pca(query, psalms):

    # Loading the PCA model
    with open("models/pca_model.pkl", "rb") as f:
        loaded_pca = pickle.load(f)

    # Load TF-IDF matrix (Ensure you have this)
    with open("models/psalms_tfidf_matrix.pkl", "rb") as f:
        tfidf_matrix = pickle.load(f)

    # Apply PCA transformation
    reduced_matrix = loaded_pca.transform(tfidf_matrix)

    # Assuming you have a list of documents corresponding to the rows in the TF-IDF matrix
    documents = list(range(len(reduced_matrix)))

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
    
    # bin for the given Psalms to put in the graph title
    target_psalms = []
    
    try:
        for psalm, doc in psalms:
            # Recording the Psalm Number
            target_psalms.append(psalm)
            
            # Determining the document of the given psalm
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

    # Saving the graph
    img_path = "static/pca_plot.png"
    plt.savefig(img_path, format='png')
    plt.close()


if __name__ == "__main__":
    graph_pca("Illumine Our Hearts", [(4, "Psalter"), (23, "Psalter"), (51, "Psalter"), (100, "Bible")])
