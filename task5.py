"""
COMP20008 Semester 1
Assignment 1 Task 5
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, Union, List

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import PCA
from sklearn.preprocessing import Normalizer


# Task 5 - Dimensionality Reduction (3 marks)
def task5(bow_df: pd.DataFrame, tokens_plot_filename: str, distribution_plot_filename: str) -> Dict[str, Union[List[str], List[float]]]:
    # bow_df is the output of Task 3, for this task you 
    # should generate a bag of words, normalisation of the 
    # data perform PCA decomposition to 2 components, and 
    # then plot all URLs in a way which helps you answer
    # the discussion questions. If you would like to verify 
    # your PCA results against the sample data, you can return
    # the PCA weights - containing the list of most positive
    # weighted words, most negatively weighted words and the 
    # weights in the PCA decomposition for each respective word.
    # Implement Task 5 here

    return {}
