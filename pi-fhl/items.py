from scrapy import Item, Field


class PoemItem(Item):
    tid = Field()
    title = Field()
    sentences = Field()
    author = Field()
