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

    def add_process(self, pro_name, func, *args, **kwargs):
        '''添加一个进程'''
        if 'return_value' in kwargs and kwargs['return_value']:
            raise KeyError
        count = 1
        name_tmp = pro_name
        while name_tmp in self.process_new or name_tmp in self.process_join or name_tmp in self.process_join:
            name_tmp = pro_name + str(count)
            count += 1
            # if count >= 10:
            #     return False
        pro_name = name_tmp
        kwargs['name'] = pro_name
        manager_dict = self.manager.dict()
        kwargs['return_value'] = manager_dict
        new_pro = Process(name=pro_name, target=func, args=args, kwargs=kwargs)
        new_pro.daemon = True
        self.process_new[pro_name] = {
            'process': new_pro,
            'pid': new_pro.pid,
            'is_alive': new_pro.is_alive(),
            'manager_dict': manager_dict
        }
        return pro_name

    def _get_manager_dict(self, pro_name):
        if not isinstance(pro_name, str):
            raise TypeError
        if pro_name in self.process_run:
            return dict(self.process_run[pro_name]['manager_dict'])
        elif pro_name in self.process_join:
            return dict(self.process_join[pro_name]['manager_dict'])
        else:
            return {}

    def del_process(self, pro_name):
        '''删除一个进程和结果'''
        if pro_name in self.process_run:
            pro = self.process_run[pro_name]['process'].terminate()
            self.process_run[pro_name]['process'].join()
            return pro, dict(self.process_run[pro_name]['manager_dict'])
            # todo: force kill the process
        elif pro_name in self.process_new:
            pro = self.process_new.pop(pro_name)
            return pro, dict(self.process_new[pro_name]['manager_dict'])
        elif pro_name in self.process_join:
            pro = self.process_join.pop(pro_name)
            return pro, dict(self.process_join[pro_name]['manager_dict'])
        else:
            return 'process {} not in lists'.format(pro_name)

    def get_pro_results(self, *pro_list):
        '''读取一个进程运行结果'''
        return map(lambda x: self.get_pro_result(x), pro_list)

    def get_pro_result(self, pro_name):
        '''非读清获取进程结果'''
        return dict(self._get_manager_dict(pro_name))

    def get_pro_result_cl(self, pro_name):
        '''读清获取进程结果'''
        result = self.get_pro_result(pro_name)
        self.del_process(pro_name)
        return result

    def clean_pro_result(self):
        '''删除所有已结束进程运行结果和进程数据'''
        pro_list = self.process_join
        self.process_join = {}
        return pro_list

    def clean_pro_all(self):
        '''删除所有进程'''
        self.process_new = {}
        self.process_join = {}
        for pro in self.process_run:
            self.process_run[pro]['process'].terminate()
            self.process_run[pro]['process'].join()

    def _check_process(self):
        while True:
            finish_list = []
            for pro in self.process_run:
                if not self.process_run[pro]['process'].is_alive():
                    self.process_run[pro]['process'].join()
                    self.process_join[pro] = self.process_run[pro]
                    self.process_join[pro]['is_alive'] = self.process_join[pro]['process'].is_alive()
                    finish_list.append(pro)
            if finish_list:
                for pro in finish_list:
                    self.process_run.pop(pro)
            sleep(0.1)

    def start_pro_list(self):
        '''运行列表中的进程.'''

        self._check_thread_flash()
        for pro in self.process_new:
            if self.process_new[pro]['process'].is_alive():
                self.process_new[pro]['pid'] = self.process_new[pro]['process'].pid
                self.process_new[pro]['is_alive'] = self.process_new[pro]['process'].is_alive()
                continue
            self.process_new[pro]['process'].start()
        sleep(0.5)
        start_failed_list = []
        for pro in self.process_new:
            if self.process_new[pro]['process'].is_alive():
                self.process_new[pro]['pid'] = self.process_new[pro]['process'].pid
                self.process_new[pro]['is_alive'] = self.process_new[pro]['process'].is_alive()
                self.process_run[pro] = self.process_new[pro]
            else:
                start_failed_list.append(pro)
        self.process_new = {}
        return start_failed_list

    def stop_pro_list(self, pro_name_list):
        if not isinstance(pro_name_list, list):
            raise TypeError
        for pro_name in pro_name_list:
            if pro_name in self.process_run and self.process_run[pro_name]['process'].is_alive():
                self.process_run[pro_name]['process'].terminate()
                self.process_run[pro_name]['process'].join()
                self.process_join[pro_name] = self.process_run[pro_name]
                self.process_run.pop(pro_name)


def srv_check_pro(*args, **kwargs):
    if 'return_value' in kwargs and 'name' in kwargs:
        kwargs['return_value'][kwargs['name']] = [1, 2, 3, 4]
    sleep(2)


def sw_check_pro(*args, **kwargs):
    if 'return_value' in kwargs and 'name' in kwargs:
        kwargs['return_value'][kwargs['name']] = [4, 3, 2, 1]
    sleep(2)


if __name__ == '__main__':
    manager = ProcessManager()
    pro_list = []
    pro_list.append(manager.add_process('srv_check_conn', srv_check_pro))
    pro_list.append(manager.add_process('srv_check_conn', srv_check_pro))
    pro_list.append(manager.add_process('srv_check_conna', srv_check_pro))
    pro_list.append(manager.add_process('srv_check_connb', srv_check_pro))
    pro_list.append(manager.add_process('sw_check_conn', sw_check_pro))
    pro_list.append(manager.add_process('sw_check_conn', sw_check_pro))
    pro_list.append(manager.add_process('sw_check_conna', sw_check_pro))
    pro_list.append(manager.add_process('sw_check_connb', sw_check_pro))
    manager.start_pro_list()
    sleep(1)
    print map(manager.get_pro_result_cl, pro_list)
    sleep(4)
    while True:
        pass