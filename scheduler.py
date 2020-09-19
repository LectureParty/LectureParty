from Collections import Counter

def scheduler(num_meetings, times):
    cnt = Counter()
    for time in times:
        cnt[time] += 1
    return cnt.most_common(num_meetings)