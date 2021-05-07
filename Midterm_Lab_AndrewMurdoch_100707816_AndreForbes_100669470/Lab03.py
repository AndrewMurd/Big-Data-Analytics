"""
Andrew Murdoch and Andre Forbes

Implementation of PCY algorithm for frequent pairs using Apriori Algo to find triples.
"""

import time
from itertools import combinations

start = time.time()


def createCk(Lk, k):
    cand_list = []
    len_Lk = len(Lk)

    for i in range(len_Lk):
        for j in range(i + 1, len_Lk):
            L1 = list(Lk[i])[:k - 2]
            L2 = list(Lk[j])[:k - 2]
            L1.sort()
            L2.sort()
            if L1 == L2:
                cand_list.append(Lk[i] | Lk[j])
    return cand_list


# hash function for hashmap
def hash(i, j):
    return (i * j) % numBuckets


itemsets = [i.strip().split() for i in open('RetailsDataset', 'r').readlines()]

percentChunk = 0.01
min_support = 0.05
numBuckets = 2000  # number of buckets for hashmap

itemsets = itemsets[:int(len(itemsets) * percentChunk)]

C1 = []
for basket in itemsets:
    for item in basket:
        if not [item] in C1:
            C1.append([item])
C1 = [set(x) for x in C1]

count = {}
freq_items = []
L1 = []
countBuckets = [0] * numBuckets

for basket in itemsets:
    for item in C1:
        if item.issubset(basket):
            candidate = frozenset(item)
            if candidate not in count:
                count[candidate] = 1
            else:
                count[candidate] += 1
    # get all the pairs possible from each basket
    pairs = list(combinations(basket, 2))
    # hash each pair to hashmap
    for pair in pairs:
        listPair = list(pair)
        numbers = [int(x) for x in listPair]
        countBuckets[hash(numbers[0], numbers[1])] += 1

# convert bucket hashmap to bitmap
# changing bucket values to 1 if it meets support requirement (frequent bucket)
for i in range(0, len(countBuckets) - 1):
    if countBuckets[i] / len(itemsets) >= min_support:
        countBuckets[i] = 1
    else:
        countBuckets[i] = 0

for key in count:
    support = count[key] / len(itemsets)
    if support >= min_support:
        freq_items.insert(0, key)
        freq_items.insert(1, support)
        L1.insert(0, key)

print("Frequent Items: ", freq_items)

freq_pairs = []
L2 = []
C2 = []
final = []
count = {}
test = [list(x) for x in L1]

for i in test:
    final.append(int(i[0]))
# construct pair candidates
for basket in itemsets:
    pairs = list(combinations(basket, 2))
    for pair in pairs:
        listPair = list(pair)
        numbers = [int(x) for x in listPair]
        # if the pair hashes to a frequent bucket and each value in pair is frequent
        if countBuckets[hash(numbers[0], numbers[1])] == 1 and numbers[0] in final and numbers[1] in final:
            C2.append(pair)

for basket in itemsets:
    for item in C2:
        item = frozenset(item)
        if item.issubset(basket):
            candidate = frozenset(item)
            if candidate not in count:
                count[candidate] = 1
            else:
                count[candidate] += 1

for key in count:
    support = count[key] / len(itemsets)
    if support >= min_support:
        freq_pairs.insert(0, key)
        freq_pairs.insert(1, support)
        L2.insert(0, key)

print("Frequent Pairs: ", freq_pairs)
# create triple candidates
C3 = createCk(L2, 3)

count = {}
freq_items = []
L3 = []

for basket in itemsets:
    for item in C3:
        if item.issubset(basket):
            candidate = frozenset(item)
            if candidate not in count:
                count[candidate] = 1
            else:
                count[candidate] += 1

for key in count:
    support = count[key] / len(itemsets)
    if support >= min_support:
        freq_items.insert(0, key)
        freq_items.insert(1, support)
        L2.insert(0, key)

print("Frequent Triples: ", freq_items)

end = time.time()

print(f"Runtime of the program is {end - start}")
