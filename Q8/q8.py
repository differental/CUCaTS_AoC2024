# q8.input.txt is a modified version, changing Ln 20, Col 23 from '/' to '%'
# Answer: (20, 23)

from collections import deque

lines = []

with open('q8.input.txt', 'r') as file:
    for _ in range(48):
        lines.append(file.readline()[:-1])

node = (0, len(lines[0])-1, 0) # x, y, direction(0/1)
stack = []
pending_nodes = []
printing = False
remembered_location = (0, 0)

commands = []
try:
    count = 0
    while True:
        ch = lines[node[0]][node[1]]
        direction = node[2]
        #print(node, ch)
        #print(stack)
        
        commands.append(ch)
        
        if printing and ch != '"':
            print(ch, end="")
        else:
            match ch:
                case '*':
                    pass
                case '/':
                    direction = 0
                case '\\':
                    direction = 1
                case '^':
                    pending_nodes.append((node[0] + 1, node[1] + 1, 1))
                    direction = 0
                case '"':
                    printing = not printing
                case '{':
                    remembered_location = node
                case '}':
                    node = (remembered_location[0], remembered_location[1], direction)
                    continue
                case '~':
                    if len(pending_nodes):
                        node = pending_nodes.pop()
                        continue
                    else:
                        break
                case 'n':
                    print('\n', end="")
                case ':':
                    stack.append(stack[-1])
                case '%':
                    stack[-2], stack[-1] = stack[-1], stack[-2]
                case '+':
                    a = stack.pop()
                    b = stack.pop()
                    stack.append(a + b)
                case '-':
                    a = stack.pop()
                    b = stack.pop()
                    stack.append(b - a)
                case '?':
                    if stack[-1] == 0:
                        direction = 0
                    else:
                        direction = 1
                        stack[-1] -= 1
                case '$':
                    stack.pop()
                case 'A':
                    stack.append(10)
                case 'B':
                    stack.append(11)
                case 'C':
                    stack.append(12)
                case 'D':
                    stack.append(13)
                case 'E':
                    stack.append(14)
                case 'F':
                    stack.append(15)
                case '0':
                    stack.append(0)
                case '1':
                    stack.append(1)
                case '2':
                    stack.append(2)
                case '3':
                    stack.append(3)
                case '4':
                    stack.append(4)
                case '5':
                    stack.append(5)
                case '6':
                    stack.append(6)
                case '7':
                    stack.append(7)
                case '8':
                    stack.append(8)
                case '9':
                    stack.append(9)
                case '.':
                    print(format(stack[-1], 'X'), end="")
                    #print("Charr")
                case _:
                    pass

        #print(f"command: {ch}, stack: {stack}, location: {(node[0], node[1])}")
        count += 1
        #if count >= 500:
        #    break

        new_x = node[0] + 1
        new_y = node[1] + (-1 if direction == 0 else 1)

        node = (new_x, new_y, direction)

except:
    #print(commands)
    pass
