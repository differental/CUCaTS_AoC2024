from collections import defaultdict

def dfs(val, friends, next_naughty, naughty_kids):
    next_naughty.add(val)
    for friend in friends[val]:
        if friend not in next_naughty:
            if friend in naughty_kids:
                print(f"{friend} found")
            dfs(friend, friends, next_naughty, naughty_kids)
            
    return

def calculate_naughties(friends, naughty_kids):
    next_naughty = set()
    for naughty in sorted(naughty_kids):
        if naughty not in next_naughty:
            print(f"Navigating {naughty}.")
            val = len(next_naughty)
            dfs(naughty, friends, next_naughty, naughty_kids)
            print(f"Finished {naughty}, {len(next_naughty) - val} found.")
        else:
            print(f"{naughty} already navigated.")
    
    return next_naughty

friends = defaultdict(list)

with open('q10.input.txt', 'r') as file:  # Open the file in read mode
    header_line = file.readline().strip()
    n, m, k, c = map(int, header_line.split())
    header = (n, m, k, c)

    second_line = file.readline().strip()
    naughty_kids = set(list(map(int, second_line.split())))

    for line in file:
        x, y = map(int, line.strip().split())
        friends[x].append(y)
        friends[y].append(x)

removed = []

'''
for roundval in range(c):
    print(f"Round {roundval}")
    results = []
    
    val = len(calculate_naughties(friends, naughty_kids))
    
    min_val = val
    decision = 9999999
    
    for removed_kid in sorted(naughty_kids):
        temp_naughty_kids = naughty_kids.copy()
        temp_naughty_kids.remove(removed_kid)
        
        new_val = len(calculate_naughties(friends, temp_naughty_kids))
        print(f"Removing {removed_kid}: Impact {val - new_val} ({val} -> {new_val})")
        
        if new_val < min_val:
            min_val = new_val
            decision = removed_kid
            
    print(f"Decision: {decision}, Impact {val - min_val} ({val} -> {min_val})")
    
    naughty_kids.remove(decision)
    removed.append(decision)


removed.sort()
print(removed)
'''


calculate_naughties(friends, naughty_kids)
