"""
COMP20008 Semester 1
Assignment 1 Task 4
"""

import matplotlib.pyplot as plt
import pandas as pd
from typing import List, Dict
from collections import defaultdict, Counter


# Task 4 - Plotting the Most Common Words (2 Marks)
def task4(bow: pd.DataFrame, output_plot_filename: str) -> Dict[str, List[str]]:
    # The bow dataframe is the output of Task 3, it has 
    # three columns, link_url, words and seed_url. The 
    # output plot should show which words are most common
    # for each seed_url. The visualisation is your choice,
    # but you should make sure it makes sense for what it
    # is meant to be.
    # Implement Task 4 here
    
    counts = []
    for link in bow['seed_url'].unique():
        # print(link)
        rows = bow[bow['seed_url'] == link]
        
        print('\n\n\n\n\n\n\n\n')

        # word_counts = pd.DataFrame(columns=['word', 'count'])
        # for word in words['words'].unique():
        #     word_rows = words[words['words'] == word]
        #     count = word_rows['count'].sum()
        #     counts.append(count)
    # print(counts)
    return {}
