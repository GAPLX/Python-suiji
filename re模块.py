# -*- coding: utf-8 -*-
"""
Created on Wed Nov  7 12:42:06 2018

@author: lenovo
"""

import re

'''
常用正则表达式符号和语法：
'''

#[] 是定义匹配的字符范围。比如 [a-zA-Z0-9] 表示相应位置的字符要匹配英文字符和数字。
#如果第一个字符是^，表示取反
example = 'aacabcacc'
re.findall('a[abc]c',example)
>>> ['aac', 'abc', 'acc']
re.findall('a[^a-b]c',example)
>>> ['acc']

#[\s*]表示空格或者*号。

#'.' 匹配所有字符串，除\n以外
re.findall('.','aaadddadd')
>>> ['a', 'a', 'a', 'd', 'd', 'd', 'a', 'd', 'd']          
re.findall('#.','aaadddadd #234455')
>>> ['#2']
re.findall('#...','aaadddadd #234455')
>>> ['#234']

#'-' 表示范围[0-9]
re.findall('[a-z]','a12z')
>>> ['a', 'z']

#'*' 匹配前面的子表达式零次或多次。要匹配 * 字符，请使用 \*
re.findall('#.*','aaadddadd #234455')
>>> ['#234455']
     
#'+' 匹配前面的子表达式一次或多次。要匹配 + 字符，请使用 \+
re.findall('#.+','aaadddadd #234455')
>>> ['#234455']
re.findall('#.+','aaadddadd #')
>>> []

#'^'或'\A' 表示表达式仅匹配字符串的开头,写在开头
re.findall('^ab','abbvbcaba')
>>> ['ab']
re.findall('^ab','cabbb')
>>> []

#'$'或'\Z' 表示表达式仅匹配字符串结尾，写在结尾
re.findall('ab$','abbvbcaab')
>>> ['ab']
re.findall('ab$','cabbcc')
>>> []

#'?' 匹配前一个字符串0次或1次
re.findall('12?','1233331')
>>> ['12','1']

#'{m}' 匹配前一个字符m次,'{m,n}' 匹配前一个字符m-n次
re.findall('ab{2}','abbccab')
>>> ['abb']
re.findall('ab{1,2}','abbccab')
>>> ['abb','ab']

#'\d' 匹配数字，'\D'匹配非数字
re.findall('\d','123hh')
>>> ['1','2','3']

#'\w' 匹配字母和数字，'\W'匹配非字母和数字
re.findall('\W','.123/ 4')
>>> [',','/',' ']

#'\s' 匹配空白字符,'\S' 匹配非空白字符
re.findall('\s','iwwiw   wiw')
>>> [' ',' ',' ']

# "数量词?" ：非贪婪模式：只匹配最少的（尽可能少）；默认贪婪模式：匹配最多的（尽可能多）
>>> pat = re.compile('[abc]+')         #贪婪模式
>>> pat.match('abcdefabcabc').group()  #匹配尽可能多的：abc
'abc'
>>> pat.match('bbabcdefabcabc').group()
'bbabc'
>>> pat.search('dbbabcdefabcabc').group()
'bbabc'
>>> pat.findall('abcdefabcabc')
['abc', 'abcabc']

>>> pat = re.compile('[abc]+?')        #非贪婪模式：+?
>>> pat.match('abcdefabcabc').group()  #匹配尽可能少的：a、b、c
'a'
>>> pat.search('dbbabcdefabcabc').group()
'b'
>>> pat.findall('abcdefabcabc')
['a', 'b', 'c', 'a', 'b', 'c', 'a', 'b', 'c']

# | 左右表达式任意匹配一个，先匹配左边一旦成功则跳过匹配右边，
# 如果|没有包含在()中,匹配整个正则表达式
re.search('123|abc','123abc').group()
>>> '123'
re.search('(123|abc)(zzz)','123abczzz').groups() #123zzz不存在
>>> ('abc','zzz')

#(?P<name>...)  除了分组序号外,指定一个 name的别名
print(re.search('(?P<名字>lx)xel','wtlxxel').group())
>>> 'lxxel'
print(re.search('(?P<名字>lx)xel','wtlxxel').groupdict())
>>> {'名字':'lx'}

#"(?P=name)"   引用命名分组(别名)匹配
print(re.search('(?P<k>a)b(?P=k)','1a2aba3').group())
>>> 'aba'
print(re.search('(?P<k>a)(b)(?P=k)','1a2aba3').groups())
>>> ('a','b')  #注意这里引用命名分组别名匹配并不属于分组行为
print(re.search('(?P<k>a)b((?P=k))','1a2aba3').groups())
>>> ('a','a')

#\<number> 引用编号为<number>的分组匹配到的字符串
print(re.search(r'(?P<k>a)b(?P=k)\1','1a2abaa3').group()) #\1 引用编号为1的分组
>>> 'abaa'

#(?=...) 匹配到...表达式，返回前面内容。对后进行匹配，总是对后面进行匹配
re.findall(r'[a-z]+(?=\d)','dasdasd12zzz3')
>>> ['dasdasd','zzz'] #在数字2处断了，其前面不是字母
re.search(r'\w+(?=\d)','dasdasd12zzz3').group()
>>> 'dasdasd12zzz' #一直符合表达式，根据总是对后面进行匹配，所以到最后才匹配

#(?!...) 匹配到不是...表达式，返回前面内容。对后进行匹配，总是对后面进行匹配
re.search(r'[a-z]+(?!\d)','dasdasd12zzz3').group()
>>>'dasdas'  #最后一个不是数字的字符是d，返回其前面的内容

# "(?<=...)"：匹配...表达式，返回。对前进行匹配,总是对前面进行匹配
pat=re.compile(r'(?<=\d)[A-Za-z]+')      #匹配前面是数字的字母
pat.findall('1abc21,2def31,3xyz41')
>>> ['abc', 'def', 'xyz']

# "(?<!...)"：不匹配...表达式，返回。对前进行匹配,总是对前面进行匹配
pat=re.compile(r'(?<!\d)[A-Za-z]+')      #匹配前面不是数字的字母
pat.findall('abc21,def31,xyz41')
>>> ['abc', 'def', 'xyz']

#(?i) 或 re.I(推荐这种) 不区分大写小
re.search('(?i)abc','Abc').group()
>>> 'Abc' 
re.search('abc','Abc',re.I).group()
>>> 'Abc'



'''常用re函数
参数说明：
pattern:匹配的正则表达式
string：要匹配的字符串
flags：标记为，用于控制正则表达式的匹配方式，如：是否区分大小写，多行匹配等等。
repl：替换的字符串，也可作为一个函数
count：模式匹配后替换的最大次数，默认0表示替换所有匹配
'''
#re.match(pattern,string,flags=0)
#从字符串的起始位置匹配，如果起始位置匹配不成功的话，match()就返回none
print(bool(re.match('ssr','ssr,sr,r')))
>>> Ture
----------------------------------------------------------------------------
#re.search(pattern,string,flags=0)
#扫描整个字符串并返回第一个成功的匹配
print(bool(re.search('sr','ssr,sr,r')))
>>> Ture
print(re.search('\d\W\D','111.wwww').group())
>>> 1.w  (str)
-------------------------------------------------------------------------
#re.findall(pattern,string,flags=0)
#找到RE匹配的所有字符串，并把他们作为一个列表返回
re.findall('\d+','13w13w62')
>>> ['13','13','62']
--------------------------------------------------------------------------
#re.finditer(pattern,sting,flags=0)
#找到RE匹配的所有字符串，并把他们作为一个迭代器返回
content = '''email:12345678@163.com
email:2345678@163.com
email:345678@163.com
'''
result_finditer = re.finditer("\d*@\d*.com", content)
#由于返回的为MatchObject的iterator，所以我们需要迭代并通过MatchObject的方法输出
for i in result_finditer:
    print(i.group())

result_findall = re.findall("\d*@\d*.com", content)
for i in result_findall:
    print(i)
-----------------------------------------------------------------------
#re.sub(pattern,repl,string,count=0,flags=o)
phone = '15757065539 #这是我的电话'
re.sub('#.*',' ',phone)
>>> '15757065539  '
-------------------------------------------------------------------------
#re.split(pattern,string,flags=0)
#根据模式分割字符串
re.split(',','12,1,15')
>>>['12', '1', '15']
re.split(',','12,1,15',maxsplit=1)
>>>['12','1,15']



'''
关于正则式表达式的分组
'''

e_mail ='''
1019775574@qq.com
756981301@163.com
1012492462@lx.com
'''
#未分组的，返回全部正则表达式内容
e_mail_split = re.findall('\d*@\w*',e_mail)
>>>['1019775574@qq', '756981301@163', '1012492462@lx']
#分组的，只返回正则表达式中的分组部分,且以list嵌套tupe的形式分组返回
e_mail_split = re.findall('(\d*)@(\w*)',e_mail)
>>>[('1019775574','qq'), ('756981301','163'), ('1012492462','lx')]
for i,j in e_mail_split :
   dic = {'账号':i,'平台':j}
   print(dic)
>>>{'账号': '1019775574', '平台': 'qq'}
{'账号': '756981301', '平台': '163'}
{'账号': '1012492462', '平台': 'lx'}
#无聊
z = ''
p = ''
t = 0  
for i,j in e_mail_split :
    if t < 2 : 
        z += (i+',')
        p += (j+',')
    else:
        z += (i+'.')
        p += (j+'.')
    t += 1
dic = {'账号合集':z,'平台合集':p}
print(dic)
>>>{'账号合集': '1019775574,756981301,1012492462.', '平台合集': 'qq,163,lx.'}



'''
获得匹配的函数
方法/属性                作用
group(num=0)    匹配的整个表达式的字符串，group() 可以一次输入多个组号，
                在这种情况下它将返回一个包含那些组所对应值的元组。
groups()        返回包含所有小组字符串的元组，从1到所含的小组
groupdict()     返回以有别名的组的别名为键、以该组截获的子串为值的字典
start()         返回匹配开始的位置
end()           返回匹配结束的位置
span()          返回一个元组包含匹配（开始，结束）的位置
'''

#补充group的使用方法
#group（）在正则表达式中用于获取分段截获的字符串，解释如下代码：
a = "123abc456"
print re.search("(\d+)(\D+)",a).group(0)    #123abc,返回整体
print re.search("(\d+)(\D+)",a).group(1)    #123
print re.search("(\d+)(\D+)",a).group(2)    #abc

#可以看出，正则表达式按照数字-字母-数字的顺序来获取相应字符串，那么分别就是“数字
#（group（1））--字母（group（2））”的对应关系，
#其中，group（0）和group（）效果相同，均为获取取得的字符串整体。
-------------------------------------------------------------------------
#补充groups()的使用方法
b = "123abc456"
print (re.search("(\d+)(\D+)",b).groups())
>>> ('123','abc')
-------------------------------------------------------------------------
#groupdict()用法，见'(?P<name>...)'表达式用法



'''
原生字符串
每一次在匹配规则前面加了一个r，表示不转义
'''

'''
编译
如果一个匹配规则要多次使用，可以先将其编译，以后就不用每次去重复写匹配规则
'''
comp = re.compile(r'1\d?')
print(comp.findall('123a1sd'))
>>> ['12','1']






