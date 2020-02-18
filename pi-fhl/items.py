from scrapy import Item, Field


class RawItem(Item):
    url = Field()
    data = Field()
