# coding: utf-8
# file name: multi_thread.py
# python version: 2.7
# author: wu ming ming
# description: study of multi thread


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


class Message():
    """class"""
    def __init__(self):
        self.s_pid = 0
        self.s_pn = ""
        self.d_pid = 0
        self.d_pn = ""
        self.method = "PUT"
        self.command = 0
        self.payload = None

    def get_payload(self):
        return self.payload

    def get_source(self):
        return self.s_pn, self.s_pid

    def get_destination(self):
        return self.d_pn, self.d_pid

    def get_method(self):
        return self.method

    def get_command(self):
        return self.command


class MessageProcess():
    """process message"""

    def __init__(self, process_name, process_id, queue_in, queue_out, call_back):
        """init"""
        self.process_id = process_id
        self.process_name = process_name
        self.msg_queue_in = queue_in
        self.msg_queue_out = queue_out
        self.msg_in_count = 0
        self.msg_out_count = 0
        # 与本进程相连的其他进程，只能和列表中的进程相通信
        self.process_link_info = {}

        # 回调函数，在调用获取消息接口后会调用回调函数进行处理
        self.call_back = call_back

        self.message_send = Message()
        self.message_receive = Message()

    def add_process_link(self, process_name, process_id, queue_in, queue_out):
        """add process link"""

        if process_name in self.process_link_info:
            return False, "process_name in link"

        for pro in self.process_link_info:
            if self.process_link_info[pro]['process_id'] == process_id:
                return False, "process_id in link"

        new_link = None
        new_link[process_name] = {
            'process_id': process_id,
            'queue_in': queue_in,
            'queue_out': queue_out,
            'msg_send_count': 0,
            'msg_receive_count': 0
        }

        self.process_link_info[process_name] = new_link
        return True, "process link add success"

    def del_process_link(self, *agr):

        if isinstance(type(agr), type(1)) is True:
            for pro in self.process_link_info:
                if agr == self.process_link_info[pro]['process_id']:
                    del self.process_link_info[pro]
        if isinstance(type(agr), type("")) is True:
            if agr in self.process_link_info:
                del self.process_link_info[agr]
        return True

    def send_msg(self, process_name, method, command, data):
        """send msg"""
        for pro in self.process_link_info:
            if process_name == self.process_link_info:
                self.message_send.d_pid = self.process_link_info[pro]
                self.message_send.d_pn = process_name
                self.message_send.s_pid = self.process_id
                self.message_send.s_pn = self.process_name
                self.message_send.method = method
                self.message_send.command = command
                self.message_send.payload = data

                # 发送数据
                self.process_link_info[pro]['msg_in'].put(self.message_send)
                self.msg_out_count += 1
                self.process_link_info[pro]['msg_send'] += 1
            else:
                return False, "process not in link"

    def get_msg(self):
        if self.msg_queue_in.empty() is True:
            return False, "there is no message"
        else:
            new_msg = self.msg_queue_in.get()
            self.message_receive.method = new_msg['method']
            self.message_receive.s_pn = new_msg['s_pn']
            self.message_receive.s_pid = new_msg['s_pid']
            self.message_receive.d_pn = new_msg['d_pn']
            self.message_receive.d_pid = new_msg['d_pid']
            self.message_receive.command = new_msg['command']
            self.message_receive.payload = new_msg['payload']


def my_process(process_name, queue_up, queue_down):

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
    for count in range(0, 1, 1):
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