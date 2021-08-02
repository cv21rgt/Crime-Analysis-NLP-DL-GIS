"""
    This script reads a csv file, extracts text from a row-column cell and creates a
    text file. 
"""

import pandas as pd
import argparse
import os
import uuid

ap = argparse.ArgumentParser()
ap.add_argument("-b", "--filepath", required=True, help="filepath to csv file")
#ap.add_argument("-n", "--column_name", required=True, help="name of column with data to convert to text file")
#ap.add_argument("-sr", "--start_row", required=True, help="first row to start converting column data to text file")
#ap.add_argument("-er", "-- last_row", required=True, help="last row to convert column data to text file")
#ap.add_argument("-d", "--directory", required=True, help="directory/folder to save the text files to")

#args = vars(ap.parse_args())

args = ap.parse_args()

if args.filepath:
    print("Filepath to csv file.")



# Extract input arguments

# csv filename
# column name 
# start row
# end row
# path to folder to save the txt files 
