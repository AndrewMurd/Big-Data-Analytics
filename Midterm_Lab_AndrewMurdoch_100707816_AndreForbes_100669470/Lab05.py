"""
Andrew Murdoch and Andre Forbes

Implementation of Multistage version of the PCY algorithm. (2 stages)
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


# hash functions
def hash1(i, j):
    return (i * j) % numBuckets


def hash2(i, j):
    return (i + j) % numBuckets


itemsets = [i.strip().split() for i in open('RetailsDataset', 'r').readlines()]

percentChunk = 0.01
min_support = 0.05
numBuckets = 2000

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
countBuckets1 = [0] * numBuckets
countBuckets2 = [0] * numBuckets

for basket in itemsets:
    for item in C1:
        if item.issubset(basket):
            candidate = frozenset(item)
            if candidate not in count:
                count[candidate] = 1
            else:
                count[candidate] += 1
    pairs = list(combinations(basket, 2))
    for pair in pairs:
        listPair = list(pair)
        numbers = [int(x) for x in listPair]
        countBuckets1[hash1(numbers[0], numbers[1])] += 1

for i in range(0, len(countBuckets1) - 1):
    if countBuckets1[i] / len(itemsets) >= min_support:
        countBuckets1[i] = 1
    else:
        countBuckets1[i] = 0

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
# construct second hashmap
for basket in itemsets:
    pairs = list(combinations(basket, 2))
    for pair in pairs:
        listPair = list(pair)
        numbers = [int(x) for x in listPair]
        # if the pair hashes to frequent bucket in first hashmap and both values are frequent
        # hash the pair to the second hashmap
        if countBuckets1[hash1(numbers[0], numbers[1])] == 1 and numbers[0] in final and numbers[1] in final:
            countBuckets2[hash2(numbers[0], numbers[1])] += 1

for i in range(0, len(countBuckets2) - 1):
    if countBuckets2[i] / len(itemsets) >= min_support:
        countBuckets2[i] = 1
    else:
        countBuckets2[i] = 0

for basket in itemsets:
    pairs = list(combinations(basket, 2))
    for pair in pairs:
        listPair = list(pair)
        numbers = [int(x) for x in listPair]
        # if pair hashes to frequent buckets in both hashmaps and values are frequent add to pair candidates
        if countBuckets1[hash1(numbers[0], numbers[1])] == 1 and countBuckets2[hash2(numbers[0], numbers[1])] == 1 and numbers[0] in final and numbers[1] in final:
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
