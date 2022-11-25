"""
Given a binary search tree print the key elements using the in-order-traversal, pre-order-traversal and post-order-traversal
"""


class Node:
    
    def __init__(self, data):
        self.data = data
        self.right = None
        self.left = None

    # O(N) -> in order to insert a new element in the tree we need to trasverse all n elements
    def insert(self, data): 
        if self.data:
            if data < self.data:
                if self.left is None:
                    self.left = Node(data)
                else:
                    self.left.insert(data)
            else:
                if self.right is None:
                    self.right = Node(data)
                else:
                    self.right.insert(data)
        else:
            self.data = data

    # in order: left -> root -> right
    def inOrderTraversalPrint(self):
        if self.left:
            self.left.inOrderTraversalPrint()
        print(self.data)
        if self.right:
            self.right.inOrderTraversalPrint()

    def inOrderTraversalList(self, root):
        res = []
        if root:
            res = self.inOrderTraversalList(root.left)
            res.append(root.data)
            res = res + self.inOrderTraversalList(root.right)
        return res
        
    # pre order: root -> left -> right
    def preOrderTraversalPrint(self):
        print(self.data)
        if self.left:
            self.left.preOrderTraversalPrint()
        if self.right:
            self.right.preOrderTraversalPrint()

    def preOrderTraversalList(self, root):
        res = []
        if root:
            res.append(root.data)
            res = res + self.preOrderTraversalList(root.left)
            res = res + self.preOrderTraversalList(root.right)
        return res

    # post order:  left -> right -> root
    def postOrderTraversalPrint(self):
        if self.left:
            self.left.postOrderTraversalPrint()
        if self.right:
            self.right.postOrderTraversalPrint()
        print(self.data)

    def postOrderTraversalList(self, root):
        res = []
        if root:
            res = res + self.postOrderTraversalList(root.left)
            res = res + self.postOrderTraversalList(root.right)
            res.append(root.data)
        return res

if __name__ == "__main__":
    root = Node(15)
    root.insert(10)
    root.insert(25)
    root.insert(6)
    root.insert(14)
    root.insert(20)
    root.insert(60)

    print("In order traversal:")
    root.inOrderTraversalPrint()

    in_order_traversal_list = root.inOrderTraversalList(root)
    print("In order traversal list: ", in_order_traversal_list)

    print("\nPre order traversal:")
    root.preOrderTraversalPrint()

    pre_order_traversal_list = root.preOrderTraversalList(root)
    print("Pre order traversal list: ", pre_order_traversal_list)

    print("\nPost order traversal:")
    root.postOrderTraversalPrint()

    post_order_traversal_list = root.postOrderTraversalList(root)
    print("Post order traversal list: ", post_order_traversal_list)