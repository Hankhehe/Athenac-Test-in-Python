import collections
from functools import reduce
from typing import Collection
from Leetcode import Leetcode
import time

#print(any(chr.isdigit() for chr in x)) #判斷文字中是否有數字
# for i in [x for x in datelist[0] if x.isdigit()]: For 回圈內撈出一個 List
#print(list(zip([1,1],[2,2])))
#arry = [2,b,'b',3,6]
#print(arry)

list1 = ['a','b','c']
list2 = ['b','c','d']

print(list(set(list1)&set(list2)))
pass

s = 'abcd'
t ='abcde'

a=[]
a.append(4)
a.insert(0,1)
a.insert(0,2)
print (a)
pass
scount ,tcount = collections.Counter(s),collections.Counter(t)
for t in tcount:
    if tcount[t] > scount[t]:
        print (t.count())
reduce



Leetcode
leedcoedc = Leetcode()

leedcoedc.reverseStr('abcdefgh',2)

time.sleep(300)
# a=b'abcd'
# b=str(a,encoding='big5')
# print(type(b))
# print(a)
