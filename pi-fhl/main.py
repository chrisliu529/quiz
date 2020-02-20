import random
import time
import sys

import pymongo


random.seed()
materials = {}
used = set()
ntab = '零一二三四五六七八九'

client = pymongo.MongoClient('mongodb://root:example@mongo')
db = client['local']
outf = open(sys.argv[1], 'w')


def prepare_materials():
    for doc in db['extract'].find():
        for n in ntab:
            for s in doc['sentences']:
                if n in s:
                    materials.setdefault(n, []).append(f'{s};{doc["title"]};{doc["author"]}')

    for k in materials:
        random.shuffle(materials[k])


def get_sentence(n):
    s = materials[n]
    try:
        while True:
            res = s.pop()
            if res in used:
                continue
            used.add(res)
            return res
    except:
        return None


def read_pi():
    with open('pi1000.txt') as f:
        return ''.join(f.read().split('\n'))


def mark_number(s, n):
    mark = f'<span style="color:red;font-size:18px"><b>{n}</b></span>'
    return s.replace(n, mark)

def main():
    outf.write('''
    <!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>白居易版圆周率飞花令</title>
</head>

<body>
    ''')
    prepare_materials()
    numbers = read_pi()
    for i in range(len(numbers)):
        n = ntab[int(numbers[i])]
        s = get_sentence(n)
        if s is None:
            print(f'broken on {n}')
            break
        fields = s.split(';')
        rid = f'<span style="font-size:14px">#{i+1}</span>'
        title = f'<span style="color:gray;font-size:12px"><i>《{fields[1]}》 {fields[2]}</i></span>'
        marked = mark_number(fields[0], n)
        outf.write(f'{rid} {marked} {title} <br>')
    outf.write('''
    </body>
</html>
    ''')
    outf.close()


def cms():
    return int(round(time.time() * 1000))


if __name__ == "__main__":
    t0 = cms()
    main()
    t = cms() - t0
    print(f'cost: {t} ms')
