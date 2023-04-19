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

INVALID = {'th':['class', 'infobox-label'], 'div':['class', 'printfooter'], 'div':['id', 'toc'], 
           'table':['class', 'ambox'], 'div':['class', 'asbox'], 'span':['class', 'mw-editsection']}

# Task 2 - Extracting Words from a Page (4 Marks)
def task2(link_to_extract: str, json_filename: str):
    # Download the link_to_extract's page, process it 
    # according to the specified steps and output it to
    # a file with the specified name, where the only key
    # is the link_to_extract, and its value is the 
    # list of words produced by the processing.
    # Implement Task 2 here
    # print('\n\n' + link_to_extract + '\n\n')
    page = requests.get(link_to_extract);
    if not page.ok: # Skip if page is inaccessible
        return

    # Scrape the code, aka, get the html to pull out the links in the page, once done, flag as visited
    soup = bs4.BeautifulSoup(page.text, 'html.parser')
    body = soup.find('div', id='mw-content-text')
    print(soup)
    for tag in soup('th'):
        if tag['class'] == 'infobox-label':
            tag.decompose()
    for tag in soup('div'):
        if tag['class'] == ('printffoter' or 'asbox') or tag['id'] == 'toc':
            tag.decompose()
    for tag in soup('table'):
        if tag['class'] == 'ambox':
            tag.decompose()
    for tag in soup('span'):
        if tag['class'] == 'mw-editsection':
            tag.decompose()
    print(soup)
    return {}
