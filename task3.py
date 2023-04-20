""" 
COMP20008 Semester 1
Assignment 1 Task 3
"""

from typing import Dict, List
import pandas as pd
import json
import requests
import bs4
import urllib
import unicodedata
import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
import csv
from robots import process_robots, check_link_ok
from task2 import task2

# Task 3 - Producing a Bag Of Words for All Pages (2 Marks)
def task3(link_dictionary: Dict[str, List[str]], csv_filename: str):
    # link_dictionary is the output of Task 1, it is a dictionary
    # where each key is the starting link which was used as the 
    # seed URL, the list of strings in each value are the links 
    # crawled by the system. The output should be a csv which
    # has the link_url, the words produced by the processing and
    # the seed_url it was crawled from, this should be output to
    # the file with the name csv_filename, and should have no extra
    # numeric index.
    # Implement Task 3 here

    # Empty dataframe to demonstrate output data format.
    links_col = []
    words_col = []
    seed_col = []
    dataframe = pd.DataFrame({'link_url': links_col, 'words': words_col, 'seed_url': seed_col}, index=links_col)
    
    for seed_url in link_dictionary.keys():
        links = link_dictionary[seed_url]
        for link_url in links:
            sentence = ''
            words = task2(link_url, 'BoW')
            for word in words[link_url]:
                sentence = sentence + ' ' + word
            dataframe.loc[len(dataframe)] = [link_url, sentence, seed_url]

    dataframe = dataframe.set_index('link_url')
    dataframe = dataframe.sort_values(by='link_url', ascending=True)
    dataframe.to_csv(csv_filename)
    return dataframe
