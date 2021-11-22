class ListNode:
    def __init__(self, data): 
    # store data
        self.data = data
    # store the reference (next item)
        self.next = None
        return

class SingleLinkedList:
    def __init__(self): 
        self.head = None
        self.tail = None
        return

    def add_list_item(self, item):
  # make sure item is a proper node
        if not isinstance(item, ListNode):
            item = ListNode(item)
            
        if self.head is None:
            self.head = item
        else:
            self.tail.next = item

        self.tail = item
        return
    
    def printlinkednode(self):
        pl = self.head
        while not pl is None:
            print(pl.data)
            pl = pl.next
        return
            
def printNode(node):
    while node:
        print(node.data)
        node = node.next
    
def ReverseNode(node):
    rnode = None
    while node:
        temp1 = ListNode(node.data)
        temp1.next = rnode
        rnode = temp1
        node = node.next
    return rnode

list1 = SingleLinkedList()
list1.add_list_item(1)
list1.add_list_item(2)
list1.add_list_item(3)
list1.add_list_item(4)
list1.add_list_item(5)
list1.add_list_item(6)
list1.add_list_item(7)
# printNode(list1.head)
# list1.printlinkednode()
node2 = ReverseNode(list1.head)
printNode(list1.head)
printNode(node2)