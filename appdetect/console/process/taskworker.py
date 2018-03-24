# -*- coding:utf-8 -*-
# taskworker.py

import time, sys, Queue
from multiprocessing.managers import BaseManager
from multiprocessing import Process,Pool
import os,random

# 创建类似的QueueManager:
class QueueManager(BaseManager):
    pass

# 由于这个QueueManager只从网络上获取Queue，所以注册时只提供名字:
QueueManager.register('get_task_queue')
QueueManager.register('get_result_queue')


def connect_server():
	# 连接到服务器，也就是运行taskmanager.py的机器:
	server_addr = '127.0.0.1'
	print('Connect to server %s...' % server_addr)
	# 端口和验证码注意保持与taskmanager.py设置的完全一致:
	m = QueueManager(address=(server_addr, 5000), authkey='abc')
	# 从网络连接:
	m.connect()
	return m


def process(name):
	m=connect_server()
	# 获取Queue的对象:
	task = m.get_task_queue()
	result = m.get_result_queue()
	# 从task队列取任务,并把结果写入result队列:
	while True:
	    try:
	        n = task.get(timeout=3)
	        # n = task.get()
	        print('run task%d %d * %d...' % (name,n, n))
	        r = '%d * %d = %d' % (n, n, n*n)
	        time.sleep(1)
	        result.put(r)
	    except Queue.Empty:
	        print('task queue is empty.')
	        sys.exit(0)
	    except EOFError:
	    	print "Connection has been disconnected"
	    	sys.exit(0)
	    except KeyboardInterrupt:
	        print "User aborted."
	        sys.exit(0)


if __name__ == '__main__':
	# m=connect_server()
	# # 获取Queue的对象:
	# task = m.get_task_queue()
	# result = m.get_result_queue()

	# #多进程，创建进程池管理所有进程
	# p = Pool()

	# for i in range(4):
	# 	p.apply_async(process, args=(i,))

	# print 'Waiting for all subprocesses done...'
	# p.close()
	# p.join()
	# print 'All subprocesses done.'

	# # 处理结束:
	# print('worker exit.')

	# 分别创建两个进程进行运行
	p1 = Process(target=process, args=(1,))
	p2 = Process(target=process, args=(2,))	
	print 'Process will start.'
	p1.start()
	p2.start()
	p1.join()
	p2.join()
	print 'Process end.'



