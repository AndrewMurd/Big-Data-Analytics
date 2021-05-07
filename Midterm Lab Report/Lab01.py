"""
Andrew Murdoch and Andre Forbes

Implementation of Apriori algorithm for frequent pairs and triples using apyori library.
"""

import pandas as pd
from apyori import apriori
import time

"""
17632 = 20%
35265 = 40%
52897 = 60%
70530 = 80%
88163 = 100%
"""
start = time.time()
# fileRetail = pd.read_csv("RetailsDataset")
fileRetail = pd.read_csv("NetflixDataset")
records = []

counter = 0
for row in fileRetail:
    if counter <= 88163:
        records.append(row)
    else:
        break
    counter += 1

association_rules = apriori(records, min_support=0.05)
association_results = list(association_rules)
print(association_results)
end = time.time()
print(end - start)
