import os
import pickle
import matplotlib
# Non-interactive backend for Flask
matplotlib.use('Agg')  
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import numpy as np
import base64
from io import BytesIO
from sklearn.decomposition import PCA
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from backend.psalm_search_lite import load_model


def graph_pca(query, psalms):
    # loading the model for use 
    tfidf_matrix = load_model()

    # Apply PCA to reduce dimensions to 2D
    pca = PCA(n_components=2)
    reduced_matrix = pca.fit_transform(tfidf_matrix)

    # Define colors and markers
    bible_color, psalter_color = 'blue', 'red'
    highlight_colors = ['green', 'orange']
    edge_colors = ['black', 'purple', 'cyan', 'magenta']

    fig, ax = plt.subplots(figsize=(10, 6))

    # Scatter Bible and Psalter points
    ax.scatter(reduced_matrix[:151, 0], reduced_matrix[:151, 1], 
               color=bible_color, alpha=0.7, marker='o', edgecolor='black', s=50, label='Bible')
    ax.scatter(reduced_matrix[151:, 0], reduced_matrix[151:, 1], 
               color=psalter_color, alpha=0.7, marker='o', edgecolor='black', s=50, label='Psalter')

   # Bin for the given Psalms to put in the graph title
    target_psalms = []

    # Highlight target Psalms
    for doc, num in psalms:  # Unpacking tuple correctly
        target_psalms.append(num)  # Recording the Psalm Number

         # Initialize highlight_index to avoid UnboundLocalError
        highlight_index = 0
        color = 'gray'  # Default color in case of unexpected values

        # Determining the document of the given psalm
        if doc == "Bible":
            highlight_index = num - 1  
            color = 'green'
        elif doc == "Psalter":
            highlight_index = (num - 1) + 151 
            color = 'orange'
        else:
            print(f"Warning: Unexpected doc type '{doc}' for Psalm {num}")


        if 0 <= highlight_index < len(reduced_matrix):  # Ensure valid index
            plt.scatter(reduced_matrix[highlight_index, 0], reduced_matrix[highlight_index, 1], 
                        color=color, edgecolor='black', 
                        s=350, label=f"{doc} Psalm {num}")

            # Adding the psalm number within the specific circle
            plt.text(reduced_matrix[highlight_index, 0], reduced_matrix[highlight_index, 1], 
                    str(num), fontsize=10, fontweight='bold', ha='center', va='center',
                    color='white' if color == 'green' else 'black')


    # Custom legend
    legend_handles = [
        mlines.Line2D([], [], color=bible_color, marker='o', markersize=10, label="Bible"),
        mlines.Line2D([], [], color=psalter_color, marker='o', markersize=10, label="Psalter"),
        mlines.Line2D([], [], color='green', marker='o', markersize=10, label="Highlighted Bible Psalms"),
        mlines.Line2D([], [], color='orange', marker='o', markersize=10, label="Highlighted Psalter Psalms")
    ]
    ax.legend(handles=legend_handles)
    # Writning the title in html on the page itself. 
    # ax.set_title(f"Searching for: '{query}'\nPsalms in Focus: {', '.join(map(str, psalms))}", fontsize=12)
    ax.set_xlabel('Principal Component 1')
    ax.set_ylabel('Principal Component 2')

    # Convert plot to Base64
    buffer = BytesIO()
    canvas = FigureCanvas(fig)
    canvas.print_png(buffer)
    
    
    return base64.b64encode(buffer.getvalue()).decode('utf-8')
