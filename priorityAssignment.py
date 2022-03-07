# -*- coding: utf-8 -*-
"""
Created on Sun Mar  6 14:43:13 2022

@author: Jellydreamer
"""

import pandas as pd
import math
from datetime import datetime

# Import in database csv from path
sampleData = pd.read_csv("final_sample_data.csv")

# Array for showing the column types of sampleData
distance_columns = ['class', 'difficulty', 'days_remaining', 'priority']

train = sampleData.to_numpy()
# Collection of Functions for KNNeighbor

def dateDaysLeft(l_date, f_date):
    delta = l_date - f_date
    return delta.days

def euclidean_distance(row1, row2):
    inner_value = 0
    for i in range(len(distance_columns))[:-1]:
        inner_value += (row1[i] - row2[i]) ** 2
    return math.sqrt(inner_value)

# Bread and Butter function right here, gets back the optimized priority 
def getRecPriority(date_assigned, date_due, classification, difficulty):
    # Aquire the Delta in days
    dayDelta = dateDaysLeft(date_due, date_assigned)   
    # Task Entry variables to be compared and tested
    emptyPriority = 0
    x = [classification, difficulty, dayDelta, emptyPriority]
    # Setup logical variables
    minimum = 10000000
    optimalPriority = -1
    # Test task x against all training tasks in y
    for y in train:
        # Calculate Euclidian Distance for y
        distance = euclidean_distance(x, y)
        # Compare with current minimum, if current is minimum, replace it and update optimalPriority
        if(distance < minimum):
            minimum = distance
            optimalPriority = y[3]
    # once optimalPriority is found
    return optimalPriority
