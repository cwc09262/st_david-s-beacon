import nltk
import re
import ssl
import os
import pickle
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from num2words import num2words


# Fix SSL certificate issues for downloading NLTK resources
ssl._create_default_https_context = ssl._create_unverified_context

# Ensure necessary NLTK resources are downloaded
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('wordnet')

class TextPreprocessingPipeline:
    def __init__(self):
        # Initialize stop words and lemmatizer
        self.stop_words_set = set(stopwords.words("english"))
        self.lemmatizer = WordNetLemmatizer()

    '''======== LOWERCASE ========'''
    def lowercase(self, text):
        return text.lower()

    '''======== STOP WORDS ========'''
    def remove_stop_words(self, text):
        # Storage for cleaned text
        newText = ""

        # Loop over words and add to newText if not a stopword
        for word in text.split():
            if word not in self.stop_words_set:  # .lower() ensures case-insensitive matching
                newText += " " + word

        # Returning the text without stop words
        return newText

    '''======== PUNCTUATION, APOSTROPHES, & SYMBOLS ========'''
    def remove_punctuation(self, text):
        # Symbols to remove (punctuation, etc.)
        symbols = "!\"#$%&()*+-.,/:;<=>?@[\]^_`{|}~\n"

        # Loop through each symbol and replace it with space
        for symbol in symbols:
            text = text.replace(symbol, ' ')

        # Remove apostrophes
        text = text.replace("'", "")  # Remove all apostrophes

        return text

    '''======== SINGLE CHARACTERS ========'''
    def remove_single_characters(self, text):
        # Ensure the input is a string
        if not isinstance(text, str):
            text = str(text)  # Convert to string if not already

        # Storage for cleaned text
        newText = ""

        # Split the text into words
        words = text.split()

        # Loop over words and add to newText if word length is greater than 1
        for word in words:
            if len(word) > 1:
                newText += " " + word

        return newText

    '''======== LEMMATIZATION ========'''
    def lemmatize_text(self, text):
        # Tokenize the text into words
        words = word_tokenize(text)

        # Lemmatize each word and join back into a single string
        newText = " ".join([self.lemmatizer.lemmatize(word) for word in words])

        # Returning the cleaned text
        return newText

    '''======== CONVERTING NUMBERS ========'''
    def convert_nums(self, text):
        # Return as-is if not a string
        if not isinstance(text, str):
            return text

        # Replace each number with its word form
        return re.sub(r'\d+', lambda x: num2words(int(x.group())), text)

    '''======== CREATING THE PIPELINE ========'''
    def pipeline(self, text):
        text = self.lowercase(text)
        text = self.remove_stop_words(text)
        text = self.convert_nums(text)
        text = self.remove_punctuation(text)
        text = self.remove_single_characters(text)
        text = self.lemmatize_text(text)

        # Returning the processed text
        return text

def main():
    # Define the save directory and ensure it exists
    save_dir = "../../data/pickles"
    os.makedirs(save_dir, exist_ok=True)

    # Save the pipeline object
    save_path = os.path.join(save_dir, "pipeline.pickle")
    pipeline = TextPreprocessingPipeline()

    with open(save_path, 'wb') as f:
        pickle.dump(pipeline, f)

    print(f"Pipeline saved successfully at {save_path}")

if __name__ == "__main__":
    main()
