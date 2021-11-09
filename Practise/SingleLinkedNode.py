# 建立單連結串列類
class SingleLinkList(object):
    def __init__(self):
        self.header = None
        self.length = 0

    # 1、判斷是否為空
    def is_empty(self):
        if self.header == None:
            return True
        else:
            return False

    # 2、頭部插入
    def add(self, node):
        # 如果為空
        if self.is_empty():
            self.header = node
        else:
            node.next = self.header
            self.header = node
            # currentNode = self.header
        self.length += 1

    # 3、尾部插入
    def append(self, node):
        current_Node = self.header
        if self.is_empty():
            self.add(node)
        else:
            # 找到最後一個結點
            while (current_Node.next != None):
                current_Node = current_Node.next
            current_Node.next = node
            self.length += 1

    # 4、指定位置插入
    def insert(self, node, index):
        current_Node = self.header
        
        if index > self.length + 1 or index <= 0:
            while (index > self.length + 1 or index <= 0):
                print("你要插入的位置不對，請重選位置:")
                index = eval(input())

        if index == 1:
            self.add(node)
        elif index == 2:
            node.next = self.header.next
            self.header.next = node
            self.length += 1
        else:
            for i in range(1, index - 1):
                current_Node = current_Node.next
            node.next = current_Node.next
            current_Node.next = node
            self.length += 1

    # 5、遍歷
    def travel(self):
        current_Node = self.header
        if self.length == 0:
            print("目前連結串列沒有資料！")
        else:
            print("目前連結串列裡面的元素有:", end=" ")
            for i in range(self.length):
                print("%s " % current_Node.element, end=" ")
                current_Node = current_Node.next
            print("\n")

    # 6、排序不用交換節點的位置，只需要交換節點上的資料值
    def list_sort(self):
        for i in range(0, self.length - 1):
            current_Node = self.header
            for j in range(0, self.length - i - 1):
                if current_Node.element > current_Node.next.element:
                    temp = current_Node.element
                    current_Node.element = current_Node.next.element
                    current_Node.next.element = temp

                current_Node = current_Node.next

    # 7、按索引刪除
    def delete(self, index):
        if index <= 0 or index > self.length:
            while (index <= 0 or index > self.length):
                print("你輸入的下標不對，請重新輸入需要刪除的值的下標：")
                index = eval(input())
                #   return
        else:
            if index == 1:
                self.header = self.header.next
                currentNode = self.header
            elif index == 2:
                current_Node = self.header
                current_Node.next = current_Node.next.next
            else:
                current_Node = self.header
                for i in range(1, index - 1):
                    current_Node = current_Node.next
                current_Node.next = current_Node.next.next
        self.length -= 1

    # 8、查詢是否包含,並返回下標
    def isContain(self, num):
        contain = 0
        current_Node = self.header
        for i in range(self.length):
            if current_Node.element == num:
                print("%d在連結串列中%d處\n" % (num, i + 1))  # i+1是在正常人認為的位置處，程式設計師一般是從0開始算起
                contain = 1
            current_Node = current_Node.next
        if contain == 0:
            print("%d不在連結串列中\n" % num)

    # 9、根據下標找節點
    def searchNodeByIndex(self, index):
        current_Node = self.header
        if index <= 0 or index > self.length:
            while (index <= 0 or index > self.length):
                print("你輸入的下標不對，請重新輸入:")
                index = eval(input())
                #   return 0
        if index > 0 or index <= self.length:
            for i in range(index - 1):
                current_Node = current_Node.next
            return current_Node

    # 10、根據下標修改節點的值
    def Alert(self, index, num):  # index定義為下標
        current_Node = self.header
        if index <= 0 or index > self.length:
            print("你輸入的下標不對，請重新輸入!\n")
        else:
            for i in range(index - 1):
                current_Node = current_Node.next
            current_Node.element = num
