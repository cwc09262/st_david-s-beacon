import pdfplumber, re, os

''' 
A challenge with is pdf is that the first letter in each psalm is dropped to be bigger. this script deomonstrates that the 
    pdf plumber package is the one between the two function that picked up the big letter, that is the package we are going to 
    go with in order to do all remaining scraping of pdfs.
    
NOTE: With more finagling I think there is a chance PYMuPDF would have worked. I did not put work work in figuring it out after 
    I got the other package to work. As another note, These are not the only pdf scrapers that exists, it is just the first two I tried. 
'''

''' NOT IN USE '''
'''
def scrape_pymupdf(pdf_path):
    print("PyMuPDF:\n")

    # Open and scrape PDF using PyMuPDF
    doc = fitz.open(pdf_path)
    for page in doc:
        text = page.get_text("text")  # Extract text in the 'text' format
        print(text)
'''

def scrape_pdfplumber_chatgpt(pdf_path):
    '''
    x_tolerance=2, y_tolerance=2: Increases spacing detection. Experiment with different values.

    re.sub(r'(\w)([A-Z])', r'\1 \2', text): Adds a space if lowercase and uppercase letters are incorrectly merged
    (e.g., "wordNEXT" → "word NEXT").

    :param pdf_path:
    :return:
    '''

    all_text = ''
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text(x_tolerance=2, y_tolerance=2)  # Adjust tolerances
            if text:
                text = re.sub(r'(\w)([A-Z])', r'\1 \2', text)  # Add space between words if needed
                cleaned_text = move_single_char_to_next_line(text)
                cleaned_text = add_next_verse_marker(cleaned_text)
                all_text += cleaned_text + '\n'
    return all_text


def scrape_pdfplumber(pdf_path):
    all_text = ''
    # Open and scrape PDF using pdfplumber
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()  # Extract text
            cleaned_text = move_single_char_to_next_line(text)  # Move single characters to the next line
            cleaned_text = add_next_verse_marker(cleaned_text)  # Add [NEXT VERSE] before numbers
            all_text += cleaned_text

    return all_text

def add_next_verse_marker(text):
    """
    Adds '[NEXT VERSE]' before any verse number. There is an exception not to do this when it comes across psalm and the number.
    Assumes verse numbers are standalone numbers (e.g., "1", "2", etc.).
    """
    return re.sub(r'(?<!Psalm )(?<!Psalm\s)(?<!\d)(\b\d+\b)', r'[NEXT VERSE] \1', text)


def move_single_char_to_next_line(text):
    # Use regex to find single characters on their own line and move them to the next line
    cleaned_text = re.sub(r'(^\w)\n([^\n])', r'\1\2', text, flags=re.MULTILINE)

    '''
    To remove all special characters such as '†ω' they are footnote symbols more than likely and will not 
        be any help as of now
    '''
    cleaned_text = re.sub(r'[^A-Za-z0-9\s]', '', cleaned_text)

    return cleaned_text

def main(pdf_path, output_path):

    raw_psalms = scrape_pdfplumber_chatgpt(pdf_path)

    # Ensure the directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # writing raw psalm text to a file for further cleaning in another script
    with open(output_path, 'w+', encoding='utf-8') as file:
        file.write(raw_psalms)
    print(f"The psalms from '{pdf_path}' have been scraped.")

if __name__ == "__main__":
    # Orthodox Bible
    main('../../data/pdf/psalms_from_bible.pdf', "../../data/txt/bible.txt")
    # Catholic Bible
    #main('../../Psalms Raw/pdf/catholic_bible_psalms.pdf', 'Psalms Raw/txt/catholic/bible.txt')
    # Anglican Paslter
    #main("../../Psalms Raw/pdf/Anglican Psalter.pdf", "../../Psalms Raw/txt/anglican/psalter.txt")
