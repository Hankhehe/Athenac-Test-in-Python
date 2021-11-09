class Test1(object): #類別名稱，(與繼承類別)
    count=10 #類屬性，但外部呼叫可以新增隨意新增和修改
    def get(num:int, string:str)-> int: # 方法，傳入參數和回傳值限定無用。
        return 1 # return 值

class BinaryTreeNode():
    def __init__(self,val) -> None:
        self.val = val
        self.right = None
        self.left = None

class Node():
    def __init__(self,val) -> None:
        self.val = val
        self.next = None


node1 = Node(1)
node1.next=Node(2)
node1.next.next =Node(3)
node1.next.next.next =Node(4)
node1.next.next.next.next = Node(5)
node1.next.next.next.next.next = Node(6)
print(node1.next.val)
current = node1

while True:
    if current.next is None:
        break
    print(current.val)
    current = current.next

print(node1.next.val)
    
    





