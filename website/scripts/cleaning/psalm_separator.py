import os
import re

def separate(text, start):
    input_path = '../../data/txt/' + text + '.txt'

    # Defining output path
    output_path = '../../data/psalms/' + text

    # Ensure the output directory exists
    if not os.path.exists(output_path):
        os.makedirs(output_path, exist_ok=True)
    # Check if 'psalms' exists and if it is not a directory, handle the error
    else:
        if not os.path.isdir(output_path):
            raise NotADirectoryError(f"'{output_path}' exists and is not a directory.")

    # Open and read the input file
    with open(input_path, 'r') as file:
        psalms_data = file.read()

    ''' Define the pattern to find the start of a psalm EX: 'PSALM 1' or 'Psalm 1' '''
    pattern = r"Psalm \d+|PSALM \d+"  # This pattern matches both 'Psalm X' and 'PSALM X'

    ''' Finding where the actual psalms start '''
    match = re.search(pattern, psalms_data)
    if match:
        placemarker = psalms_data.count('\n', 0, match.start()) + 1
        print("Placemarker:", placemarker)
    else:
        print("Pattern not found.")
        return

    ''' Reading in the text file from the start of the first psalm'''
    with open(input_path, 'r') as file:
        # Skip lines until the target line number
        for _ in range(placemarker - 1):
            file.readline()  # Skipping lines until the placemarker
        psalms = file.read()  # Read the rest of the file from the psalm start

    # Split psalms at 'PSALM' or 'Psalm'
    individ_psalms = re.split(r"Psalm \d+|PSALM \d+", psalms)  # This handles both 'Psalm X' and 'PSALM X'

    ''' Putting psalms in their own files '''
    # Remove any empty segments (e.g., leading or trailing empty strings from split)
    individ_psalms = [segment.strip() for segment in individ_psalms if segment.strip()]

    # Adjust for the first Psalm being off by one
    for i, psalm in enumerate(individ_psalms, start=start):
        output_file_path = os.path.join(output_path, f"psalm_{i}.txt")
        with open(output_file_path, 'w') as output_file:  # Use the correct file path
            output_file.write(f"PSALM {i}\n{psalm}")  # Include "PSALM X" header

    print(f"Split into {len(individ_psalms)} files.")

# Run the main function
if __name__ == "__main__":
    separate("psalter", 0)  # Start numbering from 0 for "psalter"
    separate("bible", -1)    # Start numbering from 1 for "bible"

