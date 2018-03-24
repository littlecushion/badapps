#!/usr/bin/env python
# encoding: utf-8
import sys
import threading
import sqlite3
import time
import urllib2
import os
import hashlib
import signal
import Queue
import shutil

database_filepath= "D:\\appdetect\\db.sqlite3"
output_dir = "D:\\apptest\\appAutoTest\\downloadApk\\apps\\"

def get_undownloaded_url(appid):
    app_id=appid
    try:
        connection = sqlite3.connect(database_filepath)
        cursor = connection.cursor()
        filter_sql = "select * from console_apps where id=%s"%app_id
        cursor.execute(filter_sql)
        records = cursor.fetchall()
        for r in records:
            undownloaded_url = r[4] 
        return undownloaded_url
    except sqlite3.OperationalError:
        print("get_undownloaded_url(): Operational Error.")
    finally:
        connection.close()
    


def downloading(undownloaded_url):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    # if not os.path.exists(temp_dir):
    #     os.makedirs(temp_dir)
    f = urllib2.urlopen(undownloaded_url) 
    filename = os.path.basename(f.url)
    print output_dir+filename
    if not os.path.exists(output_dir+filename):
        with open(output_dir+filename, "wb") as code:
            code.write(f.read()) 
    return filename

def update_database(appid,filename):
    try:
        connection = sqlite3.connect(database_filepath)
        cursor = connection.cursor()
        cursor.execute('update console_apps set isDownloaded = ?,appFileName=? where id = ?',
                (True, filename, appid,))
        connection.commit()
    except sqlite3.OperationalError:
        print("%s: Operational Error" % ("Downloader"))
    finally:
        connection.close()

def main():
    url=get_undownloaded_url(1)
    downloading(url)
    update_database(1)


if __name__ == '__main__':
    main()
