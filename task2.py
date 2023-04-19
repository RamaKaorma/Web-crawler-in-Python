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
from nltk.tokenize import word_tokenize

from robots import process_robots, check_link_ok


# Task 2 - Extracting Words from a Page (4 Marks)
def task2(link_to_extract: str, json_filename: str):
    # Download the link_to_extract's page, process it 
    # according to the specified steps and output it to
    # a file with the specified name, where the only key
    # is the link_to_extract, and its value is the 
    # list of words produced by the processing.
    # Implement Task 2 here
    output = {}
    response = requests.get(link_to_extract)
    if not response.ok: # Skip if page is inaccessible
        return
    encode = response.apparent_encoding
    page = response.content.decode(encode)
    ### NARROWING DOWN ##########################################################
    # Scrape the code, aka, get the html to pull out the links in the page
    soup = bs4.BeautifulSoup(page, 'html.parser')
    
    body = soup.find('div', id='mw-content-text')

    # Remove what is requied one step at a time
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
    
    ### Tokenize ################################################################
    # Extract the text from the html
    data = []
    for data_tags in body.contents:
        data.append(data_tags.get_text(separator=' ', strip=True))
    text = ' '.join(data)

    # Casefold and normalize
    normal = text.casefold()
    normal = unicodedata.normalize('NFKD', normal)
    
    # replace non-alphabetic characters with single sapce
    alpha = re.sub(r'[^a-zA-Z\s\\]', ' ', normal)
    
    # Replace whitespaces, newlines and tabs with single space
    nospace_data = re.sub('\s+', ' ', alpha)
    
    # Create explicit tokens, and remove empty strings ''
    tokens = word_tokenize(nospace_data)
    for token in tokens:
        if token == '':
            tokens.remove(token)
    
    # Remove English stopwords (first run the following on the command line) 
        # python
        # >> import nltk
        # >> nltk.download('stopwords')
    stop_words = set(stopwords.words('english'))
    tokens_no_stop = [word for word in tokens if (word.isalpha() and word not in stop_words)]
    
    # Remove short words
    tokens_no_stop = [word for word in tokens_no_stop if len(word) >= 2]
    
    # Convert to Porter stemming algorithm stemmed form
    stemmer = PorterStemmer() # Initialization
    stemmed_tokens = [] # Another new list
    for word in tokens_no_stop:
        stemmed_tokens.append(stemmer.stem(word)) # The actual tokenization
    
    output[link_to_extract] = stemmed_tokens

    print(stemmed_tokens)
    with open(json_filename, 'w') as f:
        json.dump(output, f)
    return output
