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

def calculate_species_island_distribution(penguins):
    """
    Calculates the percentage of each species living on each island in each year.
    Returns: {year: {species: {island: percentage}}}
    penguins is a list of dicts wheere each dict represents one penguin
    """
    totals = {}     # total per species per year
    counts = {}     # counts- tracks how many penguins per species lives on the island per year

    #this loops through every penguin in the list 
    #gets the exact year, species and island for the penguin
    for penguin in penguins:
        year = penguin.get("year")
        species = penguin.get("species")
        island = penguin.get("island")
        if not (year and species and island): #if any of these are missing or not here it will skip
            continue

        # if the year isn't in the total and conts dict, create a new dictionary 
        if year not in totals:
            totals[year] = {}
            counts[year] = {}
        #if the species hasn't been seen for the year
        if species not in totals[year]:
            totals[year][species] = 0 #initializes to 0 becasue the penguin hasn't been counted yet
            counts[year][species] = {} 

        
        totals[year][species] += 1 #adds one to the total number of the certain species for the year
        counts[year][species][island] = counts[year][species].get(island, 0) + 1 #adds one to the number, if it hasn't already been counnted in the dict, it will start at 0

    
    result = {} #this will store the final percents of penguins
    for year in counts: #loop through each year in the counts
        result[year] = {}
        for species in counts[year]: #loops through the specific species for the year
            result[year][species] = {}
            total = totals[year][species]
            for island, num in counts[year][species].items(): #loop through the island for the species and year
                result[year][species][island] = round((num / total) * 100, 2) #calc percent, rounds to two places

    return result

def main():
    penguin_data = load_penguins("penguins.csv")  # load the data file
    overall, per_year = most_pop(penguin_data)  # get results

    print("Overall island with the most penguins:", overall)
    print("\nIsland with the most penguins per year:")
    for year, island in per_year.items():
        print(f"  {year}: {island}")
    
    print("\n--- Species Distribution by Island and Year ---")
    distribution = calculate_species_island_distribution(penguin_data)

    for year, species_data in distribution.items():
        print(f"\nYear {year}:")
        for species, island_data in species_data.items():
            print(f"  {species}:")
            for island, pct in island_data.items():
                print(f"    {island}: {pct}%")




