arrays = []

with open('q5.input.txt', 'r') as file:
    n = int(file.readline().strip())
    
    arrays = []
    for _ in range(n):
        line = file.readline().strip()
        num = int(line)
        line = file.readline().strip()
        array = list(map(int, line.split()))
        arrays.append((num, array))

count = 0

for (num, array) in arrays:
    while True:
        newarr = []
        i = 0
        
        while i < len(array) - 1:
            if array[i] > 0 and array[i+1] < 0:
                if abs(array[i]) > abs(array[i+1]):
                    newarr.append(array[i])
                elif abs(array[i]) < abs(array[i+1]):
                    newarr.append(array[i+1])
                i += 1
            else:
                newarr.append(array[i])
                
            i += 1

        if i == len(array) - 1:
            newarr.append(array[-1])
            
        if newarr == array:
            break
        
        array = newarr
        
    #print(num - len(newarr))
    count += (num - len(newarr))

print(count)