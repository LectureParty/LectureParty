from Collections import Counter

def scheduler(bigArray, cnt=None):
    if cnt == None:
        cnt = Counter()
    for i in bigArray:
        if i != 0:
            for j in bigArray[i]:
                cnt[(i, j)] += 1
    return cnt.most_common();