# coding: utf-8
import threading
from multiprocessing import Process, Queue
import time
import os
# """
# When you use python manage.py runserver Django start two processes, one for the actual development server and other
# to reload your application when the code change
#
# You can test it importing os inside your AppConfig class and print the process id inside the ready function like so:
#
# import os
#
# class SomeAppConfig(AppConfig):
#     name = 'some_app'
#
#     def ready(self):
#         print(os.getpid())
#
# You will see it prints two different processes
#
# You can also start the server without the reload option, and you will see only one process running (and your code
# print("Redefined ready method in some_app") will only be executed once):
#
# python manage.py runserver --noreload
#
# https://stackoverflow.com/questions/37441564/redefinition-of-appconfig-ready
# """


# 为线程定义一个函数
def print_time(thread_name, delay):
    count = 0
    while count < 5:
        time.sleep(delay)
        count += 1
        print '%s: %s' % (thread_name, time.ctime(time.time()))


class myThread(threading.Thread):
    def __init__(self, thread_id, name, counter):

        threading.Thread.__init__(self)
        # super(myThread, self).__init__(self)
        self.thread_id = thread_id
        self.name = name
        self.counter = counter
        # lock.release()

    def run(self):
        # 从写run函数，增加自己的代码到run中
        print 'Starting' + self.name
        print_time(self.name, self.counter)
        print 'Exiting' + self.name


def start_thread():
    thread1 = myThread(1, 'Thread_1', 1)
    thread2 = myThread(2, 'Thread_2', 2)
    thread1.start()
    thread2.start()


def my_process(process_name, queue_up, queue_down):
    """my process"""

    pid = os.getpid()
    print "process_name:%s, process_id:%d" % (process_name, pid)
    queue_up.put(pid)

    while True:
        # 进程接收和处理从其他进程发过来的消息
        if queue_down.empty() is True:
            # print "receive not msg"
            pass
        else:
            msg_receive = queue_down.get()
            print "process pid=%d receive msg: %s" % (pid, msg_receive)
            queue_up.put_nowait(msg_receive)
            print "put msg back"
        time.sleep(0.5)

if __name__ == '__main__':
    # 使用简单线程接口创建线程
    # print 'multi_progress test function'
    # try:
    #     thread.start_new_thread(print_time, ('Thread-1', 2, ))
    #     thread.start_new_thread(print_time, ('Thread-2', 4, ))
    # except:
    #     print 'Error: unable to start thread'
    #
    # while 1:
    #     pass

    # 使用线程类创建和管理线程

    # print threading.current_thread
    # start_thread()
    # start_thread()
    # a = my_thread()
    # b = my_thread()

    msg_channal = {}
    for count in range(0, 5, 1):
        # 创建进程和通信通道
        msg_queue = {}
        queue_up = Queue()
        queue_down = Queue()
        msg_queue['queue_up'] = queue_up
        msg_queue['queue_down'] = queue_down
        print "queue_up_id:%d, queue_down_id:%d" % (id(queue_up), id(queue_down))
        new_process = Process(target=my_process, args=('process_' + str(count), queue_up, queue_down))
        new_process.start()
        # time.sleep(1)
        new_process_pid = queue_up.get()
        print "process_%d pid:%d" % (count, new_process_pid)
        msg_queue['pid'] = new_process_pid
        msg_queue['handle'] = new_process
        msg_channal['process_' + str(count)] = msg_queue

    time.sleep(2)
    for channal_key in msg_channal.keys():
        print msg_channal[channal_key]
    while True:
        for channal_key in msg_channal.keys():
            # 和进程通信
            if msg_channal[channal_key]['handle'].is_alive() is False:
                print "process pid=%d is not alive" % (msg_channal[channal_key]['pid'])
                continue
            msg_channal[channal_key]['queue_down'].put("msg for queue_%d" % (msg_channal[channal_key]['pid']))
            time.sleep(0.5)
            queue_channal = msg_channal[channal_key]['queue_up']
            msg = queue_channal.get()
            print "main process receive msg process pid=%d: %s" % (msg_channal[channal_key]['pid'], msg)
            # time.sleep(1)
        pass