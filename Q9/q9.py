from collections import defaultdict
import math

array = []

with open('q9.input.txt', 'r') as file:
    line = file.readline().strip()
    array = list(map(int, line.split()))


count = 0
jobs = defaultdict(int)

for item in array:
    jobs[item] += 1

elf_count = 0
    
for job in jobs:
    elf_count += math.ceil(jobs[job] / (job + 1)) * (job + 1)
    
print(elf_count)
