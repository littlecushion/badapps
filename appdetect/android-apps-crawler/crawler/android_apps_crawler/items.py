from scrapy.item import Item, Field

class AppItem(Item):
    url = Field()
    app_name = Field()
    app_type = Field()
    app_size = Field()
    app_description = Field()
    app_version = Field()
    app_time = Field()
    app_versionInfo = Field()
