# encoding: utf-8
# file name:multiprocess_manager.py

__author__ = 'wu ming ming'


from multiprocessing import Process, Manager
from threading import Thread
from time import sleep


class ProcessManager(object):
    '''process manager'''

    def __init__(self):
        self.manager = Manager()
        self.process_new = {}
        self.process_run = {}
        self.process_join = {}
        self._check_thread = None

    def _check_thread_flash(self):
        '''刷新检查线程,如果没有生成/启动,则生成/启动线程, 如果已经启动,则跳过'''
        if self._check_thread is None or not self._check_thread.is_alive():
            self._check_thread = Thread(target=self._check_process)
            self._check_thread.daemon = True
            self._check_thread.start()
        # elif not self._check_thread.is_alive():
        #     self._check_thread.start()

    @property
    def check_pro_type(self, pro_type):
        return pro_type in map(lambda x: x.__name__, Process.__subclasses__())

    def add_process(self, pro_name, pro_type, *args, **kwargs):
        '''添加一个进程'''
        if not self.check_pro_type(pro_type):
            raise TypeError
        if 'return_value' in kwargs and kwargs['return_value']:
            raise KeyError
        count = 1
        while pro_name in self.process_new or pro_name in self.process_join or pro_name in self.process_join:
            pro_name += str(count)
            count += 1
            # if count >= 10:
            #     return False
        new_pro = eval(pro_type)(args, kwargs)
        self.process_new[pro_name] = {
            'process': new_pro,
            'pid': new_pro.pid,
            'is_alive': new_pro.is_alive(),
            'result': dict(),
            'manager_dict': self.manager.dict()
        }
        return new_pro

    def del_process(self, pro_name):
        '''删除一个进程和结果'''
        if pro_name in self.process_run:
            # todo: manager共享数据获取
            pro = self.process_run[pro_name]['process'].terminate()
            self.process_run[pro_name]['process'].join()
            return pro
            # todo: force kill the process
        elif pro_name in self.process_new:
            pro = self.process_new.pop(pro_name)
            return pro
        elif pro_name in self.process_join:
            if not self.process_join[pro_name]['result']:
                # todo: manager 共享数据获取
                pass
            pro = self.process_join.pop(pro_name)
            return pro
        else:
            return 'process {} not in lists'.format(pro_name)

    def get_pro_result(self, *pro_list):
        '''读取一个进程运行结果,结果读清'''
        return map(lambda x: self.del_process(x) if x in self.process_join else {x: None}, pro_list)

    def clean_pro_result(self):
        '''删除所有已结束进程运行结果和进程数据'''
        pro_list = self.process_join
        self.process_join = {}
        return pro_list

    def clean_all_pro(self):
        self.process_new = {}
        self.process_join = {}
        for pro in self.process_run:
            self.process_run[pro]['process'].terminate()
            self.process_run[pro]['process'].join()

    def _check_process(self):
        while True:
            for pro in self.process_run:
                if not self.process_run[pro]['process'].is_alive():
                    self.process_run[pro]['process'].join()
                    self.process_run[pro]['result'] = dict(self.process_run[pro]['manager_dict'])
                    self.process_join[pro] = self.process_run[pro]
                    self.process_run.pop(pro)
                    self.process_join[pro]['is_alive'] = self.process_join[pro]['process'].is_alive()
            sleep(0.5)

    def start_pro_list(self):
        '''运行列表中的进程.'''

        def _move_data_ro_run(pro):
            pass
        self._check_thread_flash()
        for pro in self.process_new:
            if self.process_new[pro]['process'].is_alive():
                self.process_new[pro]['pid'] = self.process_new[pro]['process'].pid
                self.process_new[pro]['is_alive'] = self.process_new[pro]['process'].is_alive()
                _move_data_ro_run(pro)
                continue
            self.process_new[pro]['process'].start()
            count = 0
            while not self.process_new[pro]['process'].is_alive:
                sleep(0.5)
                if count >= 5:
                    break
            if self.process_new[pro]['process'].is_alive():
                self.process_new[pro]['pid'] = self.process_new[pro]['process'].pid
                self.process_new[pro]['is_alive'] = self.process_new[pro]['process'].is_alive()
                _move_data_ro_run(pro)
        pass


class CheckPro(Process):
    '''check process base class'''

    def __init__(self, *args, **kwargs):
        super(CheckPro, self).__init__()

    def start(self, *args, **kwargs):
        pass

    def stop(self, *args, **kwargs):
        pass


class SrvCheckPro(CheckPro):
    '''server check process'''

    def __init__(self, *args, **kwargs):
        super(SrvCheckPro, self).__init__()
        pass

    def start(self):
        pass

    def stop(self):
        pass


class SwCheckPro(CheckPro):
    '''switch check process'''

    def __init__(self, *args, **kwargs):
        super(SwCheckPro, self).__init__()
        pass

    def start(self):
        pass

    def stop(self):
        pass


def create_check_pro(pro_type, *args, **kwargs):
    if pro_type not in map(lambda x: x.__name__, CheckPro.__subclasses__()):
        raise TypeError

    pro = eval(pro_type)(args, kwargs)




if __name__ == '__main__':
    create_check_pro('SrvCheckPro')
    pass