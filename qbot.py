import random

def add(a, b):
    return a + b

def sub(a, b):
    return a - b

ops = [add, sub]
ops_str = '+-'

while True:
    c = random.randint(1, len(ops_str))
    if c == 1:
        a = random.randint(1, 9)
        b = random.randint(1, 9)
        r = ops[c-1](a, b)
        if r <= 5:
            continue
    else:
        a = random.randint(1, 19)
        b = random.randint(1, 19)
        r = ops[c-1](a, b)

    print '\n%s %s %s' % (a, ops_str[c-1], b)
    raw_input()
    print '\b%s %s %s = %s' % (a, ops_str[c-1], b, r)
