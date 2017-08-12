# coding: utf-8
import threading
import thread
import time

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


class my_thread():
    def __int__(self):
        start_thread().clone()


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

    str = 'test'
    print str.upper()
    # print threading.current_thread
    start_thread()
    # start_thread()
    # a = my_thread()
    # b = my_thread()
    while True:

        pass