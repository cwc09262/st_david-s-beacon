import requests
import re
from bs4 import BeautifulSoup
from utils.common_functions import write_to_individual_file  # Assuming this function is implemented in your utils module


def scrape_psalm(translation, psalm_number, debug=False):
    """
    Scrapes the text of a specific Psalm from Bible Gateway.

    Args:
        translation (str): The Bible translation (e.g., "NIV", "KJV").
        psalm_number (int): The number of the Psalm to scrape.
        debug (bool): Whether to enable debug mode for detailed output.

    Returns:
        str: The scraped Psalm text or None if an error occurred.
    """
    try:
        # URL to get the Psalm from, parameterizing the Psalm number
        url = f"https://www.biblegateway.com/passage/?search=Psalm%20{psalm_number}&version={translation.upper()}"

        if debug:
            print(f"Fetching URL: {url}")

        # Send a GET request
        response = requests.get(url)

        # Raise an exception for HTTP errors
        response.raise_for_status()

        # Parse the HTML with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Remove unnecessary elements like cross-references and footnotes
        for tag in soup.find_all('sup', class_=['crossreference', 'footnote']):
            tag.extract()

        # Add placeholders for verse numbers
        for verse_num in soup.find_all('sup', class_='versenum'):
            verse_num.replace_with("[NEXT VERSE]")

        # Locate the main content div
        content_div = soup.find('div', class_='passage-text')

        if not content_div:
            if debug:
                print(f"Content area for Psalm {psalm_number} not found.")
            return None

        # Collect and clean the Psalm text
        psalm_text = f"Psalm {psalm_number}\n"
        for line in content_div.find_all('div', class_="poetry"):
            psalm_text += line.get_text(separator=' ').strip() + ' '

        # Clean up whitespace
        psalm_text = re.sub(r'\s+', ' ', psalm_text).strip()

        return psalm_text

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the webpage: {e}")
        return None


def main(translation, output, debug=False):
    """
    Main function to scrape Psalms and save them to files.

    Args:
        translation (str): The Bible translation (e.g., "NIV", "KJV").
        output (str): The directory where the Psalm files will be saved.
        debug (bool): Whether to enable debug mode for detailed output.
    """
    if debug:
        print(f"Translation: {translation}")
        print(f"Output Directory: {output}")

    # Loop through Psalm numbers (adjust range as needed)
    for psalm_number in range(1, 151):  # Change range as needed
        psalm = scrape_psalm(translation, psalm_number, debug)
        if psalm:
            if debug:
                print(f"Psalm {psalm_number} successfully scraped.")
            # Save each Psalm to a text file
            write_to_individual_file(psalm_number, psalm, output)


if __name__ == "__main__":
    # New International Version
    main("niv", "Psalms Sorted/protestant/niv/", debug=False)
    # Contemporary English Version
    main("cev", "Psalms Sorted/protestant/cev/", debug=False)
    # King James Version
    #main("kjv", "Psalms Sorted/protestant/kjv/", debug=False)