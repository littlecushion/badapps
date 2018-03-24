#coding=utf-8
import sys
reload(sys)
#python默认环境编码时ascii
sys.setdefaultencoding("utf-8")

from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
# from scrapy import log
import logging
import scrapy

import sqlite3
from os import path
from android_apps_crawler import settings


class AppPipeline(object):
    def process_item(self, item, spider):
        # log.info("Catch an AppItem", level=log.INFO)
        # logging.warning("Catch an AppItem")
        logging.log(logging.INFO, "Catch an AppItem")
        return item

class SQLitePipeline(object):
    filename = ''
    conn = None
    def __init__(self):
        self.filename += settings.MARKET_NAME
        self.filename += ".db"
        self.filename = path.join(settings.DATABASE_DIR, self.filename)
        print self.filename
        self.conn = None
        dispatcher.connect(self.initialize, signals.engine_started)
        dispatcher.connect(self.finalize, signals.engine_stopped)

    def process_item(self, item, spider):
        try:
            cursor = self.conn.execute("select latestVersion from apps where name=?",(item['app_name'],))
            records = cursor.fetchall()
            # print 'OK'
            # print records[0]
            if  len(records)==0:
                self.conn.execute('insert into apps(url,name,type,description,size,latestVersion,updateTime) values(?,?,?,?,?,?,?)',
                        (item['url'],item['app_name'],item['app_type'],item['app_description'],item['app_size'],item['app_version'],item['app_time'],)
                    )
                self.conn.execute('insert into editions(name,version,updateTime,size,description) values(?,?,?,?,?)',
                        (item['app_name'],item['app_version'],item['app_time'],item['app_size'],item['app_versionInfo'],)
                    )
                self.conn.commit()
                logging.log(logging.INFO, "Inserting into database")
            elif  records[0]!=item['app_version']:
                self.conn.execute('update apps set url=?,type=?,description=?,size=?,latestVersion=?,updateTime=? where name=?',
                        (item['url'],item['app_type'],item['app_description'],item['app_size'],item['app_version'],item['app_time'],item['app_name'],)
                    )
                self.conn.execute('insert into editions(name,version,updateTime,size,description) values(?,?,?,?,?)',
                        (item['app_name'],item['app_version'],item['app_time'],item['app_size'],item['app_versionInfo'],)
                    )
                self.conn.commit()
                logging.log(logging.INFO, "Inserting into database")


            # size, item['app_size'],
            # # self.conn.commit()
            # self.conn.execute('insert into apps(name) values(?)',
            #             (item['app_name'],)
            #         )

            # self.conn.commit()
            # logging.log(logging.INFO, "Inserting into database")
        except sqlite3.IntegrityError:
            print "Duplicated"
        return item

    def initialize(self):
        if path.exists(self.filename):
            self.conn = sqlite3.connect(self.filename)
        else:
            self.create_table()
        self.conn.execute("PRAGMA journal_mode=WAL;")
        self.conn.commit()

    def finalize(self):
        if self.conn is not None:
            self.conn.commit()
            self.conn.close()
            self.conn = None

    def create_table(self):
        self.conn = sqlite3.connect(self.filename)
        self.conn.execute("create table apps( \
                id integer primary key autoincrement, \
                name nvarchar(50) default 'none',\
                type nvarchar(50) default 'none',\
                size nvarchar(50) default 'none',\
                latestVersion varchar(50) default 'none', \
                updateTime varchar(50) default 'none', \
                url varchar(100) not null unique, \
                description nvarchar(500) default 'none',\
                downloaded int default 0)"
            )
        self.conn.execute("create table editions( \
                id integer primary key autoincrement, \
                name nvarchar(50) default 'none',\
                version varchar(50) default 'none', \
                updateTime varchar(50) default 'none', \
                size nvarchar(50) default 'none',\
                description nvarchar(500) default 'none')"
            )
        self.conn.commit()
