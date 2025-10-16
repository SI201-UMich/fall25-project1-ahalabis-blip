import csv
import os
from collections import defaultdict
import unittest

#Reading CSV into a list of dicts
def load_penguins(filename):
    data = []
    dir_path = os.path.dirname(__file__)
    file_path = os.path.join(dir_path,filename)
    with open(file_path, mode = 'r', newline='') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            data.append(row)
    #print (data)
    return data

def most_pop(penguins):   #Abbey Halabis's calculation 
    """
    Returns the island with the largest total penguin population
    and the largest island for each year.
    """
    island_counts = defaultdict(int)
    yearly_counts = defaultdict(lambda: defaultdict(int))

    for penguin in penguins:
        island = penguin.get("island")
        year = penguin.get("year")
        if not island or not year:
            continue
        island_counts[island] += 1
        yearly_counts[year][island] += 1

    # Find island with largest total population
    overall_largest = max(island_counts, key=island_counts.get)

    # Find largest island for each year
    largest_per_year = {}
    for year, counts in yearly_counts.items():
        largest_island = max(counts, key=counts.get)
        largest_per_year[year] = largest_island

    return overall_largest, largest_per_year


