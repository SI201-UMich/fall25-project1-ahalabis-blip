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



class TestMostPop(unittest.TestCase):
        def setUp(self):
            self.sample_penguins = [
            {"species": "Adelie", "island": "Torgersen", "year": "2007"},
            {"species": "Adelie", "island": "Torgersen", "year": "2007"},
            {"species": "Gentoo", "island": "Biscoe", "year": "2008"},
            {"species": "Chinstrap", "island": "Dream", "year": "2008"},
            {"species": "Chinstrap", "island": "Dream", "year": "2008"},
            {"species": "Adelie", "island": "Torgersen", "year": "2008"},
        ]

    #Test 1: normal test case with a clear largest island
        def test_most_pop_normal(self):
            overall, per_year = most_pop(self.sample_penguins)
            self.assertEqual(overall, "Torgersen")
            self.assertEqual(per_year["2007"], "Torgersen")
            self.assertEqual(per_year["2008"], "Dream")

    #Test 2: Only one island
        def test_most_pop_single_island(self):
            data = [
            {"species": "Adelie", "island": "Biscoe", "year": "2007"},
            {"species": "Adelie", "island": "Biscoe", "year": "2008"},
        ]
            overall, per_year = most_pop(data)
            self.assertEqual(overall, "Biscoe")
            self.assertTrue(all(island == "Biscoe" for island in per_year.values()))

    #Test 3: A tie between the biggest islands
        def test_most_pop_tie(self):
            data = [
            {"species": "Adelie", "island": "Dream", "year": "2007"},
            {"species": "Adelie", "island": "Biscoe", "year": "2007"},
        ]
            overall, per_year = most_pop(data)
        #if there is a tie, max returns the first key entered
            self.assertIn(overall, ["Dream", "Biscoe"])
            self.assertIn(per_year["2007"], ["Dream", "Biscoe"])

    #Test 4: there are missing data entries
        def test_most_pop_with_missing_data(self):
            data = [
            {"species": "Adelie", "island": "Torgersen", "year": "2008"},
            {"species": "Adelie", "island": "", "year": "2008"},
            {"species": "Gentoo", "island": None, "year": "2008"},
            {"species": "Chinstrap", "island": "Dream", "year": ""},
        ]
            overall, per_year = most_pop(data)
        # Only valid entry is Torgersen in 2008
            self.assertEqual(overall, "Torgersen")
            self.assertEqual(per_year["2008"], "Torgersen")


class TestSpeciesIslandDistribution(unittest.TestCase):
    def setUp(self):
        self.sample_penguins = [
            {"species": "Adelie", "island": "Torgersen", "year": "2007"},
            {"species": "Adelie", "island": "Torgersen", "year": "2007"},
            {"species": "Gentoo", "island": "Biscoe", "year": "2007"},
            {"species": "Gentoo", "island": "Biscoe", "year": "2008"},
            {"species": "Adelie", "island": "Dream", "year": "2008"},
            {"species": "Adelie", "island": "Dream", "year": "2008"},
        ]

    # Test 1: Normal case with many species and years
    def test_distribution_normal(self):
        result = calculate_species_island_distribution(self.sample_penguins)
        self.assertIn("2007", result)
        self.assertIn("Adelie", result["2007"])
        self.assertIn("Torgersen", result["2007"]["Adelie"])
        self.assertEqual(result["2007"]["Adelie"]["Torgersen"], 100.0)
        self.assertEqual(result["2008"]["Adelie"]["Dream"], 100.0)

    #Test 2: All species on one island
    def test_single_island(self):
        data = [
            {"species": "Gentoo", "island": "Biscoe", "year": "2009"},
            {"species": "Gentoo", "island": "Biscoe", "year": "2009"},
        ]
        result = calculate_species_island_distribution(data)
        self.assertEqual(result["2009"]["Gentoo"]["Biscoe"], 100.0)
        self.assertEqual(len(result["2009"]["Gentoo"]), 1)

    #Tett 3: Missing data
    def test_missing_data(self):
        data = [
            {"species": "Adelie", "island": "Torgersen", "year": "2008"},
            {"species": "Adelie", "island": "", "year": "2008"},
            {"species": "Gentoo", "island": None, "year": "2008"},
            {"species": "Chinstrap", "island": "Dream", "year": ""},
        ]
        result = calculate_species_island_distribution(data)
        # Only one valid Adelie entry on Torgersen
        self.assertEqual(result["2008"]["Adelie"]["Torgersen"], 100.0)
        self.assertEqual(len(result), 1)

    #Test 4: Multiple islands for same species and year
    def test_multiple_islands_same_species(self):
        data = [
            {"species": "Adelie", "island": "Biscoe", "year": "2008"},
            {"species": "Adelie", "island": "Dream", "year": "2008"},
            {"species": "Adelie", "island": "Biscoe", "year": "2008"},
        ]
        result = calculate_species_island_distribution(data)
        self.assertAlmostEqual(result["2008"]["Adelie"]["Biscoe"], 66.67, delta=0.01)
        self.assertAlmostEqual(result["2008"]["Adelie"]["Dream"], 33.33, delta=0.01)




if __name__ == "__main__":
    main()
    unittest.main()