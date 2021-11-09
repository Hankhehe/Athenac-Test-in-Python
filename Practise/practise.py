def Fib(n): #堆疊練習
    if n<=1:
        return(n)
    else:
        return(Fib(n-1)+Fib(n-2))
        
def Towers(n,A,C,B): # 河內塔
    if n==1:
        print("Move disk",n,"from",A,"to",C)
    else:
        Towers(n-1,A,B,C)
        print("Move disk",n,"from",A,"to",C)
        Towers(n-1,B,C,A)

def bubbleshort(nums):
    n = len(nums)
    for i in range(n):
        for j in range(n-i-1):
            if nums[j]> nums[j+1]:
                nums[j]=nums[j]+nums[j+1]
                nums[j+1]= nums[j]-nums[j+1]
                nums[j]= nums[j]-nums[j+1]
                #nums[j+1],nums[j] = nums[j],nums[j+1]
    return nums


Towers(4,'A','C','B')