"""
COMP20008 Semester 1
Assignment 1 Task 2
"""

import json

import requests
import bs4
import urllib
import unicodedata
import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

from robots import process_robots, check_link_ok


# Task 2 - Extracting Words from a Page (4 Marks)
def task2(link_to_extract: str, json_filename: str):
    # Download the link_to_extract's page, process it 
    # according to the specified steps and output it to
    # a file with the specified name, where the only key
    # is the link_to_extract, and its value is the 
    # list of words produced by the processing.
    # Implement Task 2 here
    return {}
