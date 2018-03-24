#coding=utf-8
import sys
reload(sys)
#python默认环境编码时ascii
sys.setdefaultencoding("utf-8")

import re

from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.http import HtmlResponse
import logging
import scrapy
import chardet

from urlparse import urlparse
from urlparse import urljoin

from android_apps_crawler.items import AppItem
from android_apps_crawler import settings
from android_apps_crawler import custom_parser

class AndroidAppsSpider(Spider):
    name = "android_apps_spider"
    scrape_rules = settings.SCRAPE_RULES

    def __init__(self, market=None, database_dir="../repo/databases/", *args, **kwargs):
        super(AndroidAppsSpider, self).__init__(*args, **kwargs)
        self.allowed_domains = settings.ALLOWED_DOMAINS[market]
        self.start_urls = settings.START_URLS[market]
        settings.MARKET_NAME = market
        settings.DATABASE_DIR = database_dir

    def parse(self, response):
        response_domain = urlparse(response.url).netloc
        appItemList = []
        cookie = {}
        xpath_rule = self.scrape_rules['xpath']
        for key in xpath_rule.keys():
            if key in response_domain:
                appItemList.extend(
                        # self.parse_xpath(response, xpath_rule[key]))
                        self.parse_xpath(response, xpath_rule[key],key))
                break
        custom_parser_rule = self.scrape_rules['custom_parser']
        for key in custom_parser_rule.keys():
            if key in response_domain:
                appItemList.extend(
                        getattr(custom_parser, custom_parser_rule[key])(self,response,key)
                        )
                break
        #if "appchina" in response_domain:
        #    xpath = "//a[@id='pc-download' and @class='free']/@href"
        #    appItemList.extend(self.parse_xpath(response, xpath))
        sel = Selector(text=response.body)
        for url in sel.xpath('//a/@href').extract(): #extract()：返回一个unicode字符串，该字符串为XPath选择器返回的数据
            url = urljoin(response.url, url)
            # print url
            yield Request(url, meta=cookie, callback=self.parse)

        for item in appItemList:
            yield item


    def parse_xpath(self, response, xpath,key):
        appItemList = []
        name_xpath_rule = self.scrape_rules['name_xpath']
        type_xpath_rule = self.scrape_rules['type_xpath']
        size_xpath_rule = self.scrape_rules['size_xpath']
        description_xpath_rule = self.scrape_rules['description_xpath']
        version_xpath_rule = self.scrape_rules['version_xpath']
        time_xpath_rule = self.scrape_rules['time_xpath']
        versionInfo_xpath_rule = self.scrape_rules['versionInfo_xpath']
        sel = Selector(text=response.body)
        for url in sel.xpath(xpath).extract():
            url = urljoin(response.url, url)
            # log.info("Catch an application: %s" % url, level=log.INFO)
            # self.logger.info("Catch an application: %s",url)
            appItem = AppItem()            
            appItem['url'] = url
            # appItemList.append(appItem)
            # appItem['app_name'] = sel.xpath(name_xpath_rule[key]).extract()[0]
            app_name = ''.join(sel.xpath(name_xpath_rule[key]).extract())
            appItem['app_name'] = ''.join(app_name.split())
            # print isinstance(appItem['app_name'], unicode) 
            # # app_name.encode("utf-8")
            # print appItem['app_name']
            app_type = ''.join(sel.xpath(type_xpath_rule[key]).extract())
            appItem['app_type'] = ''.join(app_type.split())
            # app_size = ''.join(sel.xpath(size_xpath_rule[key]).extract())
            # appItem['app_size'] = ''.join(app_size.split())
            app_description = ''.join(sel.xpath(description_xpath_rule[key]).extract()).replace('<br />','')
            appItem['app_description'] = ''.join(app_description.split())

            app_size = ''.join(sel.xpath(size_xpath_rule[key]).extract())
            appItem['app_size'] = ''.join(app_size.split())
            app_version = ''.join(sel.xpath(version_xpath_rule[key]).extract())
            appItem['app_version'] = ''.join(app_version.split())
            app_time = ''.join(sel.xpath(time_xpath_rule[key]).extract())
            appItem['app_time'] = ''.join(app_time.split())
            app_versionInfo = ''.join(sel.xpath(versionInfo_xpath_rule[key]).extract()).replace('<br />','')
            appItem['app_versionInfo'] = ''.join(app_versionInfo.split())

            appItemList.append(appItem)                
        return appItemList


    # def parse_anzhi(self, response, xpath):
    #    appItemList = []
    #    hxs = HtmlXPathSelector(response)
    #    for script in hxs.select(xpath).extract():
    #        id = re.search(r"\d+", script).group()
    #        url = "http://www.anzhi.com/dl_app.php?s=%s&n=5" % (id,)
    #        appItem = AppItem()
    #        appItem['url'] = url
    #        appItemList.append(appItem)
    #    return appItemList


