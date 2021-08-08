"""
    In this script we accept the path to a directory/folder with files which we want to determine
    how similar the files are. A Similarity Index is computed between two files and the results will 
    be saved to a CSV file. It is up to the user to then determine what value to use as the cut-off 
    index to determine if two documents are similar or not. 

    Tip: If you have a lot of files to compare e.g 100 or more, you might want to check how many file handlers
         have been set on your operating system. This might need changing otherwise you will get an error. 
         On Linux use: "cat /proc/sys/fs/inotify/max_user_watches" to find the default no. of file handlers.
         To change this do the following:
            1. sudo nano /etc/sysct1.conf   # You can also use vim or nano
            2. Scroll down to the end of the file and type in the following: 
                        fs.inotify.max_user_watches = 524288
                and save the changes.

                While 524,288 is the maximum number of files that can be watched, if you're in an 
                environment that is particularly memory constrained, you may want to lower the number. 
                Each file watch takes up 1080 bytes, so assuming that all 524,288 watches are 
                consumed, that results in an upper bound of around 540 MiB.
            3. Load the new value by running:
                    sudo sysctl -p
            4. Run the command in step 1 to check if the change has been succesful.

"""

import argparse
import os
import pandas as pd
import gensim
import nltk
import numpy as np
from nltk.tokenize import word_tokenize, sent_tokenize

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

# Compute how similar two files are as a percentage
def similarity(file_1, file_2):
    
    file1_docs = []

    file2_docs = []

    # open file and tokenize into Sentences
    with open (file_1, "r") as f:
        tokens = sent_tokenize(f.read())
        for line in tokens:
            file1_docs.append(line)

    # tokenize each sentence into words        
    gen_docs = [[w.lower() for w in word_tokenize(text)] 
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

    # open second file/document and tokenize
    with open (file_2, "r") as f:
        tokens = sent_tokenize(f.read())
        for line in tokens:
            file2_docs.append(line)
            
    for line in file2_docs:
        # tokenize each word in a sentence
        query_doc = [w.lower() for w in word_tokenize(line)]
        # update the existing dictionary and create Bag of Words
        query_doc_bow = dictionary.doc2bow(query_doc)
    
    # perform a similarity query (file_2) against the corpus (created from file_1)
    query_doc_tf_idf = tf_idf[query_doc_bow]
    
    # compute average of the similarities
    average_similarity_index = sum(sims[query_doc_tf_idf]) / len(sims[query_doc_tf_idf])
    
    # convert similarity to a percentage
    percentage_of_similarity = round(average_similarity_index * 100)
    
    return percentage_of_similarity
     
def main(directory, csv_filename):

    d = []
    files = []

    # List containing full paths to our files to compare
    files = filePaths(directory)

    # Loop through all files and compare each file to every other file
    for idx, file_1 in enumerate(files[:10]):
        for file_2 in files[idx + 1: 10]:  
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
