import random
import pymongo


random.seed()
materials = {}
used = set()
ntab = '零一二三四五六七八九'

client = pymongo.MongoClient('mongodb://root:example@mongo')
db = client['local']


def prepare_materials():
    def has_letter(s):
        for c in s:
            if c.islower() or c.isupper():
                return True
        return False

    for doc in db['poems'].find():
        ss = [s for s in doc['sentences'] if not s.endswith('，') and not has_letter(s)]
        for n in ntab:
            for s in ss:
                if n in s:
                    materials.setdefault(n, []).append(f'{s};{doc["title"]}')

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
    print('''
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
            return
        fields = s.split(';')
        rid = f'<span style="font-size:14px">#{i+1}</span>'
        title = f'<span style="color:gray;font-size:12px"><i>《{fields[1]}》</i></span>'
        marked = mark_number(fields[0], n)
        print(f'{rid} {marked} {title} <br>')
    print('''
    </body>
</html>
    ''')


if __name__ == "__main__":
    main()
