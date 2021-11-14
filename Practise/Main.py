from Leetcode import Leetcode
import time

#print(any(chr.isdigit() for chr in x)) #判斷文字中是否有數字
# for i in [x for x in datelist[0] if x.isdigit()]: For 回圈內撈出一個 List
#print(list(zip([1,1],[2,2])))
#arry = [2,b,'b',3,6]
#print(arry)

# a = 'abcd'
# b='abcde'
# print(a-b)
la = 'abcde'
lb = 'abcdef'
diff = set(la)|set(lb)
print(diff)
Leetcode
leedcoedc = Leetcode()

leedcoedc.reverseStr('abcdefgh',2)

time.sleep(300)
# a=b'abcd'
# b=str(a,encoding='big5')
# print(type(b))
# print(a)
