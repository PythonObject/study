# coding: utf-8
# file name: decorator.py
# python version: 2.7
# author: wu ming ming
# description: study of decorator

import time
import sys
import functools
# function decorator


def self_introduction(func):
    print sys._getframe().f_lineno, "I am Bom. "
    return func


@self_introduction
def say_hi(name):
    """"""
    print sys._getframe().f_lineno, "hi, %s" % name


def function_performance_statistics(trace_this=True):
    if trace_this is True:
        def performance_statics_delegate(func):
            def counter(*args, **kwargs):
                start = time.clock()
                print sys._getframe().f_lineno, "start time:", start
                func(*args, **kwargs)
                end = time.clock()
                print sys._getframe().f_lineno, "end time:", end
                print sys._getframe().f_lineno, "used time %d" % (end - start)
            return counter
    else:
        def performance_statics_delegate(func):
            return func

    return performance_statics_delegate


@function_performance_statistics(True)
def add(x, y):
    time.sleep(2)
    print sys._getframe().f_lineno, "add result: %d" % (x + y)


@function_performance_statistics(False)
def mul(x, y):
    print sys._getframe().f_lineno, "mul result:%d" % (x * y)


# class decorator
def bar(dummy):
    print sys._getframe().f_lineno, "bar"


def inject(cls):
    cls.bar = bar
    return cls


@inject
class Foo(object):
    pass


class Human(object):
    def __init__(self, func):
        self.name = None
        self.func = func

    def __call__(self, *args, **kwargs):
        self.eat()
        return self.func

    @staticmethod
    def breath():
        print sys._getframe().f_lineno, "I need air"

    def eat(self):
        print sys._getframe().f_lineno, "I am %s, I want rice" % self.name

@Human
def someone():
    pass


def CatDecorator(cls):

    @functools.wraps(cls)
    class new_class:
        def __init__(self, name):
            cls.__init__(self, name)
            self.sex = "male"

        def set_sex(self, sex):
            self.sex = sex

        def get_set(self):
            return self.sex

    return new_class


@CatDecorator
class Cat(object):
    def __init__(self, name):
        self.name = name


if __name__ == "__main__":
    # function decorator
    print "\n----------function decorator----------"
    say_hi("tim")
    add(3, 5)
    mul(3, 5)

    # class decorator
    print "\n-----------class decorator-------------"
    foo = Foo()
    foo.bar()
    Human.breath()
    Tim = Human("Tim")
    Tim.breath()
    Tim.eat()
    Bob = someone()

    Jack = Cat("Jack")
    Jack.set_sex("femal")
    print Jack.get_set()
