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


node1 = ListNode(15)
list1 = SingleLinkedList()
list1.add_list_item(1)
list1.add_list_item(1)
list1.add_list_item(2)
list1.add_list_item(3)