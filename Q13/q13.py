from collections import defaultdict
import copy

def dfs(val, friends, next_naughty, naughty_kids):
    next_naughty.add(val)
    for friend in friends[val]:
        if friend not in next_naughty:
            #if friend in naughty_kids:
            #print(f"{friend} found")
            dfs(friend, friends, next_naughty, naughty_kids)
            
    return

def calculate_naughties(friends, naughty_kids):
    next_naughty = set()
    for naughty in sorted(naughty_kids):
        if naughty not in next_naughty:
            #print(f"Navigating {naughty}.")
            val = len(next_naughty)
            dfs(naughty, friends, next_naughty, naughty_kids)
            #print(f"Finished {naughty}, {len(next_naughty) - val} found.")
        #else:
            #print(f"{naughty} already navigated.")
    
    return next_naughty

friends = defaultdict(list)

with open('q13.input.txt', 'r') as file:  # Open the file in read mode
    header_line = file.readline().strip()
    n, m, k = map(int, header_line.split())

    second_line = file.readline().strip()
    naughty_kids = set(list(map(int, second_line.split())))

    for line in file:
        x, y = map(int, line.strip().split())
        friends[x].append(y)
        friends[y].append(x)


results = []

for i in range(n):
    # try removing this kid
    
    #print(f"Calculating {i}")
    
    naughty_kids_copy = copy.deepcopy(naughty_kids)
    #print(f"Naughty kids length {len(naughty_kids_copy)}")
    
    if i in naughty_kids_copy:
        naughty_kids_copy.remove(i)
    #print(f"Naughty kids length {len(naughty_kids_copy)}")
    
    friends_copy = copy.deepcopy(friends)
    
    for item in friends_copy[i]:
        friends_copy[item].remove(i)
        #print(f"Removed friendship {i} <-> {item}")
        
    friends_copy[i] = []

    results.append((len(calculate_naughties(friends_copy, naughty_kids_copy)), i))
    
results.sort()
print(results[0])
