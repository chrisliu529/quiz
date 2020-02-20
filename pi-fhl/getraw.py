import os
import re
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy import Spider
from items import RawItem


class PoemsSpider(Spider):
    name = "poems"
    start_urls = [f'https://www.shigeku.org/xlib/lingshidao/gushi/tangshi/qts_{i:04d}.htm' for i in range(1, 889)]

    def parse(self, response):
        div_text = ''.join(response.css('body > div:nth-child(4)::text').getall())
        yield RawItem(
            url = response.url,
            data = div_text
        )


def main():
    os.environ.setdefault('SCRAPY_SETTINGS_MODULE', 'settings')
    process = CrawlerProcess(get_project_settings())
    process.crawl(PoemsSpider)
    process.start()


if __name__ == "__main__":
    main()
