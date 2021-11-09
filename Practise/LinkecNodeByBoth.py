#Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def binaryTreePaths(root):
    if not root: return []
    if not root.left and not root.right: return [str(root.val)]
    results = sum(map(binaryTreePaths, (root.left, root.right)), [])
    return [str(root.val) + '->' + substr for substr in results]

a = TreeNode(1)
a.left = TreeNode(2)
a.right =TreeNode(3)
a.left.right = TreeNode(5)

print(binaryTreePaths(a))


