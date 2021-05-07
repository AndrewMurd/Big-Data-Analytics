"""
Andrew Murdoch and Andre Forbes

Implementation of Apriori algorithm for frequent pairs and triples.
"""

import time

start = time.time()


# create size k combinations
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


# open dataset and create data array
itemsets = [i.strip().split() for i in open('RetailsDataset', 'r').readlines()]

percentChunk = 0.01    # dataset chunk (0.2 = 20% of data)
min_support = 0.05      # minimum support value

itemsets = itemsets[:int(len(itemsets) * percentChunk)]
# create single candidates
C1 = []
for basket in itemsets:
    for item in basket:
        if not [item] in C1:
            C1.append([item])
C1 = [set(x) for x in C1]

count = {}
freq_item = []
L1 = []
# count number of occurrences of each candidate
for basket in itemsets:
    for item in C1:
        if item.issubset(basket):
            candidate = frozenset(item)
            if candidate not in count:
                count[candidate] = 1
            else:
                count[candidate] += 1
# check if candidate meets minimum support requirement
for key in count:
    support = count[key] / len(itemsets)
    if support >= min_support:
        freq_item.insert(0, key)
        freq_item.insert(1, support)
        L1.insert(0, key)

print("Frequent Items: ", freq_item, "\n")

# create pair candidates
C2 = createCk(L1, 2)

count = {}
freq_items = []
L2 = []

for basket in itemsets:
    for item in C2:
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

print("Frequent Pairs: ", freq_items, "\n")

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

print("Frequent Triples: ", freq_items, "\n")

end = time.time()
# print runtime of program
print(f"Runtime of the program is {end - start}")
