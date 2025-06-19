
import requests
from bs4 import BeautifulSoup
import re
import os


# Function to scrape a webpage and clean the content
def scrape_webpage(url):
    try:
        # Fetch the HTML of the webpage
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful

        # Parse the HTML with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Replace all <br> tags with the text "Verse "
        for br in soup.find_all("br"):
            br.replace_with("[NEXT VERSE]")

        # Extract the text from the modified HTML
        page_content = soup.get_text()

        # Clean the content by removing extra whitespace and newline characters
        page_content = re.sub(r'[\r\n]+', ' ', page_content)  # Remove extra newline characters
        page_content = re.sub(r'\s+', ' ', page_content).strip()  # Replace multiple spaces with a single space

        # Return the cleaned content
        return page_content

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the webpage: {e}")
        return None


# Function to write content to a file
def write_to_file(content, output_path):
    # Ensure the directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Write content to the file
    with open(output_path, 'w') as file:
        file.write(content)


def main(source, output):
    print(f"Current Working Dir: {os.getcwd()}")

    # Call the scrape function
    content = scrape_webpage(source)

    if content:
        # Replace multiple newlines with a single newline
        cleaned_content = content.replace('\n\n', '\n').strip()

        # Print cleaned content
        #print(cleaned_content)

        # Write the cleaned content to the output file
        write_to_file(cleaned_content, output)
        print(f"File saved: {output}")
    else:
        print("No content to write.")


if __name__ == "__main__":
    # Orthodox Psalter
    main('https://www.liturgies.net/Prayers/orthodoxpsalter.html', "../../data/txt/psalter.txt")
