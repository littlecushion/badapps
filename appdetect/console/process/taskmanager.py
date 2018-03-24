#!/usr/bin/env python
# -*- coding: utf-8 -*-

'分布式进程 -- 服务器端'

import time,random, multiprocessing,threading
from multiprocessing.managers import BaseManager
from multiprocessing import freeze_support


# 从BaseManager继承的QueueManager:
class QueueManager(BaseManager):
    pass


# 发送任务的队列:
task_queue = multiprocessing.Queue()
# 接收结果的队列:
result_queue = multiprocessing.Queue()

# 为解决__main__.<lambda> not found问题
def get_task_queue():
    return task_queue

# 为解决__main__.<lambda> not found问题
def get_result_queue():
    return result_queue


# 把两个Queue都注册到网络上, callable参数关联了Queue对象:
QueueManager.register('get_task_queue', callable=get_task_queue)
QueueManager.register('get_result_queue', callable=get_result_queue)
# 绑定端口5000, 设置验证码'abc':
manager = QueueManager(address=('127.0.0.1', 5000), authkey='abc')


    # 放几个任务进去:
def put_task():
    for i in range(10):
        n = random.randint(0, 10000)
        print('Put task %d...' % n)
        task.put(n)

    # 从result队列读取结果:
def get_result():
    print('Try get results...')
    for i in range(10):
        # r = result.get(timeout=10)
        r = result.get()
        print('Result: %s' % r)

if __name__ == '__main__':
    freeze_support()
    # 启动Queue:
    manager.start()

    # 获得通过网络访问的Queue对象:
    task = manager.get_task_queue()
    result = manager.get_result_queue()

    # 创建两个线程，一个发数据，一个收数据
    t1 = threading.Thread(target=put_task, name='put_task_thread')
    t2 = threading.Thread(target=get_result, name='get_result_thread')
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    # 关闭:
    time.sleep(10)
    manager.shutdown()