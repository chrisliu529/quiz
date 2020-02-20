import pymongo
import re
import time


client = pymongo.MongoClient('mongodb://root:example@mongo')
db = client['local']
pattern_title = re.compile(r'^卷[0-9]+_[0-9]+')
pattern_mixed = re.compile(r'^(.*)(卷[0-9]+_[0-9]+.*)')


def flat_list(l):
    return [item for sublist in l for item in sublist]


def is_title(s):
    return bool(pattern_title.match(s))


def preprocess(text):
    lines = text.split('\n')
    res = []
    for line in lines:
        if '卷' in line and '_' in line and not is_title(line):
            t = pattern_mixed.search(line)
            res.append(t.group(1).strip())
            res.append(t.group(2).strip())
        else:
            res.append(line)
    return '\n'.join(res)


def process(text):
    def has_letter(s):
        for c in s:
            if c.islower() or c.isupper():
                return True
        return False

    def split_sentences(ss):
        ss1 = [s.replace('.', '。').split('。') for s in ss]
        return [s for s in flat_list(ss1) if s != '' and not has_letter(s)]

    lines = text.split('\n')
    lines2 = [x.strip() for x in lines]
    lines3 = [x for x in lines2 if x != '']
    lines3.append('end')

    pattern = re.compile(r'^卷(.*)「(.*)」(.*)')
    st = 'find-title'
    ps = []
    last = None
    ss = None
    inst = {}
    i = 0
    while i < len(lines3):
        line = lines3[i]
        if st == 'find-title':
            if last is not None and not inst.get(last['tid'], False):
                ps.append(last)
                inst[last['tid']] = True
            if line == 'end':
                break
            if is_title(line):
                t = pattern.search(line)
                last = {
                    'tid': t.group(1).strip(),
                    'title': t.group(2).strip(),
                    'author': t.group(3).strip()
                }
                st = 'find-sentenses'
                ss = []
        elif st == 'find-sentenses':
            if is_title(line):
                st = 'find-title'
                last['sentences'] = split_sentences(ss)
                continue
            ss.append(line)
        i += 1
    return ps


def main():
    for doc in db['raw'].find():
        poems = process(preprocess(doc['data']))
        for p in poems:
            db['extract'].insert_one(p)


def cms():
    return int(round(time.time() * 1000))


if __name__ == "__main__":
    t0 = cms()
    main()
    t = cms() - t0
    print(f'cost: {t} ms')
