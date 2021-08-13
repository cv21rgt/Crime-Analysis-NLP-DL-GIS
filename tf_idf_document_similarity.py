"""
    In this script we accept the path to a directory/folder with files which we want to determine
    how similar the files are. A Similarity Index is computed between two files and the results will 
    be saved to a CSV file. It is up to the user to then determine what value to use as the cut-off 
    index to determine if two documents are similar or not. 

    Tip: Do not compare more than 100 files at a time. You might want to start with a few files 
         depending on your memory resources.

"""

import argparse
import os
from gensim import similarities
import pandas as pd
import gensim
import nltk
import numpy as np
import sys
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords

# Create an argument parser
parser = argparse.ArgumentParser()

# Add the positional arguments
parser.add_argument("directory", help="path to directory with files to compare")
parser.add_argument("filename", help="name of csv file (without .csv extension) to use for the similarity indices")

args = parser.parse_args()


# Get full file paths
def filePaths(directory_with_files):
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
    filecontent = ""
    # check if file exists before trying to read from it
    if os.path.exists(filename):
        with open(filename, 'r') as filehandle:
            filecontent = filehandle.read()
    else:
        sys.exit(f"File does not exists: {filename}")

    return filecontent

# Compute how similar two files are as a percentage
def similarity(file_1, file_2):
    
    file1_docs = []

    file2_docs = []

    avg_sims = []

    # get the English stopwords
    stopwords_en = stopwords.words("english")

    # open file and tokenize into Sentences
    fileContents = get_file_contents(file_1)
    # split file contents into sentences
    sentence_tokens = sent_tokenize(fileContents)
    # place the sentences into a list
    for line in sentence_tokens:
        file1_docs.append(line)

    # tokenize each sentence into words minus the stopwords like 'the', 'should' etc      
    gen_docs = [[w.lower() for w in word_tokenize(text) if w not in stopwords_en] 
                for text in file1_docs]

    # create a dictionary - each word will be given a unique Index
    dictionary = gensim.corpora.Dictionary(gen_docs)

    # Create a Bag of Words - this is an object that contains the word ID and its frequency in each document.
    # Document can refer to a sentence or paragraph
    # Corpus is typically a 'collection of documents as a bag of words'
    corpus = [dictionary.doc2bow(gen_doc) for gen_doc in gen_docs]

    # TF-IDF (Term Frequency - Inverse Document Frequency) --> is also a bag of words, however it 
    # calculates the weight of words that appear frequently across documents. Words that appear more 
    # frequently across a document get smaller weights.
    tf_idf = gensim.models.TfidfModel(corpus)

    # make sure you do not have another folder/directory named "sims-workdir" in your workspace
    temp_directory = "sims-workdir/"

    # check if such a directory already exists in the current workspace before creating it
    if not os.path.exists(temp_directory):
        os.mkdir(temp_directory)    

    # Create a Similarity measure object --> The Similarity class builds an index for a given set of 
    # documents. The Similarity class splits the index into several smaller sub-indexes, which are 
    # disk-based.
    sims = gensim.similarities.Similarity(temp_directory, tf_idf[corpus],
                                        num_features=len(dictionary))

    # open file and tokenize into Sentences
    fileContents_2 = get_file_contents(file_2)
    # split file contents into sentences
    sentence_tokens_2 = sent_tokenize(fileContents_2)
    # place the sentences into a list
    for line in sentence_tokens_2:
        file2_docs.append(line)
                
    for line in file2_docs:
        # tokenize each word in a sentence
        query_doc = [w.lower() for w in word_tokenize(line) if w not in stopwords_en]
        # update the existing dictionary and create Bag of Words
        query_doc_bow = dictionary.doc2bow(query_doc)    
        # perform a similarity query (file_2) against the corpus (created from file_1)
        query_doc_tf_idf = tf_idf[query_doc_bow]
        # print (document/sentence_number, document/sentence_similarity)
        #print(f"Comparing Result: {sims[query_doc_tf_idf]}")
        # calculate sum of similarities for each sentence in file_2
        sum_of_sims = (np.sum(sims[query_doc_tf_idf], dtype=np.float32))
        # calculate the averahe of similarity for each sentence in file_2
        avg = sum_of_sims / len(file1_docs)
        #print(f"Avg: {avg}")
        # add average values into an array
        avg_sims.append(avg)
    
    # compute the total average 
    total_avg = np.sum(avg_sims, dtype=np.float32)    
    
    # round the value and multiply by 100 to convert it to a percentage
    percentage_of_similarity = round(float(total_avg) * 100)

    # if percentage is greater than 100
    # that means documents are almost similar
    if percentage_of_similarity >= 100:
        percentage_of_similarity = 100
    
    return percentage_of_similarity
     
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

    # get the directory and filename values
    directory = args.directory
    csv_filename = args.filename
    
    # call the main() function
    main(directory, csv_filename)