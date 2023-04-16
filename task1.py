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

    ### FIND THE BASE URL ########################################################
    from urllib.parse import urlparse, urljoin
    for start_link in starting_links:
        parsed_url = urlparse(start_link)
        base_url = parsed_url.scheme + '://' + parsed_url.netloc
        path = parsed_url.path
        directory = path.split('/')[1]

        # Set of things to check for eaach link
        check = set()
        check.add(parsed_url.netloc)
        check.add(directory)

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
        output = {}
        visited[seed_url] = True
        pages_visited = 1

        # Find all the links in the html
        links = soup.findAll('a')

        # Search for all links that lead to "/sample_wiki" or so, storing them as the seed link
        path_segment = path.split('/')
        directory = base_url + '/' + path_segment[1]
        seed_links = soup.findAll('a', href=re.compile("^{}".format(path)))

        # Check if the seed links cannot be visited, remove if so
        for link in seed_links:
            sub_url = urlparse(link['href'])
            sub_path = sub_url.path
            if not check_link_ok(robot_rules, sub_path):
                seed_links.remove(link)

        # Check if the link 
        to_visit = []
        for link in links:
            if link not in seed_links and "href" in link.attrs:
                if not check_link_ok(robot_rules, link['href']):
                    continue
                to_visit.append(urljoin(seed_url, link['href']))

        # Find all outbound links on successor pages and explore each one
        while (to_visit):
            # Impose a limit to avoid breaking the site
            if pages_visited == SAFE_PAGE_LIMIT:
                break
            
            # Consume the list of urls
            # Assign the first item from to_visit to link, and remove it from the to_visit list
                # to make sure each link is visited once
            link = to_visit.pop(0)
            # print(link)
            # Get the webpage
            page = requests.get(link)
            if not page.ok:
                continue
            # Scrape the code, aka, get the html to pull out the links in the page
            soup = bs4.BeautifulSoup(page.text, 'html.parser')

            # Mark the item as visited, i.e., add to visited dict, remove from to_visit
            visited[link] = True
            new_links = soup.findAll('a')
            
            for new_link in new_links:
                # Skip the links that don't have href values (links that don't actually exist or don't lead anywhere)
                if "href" not in new_link.attrs or path_segment[1] not in new_link:
                    continue

                new_item = new_link['href']
                if '#' in new_item:
                    index = new_item.index('#')
                    new_item = new_item[:index]
                
                # Skip any links which Wikipedia has asked us not to visit.
                if not check_link_ok(robot_rules, new_item):
                    continue

                # Need to concat with base_url to get an absolute link, 
                # an example item <a href="/wiki/Category:Marvel_Cinematic_Universe_images_by_film_series"> 
                new_url = urljoin(link, new_item)
                new_parsed_url = urlparse(new_url)

                # Check it's not already in the list before adding it.
                if (new_url not in visited) and (new_url not in to_visit) and (new_parsed_url.netloc == base_url):
                    to_visit.append(new_url)
                
            # Increase the number of pages we've visited so the page limit is enforced.
            pages_visited = pages_visited + 1
            
            # print("pages_visited = " + str(pages_visited))
            # print("to_visit = " + str(len(to_visit)))
            # print("visited = " + str(len(visited)))
            # print()
            # print()

        print('\nvisited: {0:5d} pages; to_visit: {1:5d} pages '.format(len(visited), len(to_visit)))
        for i in visited:
            print(i)
    return {}