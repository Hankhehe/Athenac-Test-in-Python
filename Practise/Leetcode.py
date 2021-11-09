import operator

class Leetcode:
    def longestCommonPrefix(self, strs) -> str:
        common_index = 0
        for i in range(min(len(w) for w in strs)):
            orders = [ord(word[i]) for word in strs]
            if max(orders) == min(orders):
                common_index += 1
            else:
                break
        return strs[0][:common_index]

    def isValid(self, s: str) -> bool:
        while "()" in s or "{}" in s or "[]" in s:
            s = s.replace("{}", "").replace("()", "").replace("[]", "")
        return s == ""

    def mergeTwoLists(self, l1, l2):
        l3 = l1+l2
        l3.sort()
        return l3

    def removeDuplicates(nums) -> int:
        i = 1
        for j in range(1, len(nums)):
            if nums[j - 1] < nums[j]:
                nums[i] = nums[j]
                i += 1
        return i

    def twoSum(nums, target):
        lookup = {}
        for i, num in enumerate(nums):
            if num in lookup:
                return [lookup[num], i]
        lookup[target - num] = i

    def maxSubArray(nums):
        max_ending_here, max_so_far = float('-inf'), float('-inf')
        for num in nums:
            max_ending_here = max(num, max_ending_here + num)
            max_so_far = max(max_so_far, max_ending_here)
        return max_so_far

    def searchInsert(nums, target):
        index = len(nums)//2

        while index != len(nums) and target > nums[index]:
            index += 1

        while index > 0 and target <= nums[index - 1]:
            index -= 1
        return index

    def lengthOfLastWord(self, s: str) -> int:
        slist = s.strip().split(" ")
        return len(slist[-1])

    def plusOne(digits: list) -> list:
        temp = str()
        retlist = []
        for digit in digits:
            temp += str(digit)
        temp = str(int(temp)+1)
        for tem in temp:
            retlist.append(tem)
        return retlist

    def addBinary(a: str, b: str) -> str:
        return format(int(a, 2) + int(b, 2), 'b')

    def climbStairs(self, n: int) -> int:  # 第 70 題，爬樓梯(費氏數列)
        prev, curr = 1, 1
        for i in range(1, n):
            prev, curr = curr, prev + curr
        return curr

    def isPalindrome(self, s: str) -> bool:  # 第 125 題
        # 將文字用空值用 join 接起來並用 isalnum 去除英數之外
        st = ''.join(a for a in s if a.isalnum()).upper()
        rst = ''.join(reversed(st)).upper()  # 用reversed 反轉字串
        return st == rst

    def singleNumber(self, nums: list) -> int:  # 136. Single Number
        countl = {}
        for num in nums:
            if countl.__contains__(num):
                countl[num] += 1
            else:
                countl[num] = 1
        return int([k for k, v in countl.items() if v == 1][0])

    def convertToTitle(self, n: int) -> str:  # 168. Excel Sheet Column Title
        result = []
        while n > 0:
            n, r = divmod(n-1, 26)  # 取出除數和餘數
            result.append(chr(r + ord('A')))  # 用餘數 + A 的 ASCII code 得出是甚麼英文
        return ''.join(result[::-1])  # 返回

    def reverseBits(self, n: int) -> int:
        # check = 1
        # binstr = ""
        # for i in range(32):
        #     if check & n:
        #         binstr += str('1')
        #     else:
        #         binstr += str('0')
        #     check <<= 1
        # return int(binstr, 2)

        n = 43261596
        result = 0
        for x in range(32):
            if (n & 1):
                result = result | 1

            result <<= 1
            n >>= 1

        if (n & 1):
            result = result | 1
        print(bin(result))
        print(result)
        return

    def hammingWeight(self, n: int) -> int:  # 191 Number of 1 Bits
        count = 0
        check = 1
        for i in range(32):
            if n & check:
                count += 1
            check <<= 1
        return count

    def isPowerOfThree(self, n: int) -> bool:  # 326 Power of Three
        if n == 0:
            return False
        if n == 1:
            return True
        if n < 3 and n > -3 and n != 1:
            return False
        return self.isPowerOfThree(n/3)
    
    def maxProfit(prices) -> int: #121 Best Time to Buy and Sell Stock
        max_ending_here, max_so_far = 0, 0
        for profit in map(operator.sub, prices[1:], prices):
            max_ending_here = max(max_ending_here + profit, 0)
            max_so_far = max(max_so_far, max_ending_here)
        return max_so_far

    def twoSum(self, nums, target: int): #2. Two Sum
        lookup = {}
        for i, num in enumerate(nums):
            if num in lookup:
                return [lookup[num], i]
            lookup[target - num] = i
    
    def fib(self, n: int) -> int: #509. Fibonacci Number
        if n ==1 or n==2:
            return n
        else:
            return self.fib(n-1)+self.fib(n-2)

    def reverseStr(self, s: str, k: int) -> str: # 541 Reverse String II
        index = 0
        returnstr = ''
        while index < len(s):
            returnstr += ''.join(reversed(s[index:index+k]))
            index += k
            returnstr += s[index:index+k]
            index +=k
        return returnstr
