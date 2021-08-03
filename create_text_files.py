"""
    This script reads a csv file, extracts text from a row-column cell and creates a
    text file. 
"""

import pandas as pd
import argparse
import os
import sys
import uuid

# Create an argument parser
parser = argparse.ArgumentParser()

# Add the positional arguments
parser.add_argument("filepath", help="filepath to csv file")
parser.add_argument("column_name", help="name of column with data to convert to text file")
parser.add_argument("start_row", help="first row to start converting column data to text file")
parser.add_argument("last_row", help="last row to convert column data to text file")
parser.add_argument("directory", help="directory/folder to save the text files to")

args = parser.parse_args()

csv_filepath = args.filepath
column_name = args.column_name
start_row = int(args.start_row)
last_row = int(args.last_row)
directory = args.directory

# Read CSV file into a Pandas dataframe
df = pd.read_csv(csv_filepath)

# Loop through dataframe from starting row to end row
for idx in range(start_row, last_row + 1):
    # Get the data at the intersection of row_index == idx and column == column_name
    text = df.loc[idx, column_name]
    # Path to text file with unique ID
    text_filepath = os.path.join(directory, f"{str(uuid.uuid1())}.txt")
    # Open file object for "writing"
    file = open(text_filepath, "w")
    # Write to file
    file.write(text)
    # Close file object
    file.close()    
