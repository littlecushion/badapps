#coding=utf-8
import sys
reload(sys)
#python默认环境编码时ascii
sys.setdefaultencoding("utf-8")

import re;
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

def update_database(appid,result):
    try:
        connection = sqlite3.connect(database_filepath)
        cursor = connection.cursor()
        cursor.execute('update console_apps set isDetect = ?,result=? where id = ?',
                (True,result,appid,))
        connection.commit()
    except sqlite3.OperationalError:
        print("%s: Operational Error" % ("reDetect"))
    finally:
        connection.close()

def main():
    path='D:\\apptest\\appAutoTest\\text\\'+sys.argv[1]
    app_id=sys.argv[2]

    with open(path,'r') as f:
		test=f.read()
    # print test
    if re.match(r'[\s\S]*我们[\s\S]*',test):
    # if re.match(r'[\s\S]*阿富汗[\s\S]*',test):
        update_database(app_id,True)
    	# print 'OK'
    else:
        update_database(app_id,False)
    	# print 'failed'

    print 'successful'

if __name__ == '__main__':
	main()