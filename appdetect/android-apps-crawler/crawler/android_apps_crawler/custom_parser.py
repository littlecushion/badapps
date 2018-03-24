import re

from scrapy.selector import Selector
from android_apps_crawler.items import AppItem

def parse_anzhi(self,response,key):
    xpath = "//div[@class='detail_down']/a/@onclick"
    appItemList = []
    name_xpath_rule = self.scrape_rules['name_xpath']
    type_xpath_rule = self.scrape_rules['type_xpath']
    size_xpath_rule = self.scrape_rules['size_xpath']
    description_xpath_rule = self.scrape_rules['description_xpath']
    sel = Selector(text=response.body)
    for script in sel.xpath(xpath).extract():
        id = re.search(r"\d+", script).group()
        url = "http://www.anzhi.com/dl_app.php?s=%s&n=5" % (id,)
        appItem = AppItem()
        appItem['url'] = url
        # appItemList.append(appItem)
        app_name = ''.join(sel.xpath(name_xpath_rule[key]).extract())
        appItem['app_name'] = ''.join(app_name.split())
        app_type = ''.join(sel.xpath(type_xpath_rule[key]).extract())
        appItem['app_type'] = ''.join(app_type.split())
        app_size = ''.join(sel.xpath(size_xpath_rule[key]).extract())
        appItem['app_size'] = ''.join(app_size.split())
        app_description = ''.join(sel.xpath(description_xpath_rule[key]).extract()).replace('<br />','')
        appItem['app_description'] = ''.join(app_description.split())
        appItemList.append(appItem)
    return appItemList

