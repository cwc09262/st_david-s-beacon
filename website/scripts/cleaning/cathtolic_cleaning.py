import re
from utils.common_functions import write_to_file

def main(text):
    try:
        # Read the file containing Psalms
        with open(text, 'r') as file:
            psalms_text = file.read()

        print(psalms_text)
        # Trying to do some editing to ahve the grammar and spacing to work


    except FileNotFoundError:
        print(f"The file '{text}' was not found.")


if __name__ == "__main__":
    main()