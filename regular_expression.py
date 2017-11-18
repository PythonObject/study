# coding: utf-8
# file name: regular_expression.py
# python version: 2.7
# author: wu ming ming
# description: study of regular expression

"""
.                    匹配任意字符（不包括换行符）
^                    匹配开始位置，多行模式下匹配每一行的开始
$                    匹配结束位置，多行模式下匹配每一行的结束
*                    匹配前一个元字符0到多次
+                    匹配前一个元字符1到多次
?                    匹配前一个元字符0到1次
{m,n}                匹配前一个元字符m到n次
\\                   转义字符，跟在其后的字符将失去作为特殊元字符的含义，例如\\.只能匹配.，不能再匹配任意字符
[]                   字符集，一个字符的集合，可匹配其中任意一个字符
|                    逻辑表达式 或 ，比如 a|b 代表可匹配 a 或者 b
(...)                分组，默认为捕获，即被分组的内容可以被单独取出，默认每个分组有个索引，从 1 开始，按照"("的顺序决定索引值
(?iLmsux)            分组中可以设置模式，iLmsux之中的每个字符代表一个模式,用法参见 模式 I
(?:...)              分组的不捕获模式，计算索引时会跳过这个分组
(?P<name>...)        分组的命名模式，取此分组中的内容时可以使用索引也可以使用name
(?P=name)            分组的引用模式，可在同一个正则表达式用引用前面命名过的正则
(?#...)              注释，不影响正则表达式其它部分,用法参见 模式 I
(?=...)              顺序肯定环视，表示所在位置右侧能够匹配括号内正则
(?!...)              顺序否定环视，表示所在位置右侧不能匹配括号内正则
(?<=...)             逆序肯定环视，表示所在位置左侧能够匹配括号内正则
(?<!...)             逆序否定环视，表示所在位置左侧不能匹配括号内正则
(?(id/name)yes|no)   若前面指定id或name的分区匹配成功则执行yes处的正则，否则执行no处的正则
\number              匹配和前面索引为number的分组捕获到的内容一样的字符串
\A                   匹配字符串开始位置，忽略多行模式
\Z                   匹配字符串结束位置，忽略多行模式
\b                   匹配位于单词开始或结束位置的空字符串
\B                   匹配不位于单词开始或结束位置的空字符串
\d                   匹配一个数字， 相当于 [0-9]
\D                   匹配非数字,相当于 [^0-9]
\s                   匹配任意空白字符， 相当于 [ \t\n\r\f\v]
\S                   匹配非空白字符，相当于 [^ \t\n\r\f\v]
\w                   匹配数字、字母、下划线中任意一个字符， 相当于 [a-zA-Z0-9_]
\W                   匹配非数字、字母、下划线中的任意字符，相当于 [^a-zA-Z0-9_]
"""

import re

if __name__ == '__main__':
    print 'regular_expression study'

    # '''
    # re模块中的search和match的差别
    # re.compile(pattern, flags=0)
    #   给定一个正则表达式pattern，指定使用的模式，
    #   flag默认为0，即不使用任何模式，返回SRE_Pattern对象
    #   推荐使用compile函数预编译出一个正确的模式之后去使用，这样后面的代码中
    #   可以很方便的复用他
    # '''

    regex = re.compile('.+')
    print regex

    s = '''
    first line
    second line
    third line
    '''
    # 调用findall函数
    regex = re.compile('.+')
    print regex.findall(s)

    # 调用search 函数
    print regex.search(s).group()

    # '''
    # match(pattern, string, flags=0)
    #     使用指定的正则表达式去待操作字符串中寻找可以匹配的子串，返回匹配上的
    #     第一个字符串，并且不再继续寻找，如果开始处不匹配，则不再继续寻找，返回
    #     一个SRE_Match对象，找不到时返回None
    # '''

    s = '''first line 
second line
third line
    '''
    regex = re.compile('\w+')
    m = regex.match(s)
    print m
    print m.group()

    regex = re.compile('^s\w+')
    print regex.match(s).group()
    print regex.search(s).group()