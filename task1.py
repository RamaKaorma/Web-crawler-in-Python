""" 
COMP20008 Semester 1
Assignment 1 Task 1
"""

import pandas as pd
import json
from typing import Dict, List

import requests
import bs4
import urllib
from robots import process_robots, check_link_ok

# A simple page limit used to catch procedural errors.
SAFE_PAGE_LIMIT = 1000


# Task 1 - Get All Links (3 marks)
def task1(starting_links: List[str], json_filename: str) -> Dict[str, List[str]]:
    # Crawl each url in the starting_link list, and output
    # the links you find to a JSON file, with each starting
    # link as the key and the list of crawled links for the
    # value.
    # Implement Task 1 here
    
    # Find the base URL
    from urllib.parse import urlparse

    parsed_url = urlparse(starting_links[0])
    base_url = parsed_url.scheme + '://' + parsed_url.netloc
    path = parsed_url.path
    # .scheme returns the protocol, .netloc returns the website www.____.com/net/etc, path is /sub-link/sub-link

    ### READING robots.txt

    # Specify the location of robots.txt
    robots_item = '/robots.txt'

    robots_url = base_url + robots_item
    print(robots_url)
    page = requests.get(robots_url) # Gets the server's response to the HTTP request

    # Import robots file and derive the page rules
    from robots import process_robots, check_link_ok
    robots_rules = process_robots(page.text)

    # DEBUGGING CODE: Print which links are ok
    for test_link in starting_links:
        print("Can we visit {}? {}".format(test_link, "Yes" if check_link_ok(robots_rules, test_link) else"No"))


    return {}
