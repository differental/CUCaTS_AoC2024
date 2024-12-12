height = [0] * int(1.3e7) # height[0] means "0.5"

max_height = 0

results = []

with open('q12.input.txt', 'r') as file:
    header_line = file.readline().strip()
    n = int(header_line.split()[0])

    for case in range(n):
        line = file.readline().strip()
        x, size = list(map(int, line.split()))
        
        ori_height = max(height[x:x+size])
        max_height = max(max_height, ori_height + size)
        results.append(max_height)
        
        for i in range(x, x + size):
            height[i] = ori_height + size
            
        print(case)
        
print(results)
print(sum(results))
        