import random
import sys
from operator import add, sub, mul

ops = [add, sub, mul]
ops_str = '+-x'

right = wrong = 0

while True:
    c = random.randint(1, len(ops_str))
    if c == 1:
        a = random.randint(1, 9)
        b = random.randint(1, 9)
        r = ops[c-1](a, b)
        if r <= 5:
            continue
    elif c == 2:
        a = random.randint(1, 19)
        b = random.randint(1, 19)
        r = ops[c-1](a, b)
    else:
        a = random.randint(1, 9)
        b = random.randint(1, 9)
        r = ops[c-1](a, b)

    op = ops_str[c-1]
    print(f'\n{a} {op} {b}')
    rs = f'{a} {op} {b} = {r}'
    try:
        s = input('=')
    except EOFError:
        print(f'\nright:{right}\nwrong:{wrong}\n')
        sys.exit(0)

    try:
        if int(s) == r:
            print(f'\b\033[92m{rs}\033[00m')
            right += 1
        else:
            print(f'\b\033[91m{rs}\033[00m')
            wrong += 1
    except:
        print(f'\b\033[91m{rs}\033[00m')
        wrong += 1
