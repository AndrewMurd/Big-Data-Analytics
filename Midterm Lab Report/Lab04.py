"""
Andrew Murdoch and Andre Forbes

Implementation of Multistage version of the PCY algorithm. (2 stages)
"""

import time

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


# calculates the difference between two lists
def Diff(li1, li2):
    li_dif = [i for i in li1 + li2 if i not in li1 or i not in li2]
    return li_dif


def apriori(itemsets, percentChunk, min_support):
    C1 = []
    for basket in itemsets:
        for item in basket:
            if not [item] in C1:
                C1.append([item])
    C1 = [set(x) for x in C1]

    count = {}
    freq_itemSingle = []
    L1 = []

    for basket in itemsets:
        for item in C1:
            if item.issubset(basket):
                candidate = frozenset(item)
                if candidate not in count:
                    count[candidate] = 1
                else:
                    count[candidate] += 1

    for key in count:
        support = count[key] / len(itemsets)
        if support >= min_support:
            freq_itemSingle.insert(0, key)
            freq_itemSingle.insert(1, support)
            L1.insert(0, key)

    C2 = createCk(L1, 2)

    count = {}
    freq_itemDouble = []
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
            freq_itemDouble.insert(0, key)
            freq_itemDouble.insert(1, support)
            L2.insert(0, key)

    C3 = createCk(L2, 3)

    count = {}
    freq_itemTriple = []
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
            freq_itemTriple.insert(0, key)
            freq_itemTriple.insert(1, support)
            L3.insert(0, key)

    return L1, L2, L3


itemsets = [i.strip().split() for i in open('RetailsDataset', 'r').readlines()]

percentChunk = 0.2
min_support = 0.01

# divide item set sample into 2 chunks for SON implementation
itemsets = itemsets[:int(len(itemsets) * percentChunk)]
middle = int(len(itemsets) / 2)
itemsetOne = itemsets[:middle]
itemsetTwo = itemsets[middle:]
# change support value for both chunks appropriately
newMinSupp = min_support / 2
# get singles, pairs and triples for each chunk
singlesOne, doublesOne, triplesOne = apriori(itemsetOne, percentChunk, newMinSupp)
singlesTwo, doublesTwo, triplesTwo = apriori(itemsetTwo, percentChunk, newMinSupp)
# get singles, pairs and triples for whole item set
singles, doubles, triples = apriori(itemsets, percentChunk, min_support)
# get the union of both chunks results
UnionSingle = set(singlesOne + singlesTwo)
UnionDouble = set(doublesOne + doublesTwo)
UnionTriple = set(triplesOne + triplesTwo)

print("Frequent Values with false positives: ", UnionSingle, "\n")
print("Frequent Pairs with false positives: ", UnionDouble, "\n")
print("Frequent Triples with false positives: ", UnionTriple, "\n")
# get the number of false positives
numfalsePositivesSingle = len(Diff(list(UnionSingle), singles))
numfalsePositivesDoubles = len(Diff(list(UnionDouble), doubles))
numfalsePositivesTriples = len(Diff(list(UnionTriple), triples))

falsePositivesSingle = Diff(list(UnionSingle), singles)
falsePositivesDoubles = Diff(list(UnionDouble), doubles)
falsePositivesTriples = Diff(list(UnionTriple), triples)

print("Number of False Positives Single: ", numfalsePositivesSingle,
      "\nNumber of False Positives Doubles: ", numfalsePositivesDoubles,
      "\nNumber of False Positives Triples: ", numfalsePositivesTriples)
# output the results without false positives
print("Frequent Values: ", Diff(list(UnionSingle), falsePositivesSingle), "\n")
print("Frequent Pairs: ", Diff(list(UnionDouble), falsePositivesDoubles), "\n")
print("Frequent Triples: ", Diff(list(UnionTriple), falsePositivesTriples), "\n")

end = time.time()
print(f"Runtime of the program is {end - start}")
