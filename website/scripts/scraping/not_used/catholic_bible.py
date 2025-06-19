import requests, re
from bs4 import BeautifulSoup
from utils.common_functions import *

def scrape_psalm(num):
    try:
        # URL to get the psalm from
        url = 'https://bible.usccb.org/bible/psalms/' + str(num)

        # Confirming the page is active
        response = requests.get(url)
        # Check if the request was successful
        response.raise_for_status()

        # Parse the HTML with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Starting point to scrape the page for the psalm
        start = soup.find('li', class_='pager__item is-active')

        if start:
            # Locate the relevant section that follows the start point
            content_div = soup.find('div', class_='contentarea')

            # Container to hold the scraped psalm text
            psalm = ""

            if content_div:
                # Extract all paragraph and heading tags in the contentarea div
                elements = content_div.find_all(['p', 'small'])

                # Loop through each element and stop at <p class="fn wv">
                for element in elements:
                    # Skip elements with the class 'chsect'
                    if 'chsect' in element.get('class', []):
                        continue

                    # Stop at footnotes indicated by <p class="fn wv">
                    if 'fn' in element.get('class', []):
                        # Reached the footnotes
                        break

                    # Going through possible tags that are within each p tag
                    for sub_element in element.descendants:
                        # Check for the <span> with class "bcv" to insert "NEXT VERSE"
                        if sub_element.name == 'span' and 'bcv' in sub_element.get('class', []):
                            psalm += "<NEXT VERSE> "

                        # Skipping over everything that is a link to something because it is not part of the actual psalm
                        if sub_element.name in ['sup', 'a', 'span']:
                            continue

                        # Handling the single letters that are the footnote links
                        if len(sub_element) < 2:
                            continue

                        # Handling the text wrapped in the 'small' tag, which is usually formatted weirdly
                        if sub_element.name == 'small':
                            # Get the text, strip leading/trailing whitespace, and remove new lines
                            sub_element = sub_element.get_text(strip=True).replace('\n', '')
                            # Append text content to psalm if it's not an unwanted pattern
                            if not re.search(r'\bORD\b', sub_element):
                                psalm += sub_element + ' '

                        # Collecting the correct sub-elements
                        psalm += sub_element + " "

                # This regular expression will replace "ORD" and variations of it, ensuring "LORD" and "ORD" are handled correctly.
                psalm = re.sub(r'\bL?ORD\b', 'Lord', psalm)

                # Writing psalm to a txt file
                write_to_individual_file(num, psalm, 'Psalms Sorted/catholic/bible')

            else:
                print("Content area not found.")
        else:
            print("Starting point not found.")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the webpage: {e}")

def main():
    # Loop to go through the 150 Catholic Psalms
    for i in range(1, 151):
        scrape_psalm(i)

if __name__ == "__main__":
    main()
