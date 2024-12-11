times = []

with open('q11.input.txt', 'r') as file:
    line = file.readline().strip()
    [d, n] = list(map(int, line.split()))
    
    for _ in range(n):
        line = file.readline().strip()
        [name, vnorm, vturbo, cooldown, duration] = line.split()
        [vnorm, vturbo, cooldown, duration] = map(int, [vnorm, vturbo, cooldown, duration])
        
        cycle_d = vturbo * duration + vnorm * cooldown
        cycles = d // cycle_d
        cycled_time = cycles * (duration + cooldown)
        remaining_d = d % cycle_d
        
        turbo_d = vturbo * duration
        if remaining_d <= turbo_d:
            remaining_time = remaining_d / vturbo
        else:
            remaining_time = duration + (remaining_d - turbo_d) / vnorm
        
        times.append((cycled_time + remaining_time, name))
        
times = sorted(times)
names = [times[i][1] for i in range(3)]
print(','.join(names))
