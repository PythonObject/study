# coding: utf-8
import threading
import thread
import time


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

    def run(self):
        # 从写run函数，增加自己的代码到run中
        print 'Starting' + self.name
        print_time(self.name, self.counter)
        print 'Exiting' + self.name


    #创建两个线程
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

    #使用线程类创建和管理线程
    thread1 = myThread(1, 'Thread_1', 1)
    thread2 = myThread(2, 'Thread_2', 2)
    thread1.start()
    thread2.start()
    # print threading.current_thread

    while True:
        pass