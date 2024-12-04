import numpy as np
def parse_file(file_path):
    with open(file_path, 'r') as file:
        n = int(file.readline().strip())
        
        arrays = []
        for _ in range(n):
            line = file.readline().strip()
            array = list(map(int, line.split()))
            arrays.append(array)
        
    return n, arrays

n, arrays = parse_file('q3.input.txt')

res = 0

for case in range(n):

    new_arrays = [
            [int(item != 0) for item in arrays[case]],
            [int(item != 1) for item in arrays[case]],
            [int(item != 2) for item in arrays[case]]
            ]

    #print(new_arrays)

    m = len(new_arrays[0])
    #print(m)

    dp = np.full((m, 3), float('inf'))

    for j in range(3):
        if new_arrays[j][0] == 1 and new_arrays[j][m-1] == 1:
            dp[0][j] = 0

    val = []

    for start_point in range(3):
        if new_arrays[start_point][0] == 0:
            continue
        
        dp = np.full((m, 3), float('inf'))
        dp[0][start_point] = 0
                
        for i in range(1, m): # for each step
            for j in range(3): # at the relevant position
                if new_arrays[j][i]: # if it's landable
                    dp[i][j] = min(dp[i][j], dp[i-1][j]) # same cost as left

                    for j_prime in range(3):
                        if new_arrays[j_prime][i]:
                            dp[i][j_prime] = min(dp[i][j_prime], dp[i][j] + 1)
                            
        val.append(min(dp[m-1][start_point], min(dp[m-1]) + 1))
        

    #if case == 0:
        #print(dp)

    print(min(val))
    res += min(val)

print(res)
