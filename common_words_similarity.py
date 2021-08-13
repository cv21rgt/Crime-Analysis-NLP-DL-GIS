"""
This script uses common words to determine how similar two documents are as a percentage.

Arguments are 1: Path to directory/folder that contains the files to compare
              2: A name for the CSV file that will be created.

The cut-off percentage on how you define "similarity" depends on the application. For example, this script
was used to compare newspaper articles on crime. The cut-off point was 40%. This is because the same crime 
story can be written more than once depending on public interest or proceedings in court e.g. a defendant
has been granted bail etc. However, the amount of detail in the written story reduces as time progresses - 
which makes it harder to tell how similar the current version is to the original article since the the common
words get fewer and fewer. For such a scenario a lower cut-off point is important.

Tip: Ideally you do not want to run more than 100 files at once. It's best to experiment with a few files
first depending on memory resources on your computer.
"""

from typing import List
import argparse
import spacy
import os
import pandas as pd

# Create an argument parser
parser = argparse.ArgumentParser()

# Add the positional arguments
parser.add_argument("directory", help="path to directory with files to compare")
parser.add_argument("filename", help="name of csv file (without .csv extension) to use for the similarity indices")

args = parser.parse_args()

# Get full file paths
def filePaths(directory_with_files: str) -> List[str]:
  """
  Gets the full path of each file in a directory

    Args:
      directory_with_files (str): path to directory that holds files

    Returns:
      filepaths (list): a list of full file paths 
  """

  # get a list of file names in directory
  list_of_files = os.listdir(directory_with_files) 

  # join directory path and file name to get full paths to files
  filepaths = [os.path.join(directory_with_files, filename) for filename in list_of_files]

  return filepaths

# Function to read the contents of a file
def get_file_contents(filename: str) -> str:
    """
    Reads the contents of a file

    Args:
      filename (str): full path to file

    Returns:
      filecontent (str): contents of file 
    """
    with open(filename, 'r') as filehandle:
        filecontent = filehandle.read()
    return filecontent

# Function to remove stop words, punctuation and pronouns
def process_text(text: str) -> str:
    """
    Removes stop words, punctuation, pronouns and empty tokens

    Args:
        text (str): contents of a file/sentence/paragraph etc as a string

    Returns:
        String of tokens with stop words, punctuation, pronouns and empty tokens removed
    """
    doc = nlp_lg(text.lower())
    result = []
    for token in doc:
        if token.text in nlp_lg.Defaults.stop_words:
            continue
        if token.is_punct:
            continue
        if token.lemma_ == '-PRON-':
            continue
        if token.text == " ":
            continue
        result.append(token.lemma_)
    return " ".join(result)

# Function to compute the Similarity between two documents as a percentage
def similarity(file_1: str, file_2: str)-> int:
    """
    Computes how similar two newspaper articles are. The similarity is calculated based on the
    common words that appear in both articles. This is after the removal of stop words, punctuation, 
    empty spaces and pronouns.

    Args:
        file_1 (str): full path to first newspaper article
        file_2 (str): full path to second article to compare with

    Returns:
        similarity_as_percentage (int): Percentage of how similar two articles are
    """

    # Get file contents, then remove stop words, punctuation & pronouns
    file1_contents = process_text(get_file_contents(file_1).replace("\n", " "))
    file2_contents = process_text(get_file_contents(file_2).replace("\n", " "))

    # remove duplicate words from string
    file1_contents = ' '.join(dict.fromkeys(file1_contents.split()))
    file2_contents = ' '.join(dict.fromkeys(file2_contents.split()))

    # create document objects, which contain the tokenized words
    doc1 = nlp_lg(file1_contents)
    doc2 = nlp_lg(file2_contents)

    ### Uncomment the following line if you want to see the words in file_1 used in computing the similarity
    #print(doc1)

    #print(f"************************************************************************************************")            
    
    ### Uncomment the following line if you want to see the words in file_2 used in computing the similarity
    #print(doc2)

    # Count how many times the tokens in file_1 appear in file_2
    count = 0
    for t1 in doc1:
        for t2 in doc2:
            if t1.text == t2.text:
                count += 1

    sim = 0
    # to avoid division by zero
    if (len(doc2) != 0):
        sim = count / len(doc2)
    else:
        sim = 0

    similarity_as_percentage = round(float(sim) * 100)

    return similarity_as_percentage

def main(directory, csv_filename):

    d = []
    files = []

    # List containing full paths to our files to compare
    files = filePaths(directory)

    # Loop through all files and compare each file to every other file
    for idx, file_1 in enumerate(files):
        for file_2 in files[idx + 1: ]:  
            # compute similarity
            similarity_percentage = similarity(file_1, file_2)
            # append data to a List of dictionaries
            d.append({"File_1": file_1, "File_2": file_2, "Similarity (%)": similarity_percentage})

    # Create a temporary Pandas DataFrame from our List of dictionaries
    temp_dataframe = pd.DataFrame(d)

    # save DataFrame to CSV file
    temp_dataframe.to_csv(f"{csv_filename}.csv")


if __name__ == "__main__":

    # load a large pipeline package that comes with word vectors
    nlp_lg = spacy.load('en_core_web_lg')

    # get the directory and filename values
    directory = args.directory
    csv_filename = args.filename
    
    # call the main() function
    main(directory, csv_filename)


