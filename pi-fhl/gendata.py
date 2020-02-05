import os
import re
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy import Spider
from items import PoemItem


def flat_list(l):
    return [item for sublist in l for item in sublist]


def process(text):
    def is_title(s):
        return '卷' in s and '_' in s or s == 'end'

    def split_sentences(ss):
        ss1 = [s.replace('.', '。').split('。') for s in ss]
        return [s for s in flat_list(ss1) if s != '']

    lines = text.split('\n')
    lines2 = [x.strip() for x in lines]
    lines3 = [x for x in lines2 if x != '']
    lines3.append('end')

    pattern = re.compile(r'^卷(.*)「(.*)」')
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
                    'title': t.group(2).strip()
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


class PoemsSpider(Spider):
    name = "poems"
    start_urls = [f'https://www.shigeku.org/xlib/lingshidao/gushi/tangshi/qts_0{i}.htm' for i in range(424, 463)]

    def parse(self, response):
        div_text = ''.join(response.css('body > div:nth-child(4)::text').getall())
        poems = process(div_text)
        for p in poems:
            yield PoemItem(
                tid = p['tid'],
                title = p['title'],
                sentences = p['sentences'],
                author = '白居易'
            )


def main():
    os.environ.setdefault('SCRAPY_SETTINGS_MODULE', 'settings')
    process = CrawlerProcess(get_project_settings())
    process.crawl(PoemsSpider)
    process.start()


if __name__ == "__main__":
    main()
