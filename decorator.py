# coding: utf-8
# file name: decorator.py
# author: wumingming
# description: study of decorator

import time

# function decorator


def self_introduction(func):
	print "I am Bom. "
	return func


@self_introduction
def say_hi(name):
	""""""
	print "hi, %s" % name


def function_performance_statistics(trace_this=True):
	if trace_this is True:
		def performance_statics_delegate(func):
			def counter(*args, **kwargs):
				start = time.clock()
				print "start time:", start
				func(*args, **kwargs)
				end = time.clock()
				print "end time:", end
				print "used time %d" % (end - start)
			return counter
	else:
		def performance_statics_delegate(func):
			return func

	return performance_statics_delegate


@function_performance_statistics(True)
def add(x, y):
	time.sleep(5)
	print "add result: %d" % (x + y)


@function_performance_statistics(False)
def mul(x, y):
	print "mul result:%d" % (x * y)


# class decorator
def bar(dummy):
	print "bar"


def inject(cls):
	cls.bar = bar
	return cls


@inject
class Foo(object):
	pass


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
