import time

class Node():
    #節點類
    def __init__(self,data = -1):
        self.data = data
        self.left = None
        self.right = None
class Tree():
    #樹類
    def __init__(self):
        self.root = Node()
 
    def add(self,data):
        # 為樹加入節點
        node  = Node(data)
        if self.root.data == -1:        #如果樹為空，就對根節點賦值
            self.root = node
        else:
            myQueue = []
            treeNode = self.root
            myQueue.append(treeNode)
            while myQueue:              #對已有的節點進行層次遍歷
                treeNode = myQueue.pop(0)
                if not treeNode.left:
                    treeNode.left = node
                    return
                elif not treeNode.right:
                    treeNode.right = node
                    return
                else:
                    myQueue.append(treeNode.left)
                    myQueue.append(treeNode.right)
 
    def pre_order_recursion(self,root):     #遞迴實現前序遍歷
        if not root:
            return
        print (root.data)
        self.pre_order_recursion(root.left)
        self.pre_order_recursion(root.right)
 
    def pre_order_stack(self,root):         #堆疊實現前序遍歷（非遞迴）
        if not root:
            return
        myStack = []
        node = root
        while myStack or node:
            while node:       #從根節點開始，一直尋找他的左子樹
                print(node.data)
                myStack.append(node)
                node = node.left
            node = myStack.pop()    #while結束表示當前節點node為空，即前一個節點沒有左子樹了
            node = node.right       #開始檢視它的右子樹
 
    def in_order_recursion(self,root):      #遞迴實現中序遍歷
        if not root:
            return
        self.in_order_recursion(root.left)
        print(root.data)
        self.in_order_recursion(root.right)
 
    def in_order_stack(self,root):        #堆疊實現中序遍歷（非遞迴）
        if not root:
            return
        myStack = []
        node = root
        while myStack or node:     #從根節點開始，一直尋找它的左子樹
            while node:
                myStack.append(node)
                node = node.left
            node = myStack.pop()
            print(node.data)
            node = node.right
 
 
    def post_order_recursion(self,root):     #遞迴實現後序遍歷
        if not root:
            return
        self.post_order_recursion(root.left)
        self.post_order_recursion(root.right)
        print(root.data)
        
    def post_order_stack(self, root):  # 堆疊實現後序遍歷（非遞迴）
        # 先遍歷根節點，再遍歷右子樹，最後是左子樹，這樣就可以轉化為和先序遍歷一個型別了，最後只把遍歷結果逆序輸出就OK了。
        if not root:
            return
        myStack1 = []
        myStack2 = []
        node = root
        while myStack1 or node:
            while node:
                myStack2.append(node)
                myStack1.append(node)
                node = node.right
            node = myStack1.pop()
            node = node.left
        while myStack2:
            print(myStack2.pop().data)
 
    def level_order_queue(self,root):       #佇列實現層次遍歷（非遞迴）
        if not root :
            return
        myQueue = []
        node = root
        myQueue.append(node)
        while myQueue:
            node = myQueue.pop(0)
            print(node.data)
            if node.left:
                myQueue.append(node.left)
            if node.right:
                myQueue.append(node.right)
                
if __name__ == '__main__':
    #主函式
    datas = [2,3,4,5,6,7,8,9]
    tree = Tree()          #新建一個樹物件
    for data in datas:
        tree.add(data)      #逐個加入樹的節點
 
    #time.sleep(50)
    print('遞迴實現前序遍歷：')
    tree.pre_order_recursion(tree.root)
 
    # print ('\n堆疊實現前序遍歷')
    # tree.pre_order_stack(tree.root)
 
    # print ("\n\n遞迴實現中序遍歷：")
    # tree.in_order_recursion(tree.root)
 
    # print ("\n堆疊實現中序遍歷：")
    # tree.in_order_stack(tree.root)
 
    # print ('\n\n遞迴實現後序遍歷：')
    # tree.post_order_recursion(tree.root)
 
    # print ('\n堆疊實現後序遍歷：')
    # tree.post_order_stack(tree.root)
 
    # print ('\n\n佇列實現層次遍歷：')
    # tree.level_order_queue(tree.root)