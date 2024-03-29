""" 
COMP20008 Semester 1
Assignment 1 Task 1
"""
import re
import pandas as pd
import json
from typing import Dict, List

import requests
import bs4
from urllib.parse import urlparse, urljoin
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
    output = {} # The final dictionary, to be converted to JSON

    for start_link in starting_links:
        output[start_link] = [];
        ### FIND THE BASE URL ########################################################
        parsed_url = urlparse(start_link)
        base_url = parsed_url.scheme + '://' + parsed_url.netloc
        path = parsed_url.path
        # .scheme returns the protocol, .netloc returns the website 
            # www.____.com/net/etc, path is /sub-link/sub-link

        ### READING ROBOTS.TXT ######################################################

        # Specify the location of robots.txt
        robots_item = '/robots.txt'
        robots_url = base_url + robots_item
        page_bot = requests.get(robots_url) # Gets the server's response to the HTTP request
        robot_rules = process_robots(page_bot.text)


        ### CREATING THE CRAWLER ####################################################
        # Check if we can visit the page, get the html using beautiful soup
        seed_url = base_url + path
        page = requests.get(seed_url)
        soup = bs4.BeautifulSoup(page.text, 'html.parser')

        # Initiate a dictionary to hold all the links and whether they've been visited
        visited = {}
        visited[seed_url] = True
        pages_visited = 1

        # Search for all links that lead to "/samplewiki" or so, storing them as the seed link
        path_segment = path.split('/')
        seed_links = soup.findAll('a', href=re.compile(f"^{path}"))

        # Find all the links in the html, making sure they are samplewiki or fullwiki
            # "All pages you need to crawl will be in the /samplewiki/ or /fullwiki/ 
            # section of the server, other links can freely be ignored"
        links = soup.findAll('a', href=re.compile(f".*\/{path_segment[1]}\/.*"))

        # Check if the seed links cannot be visited, remove if so
        for seed in seed_links:
            # full_url = urljoin(seed_url, seed['href'])
            sub_url = urlparse(seed['href']).path
            # sub_path = sub_url
            if not check_link_ok(robot_rules, sub_url):
                continue
            links.append(seed)

        # Find all outbound links on successor pages and explore each one
        for link in links:
            # Impose a limit to avoid breaking the site
            if pages_visited == SAFE_PAGE_LIMIT:
                break
            
            # Merge to create the full URL, just for easy access
            response = ''
            if type(link) != str:
                response = link['href']
                full_url = urljoin(seed_url, response)
            else:
                sub_link = link.split('/')
                response = sub_link[3] + sub_link[4]
                full_url = urljoin(seed_url, response)
            print(link)
            
            # Get the page, check if accessible
            page = requests.get(full_url)
            if not page.ok: # Skip if page is inaccessible
                continue

            # Scrape the code, aka, get the html to pull out the links in the page, once done, flag as visited
            soup = bs4.BeautifulSoup(page.text, 'html.parser')
            visited[link] = True

            
            # Check if link and path abides by robots.txt... Append to links if meets both rules
            sub_url = urlparse(response)
            sub_path = sub_url.path
            if link not in seed_links and sub_path == path:
                if check_link_ok(robot_rules, response) or check_link_ok(robot_rules, sub_path):
                    links.append(link)
                
            for i in links:
                print(i)
            print('==================================')
            # Explore the links inside the current link
            new_links = soup.findAll('a', href=re.compile(f".*\/{path_segment[1]}\/.*"))
            for new_link in new_links:
                
                # Skip links that don't lead anywhere
                if 'href' not in link.attrs:
                    continue
                
                new_item = new_link['href']
                if '#' in new_item:
                    index = new_item.index('#')
                    new_item = new_item[:index]
                
                # Skip any links which Wikipedia has asked us not to visit.
                if not check_link_ok(robot_rules, new_item):
                    continue

                # Need to concat with base_url to get an absolute link,
                new_url = urljoin(base_url, new_item)

                # Check it's not already in the list before adding it 
                if new_url not in visited and new_url not in links:
                    links.append(new_url)
            
            # Increase the number of pages we've visited so the page limit is enforced.
            pages_visited = pages_visited + 1
            # Add the link to the json file
            output[start_link].append(full_url)
            
    # Dump the output in a json file
    with open(json_filename, 'w') as f:
        output_json = json.dump(output, f)

    return output_json