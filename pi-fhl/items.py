from scrapy import Item, Field


class RawItem(Item):
    url = Field()
    data = Field()


class PoemItem(Item):
    tid = Field()
    title = Field()
    sentences = Field()
    author = Field()
