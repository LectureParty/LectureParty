from collections import Counter

def scheduler(bigArray, cnt=None):
    if cnt == None:
        cnt = Counter()
    for i in range(len(bigArray)):
        if bigArray[i] != 0:
            for j in range(len(bigArray[i])):
                cnt[(i, j)] += 1
    return cnt