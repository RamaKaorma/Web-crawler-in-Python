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
    page = requests.get(link_to_extract)
    if not page.ok: # Skip if page is inaccessible
        return

    # Scrape the code, aka, get the html to pull out the links in the page, once done, flag as visited
    soup = bs4.BeautifulSoup(page.text, 'html.parser')
    body = soup.find('div', id='mw-content-text')

    th = body.findAll('th', class_='infobox-label')
    for tag in th:
        tag.decompose()

    div_footer = body.findAll('div', class_='printfooter')
    for tag in div_footer:
        tag.decompose()

    div_toc = body.findAll('div', id_='toc')
    for tag in div_toc:
        tag.decompose()

    table = body.findAll('table', class_='ambox')
    for tag in table:
        tag.decompose()

    div_asbox = body.findAll('div', class_='asbox')
    for tag in div_asbox:
        tag.decompose()

    span = body.findAll('span', class_='mw-editsection')
    for tag in span:
        tag.decompose()
    
    for data in body.findAll():
        print(data.get_text(' '))
        
    return {}
