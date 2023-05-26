import random
from queue_ import Queue
from stack import Stack

# BSTNode is a node in the Binary Search Tree.
class BSTNode:
    def __init__(self, value: object) -> None:
        """
        Initialize a BST Node.

        :param value: The value to be stored in the node.
        """
        self.value = value
        self.left = None
        self.right = None

    def __str__(self) -> str:
        """
        String representation of a BST Node.

        :return: A string representation of the BST Node.
        """
        return 'BST Node: {}'.format(self.value)

# BST is a Binary Search Tree.
class BST:
    def __init__(self, start_tree=None) -> None:
        """
        Initialize a BST.

        :param start_tree: A starting tree.
        """
        self._root = None
        if start_tree is not None:  # If a starting tree is provided
            for value in start_tree:  # For each value in the starting tree
                self.add(value)  # Add the value to the BST

    def __str__(self) -> str:
        """
        String representation of the BST.

        :return: A string representation of the BST.
        """
        values = []
        self._str_helper(self._root, values)
        return "BST pre-order { " + ", ".join(values) + " }"

    def _str_helper(self, node: BSTNode, values: []) -> None:
        """
        A helper function to get a string representation of the BST.

        :param node: The current node.
        :param values: The list of values in the BST.
        """
        if not node:  # If node is None, return
            return
        values.append(str(node.value))  # Append the value of the current node
        self._str_helper(node.left, values)  # Traverse the left subtree
        self._str_helper(node.right, values)  # Traverse the right subtree

    def get_root(self) -> BSTNode:
        """
        Get the root of the BST.

        :return: The root of the BST.
        """
        return self._root

    def is_valid_bst(self) -> bool:
        """
        Check if the BST is valid.

        :return: True if the BST is valid, False otherwise.
        """
        stack = Stack()
        stack.push(self._root)
        while not stack.is_empty():
            node = stack.pop()
            if node:
                if node.left and node.left.value >= node.value:
                    return False
                if node.right and node.right.value < node.value:
                    return False
                stack.push(node.right)
                stack.push(node.left)
        return True

    def add(self, value: object) -> None:
        """
        Add an element to the BST.

        :param value: The value to be added.
        """
        new_node = BSTNode(value)  # Create a new node
        node = self._root  # Start at the root
        if self._root is None:  # If the tree is empty
            self._root = new_node  # Set the root to the new node
            return
        while node:
            if value < node.value:  # If value is less than current node's value
                if node.left is None:  # And current node has no left child
                    node.left = new_node  # Insert the new node as the left child
                    return
                else:
                    node = node.left  # Move to the left child
            elif value >= node.value:  # If value is greater or equal to current node's value
                if node.right is None:  # And current node has no right child
                    node.right = new_node  # Insert the new node as the right child
                    return
                else:
                    node = node.right  # Move to the right child

    def remove(self, value: object) -> bool:
        """
        Remove an element from the BST.

        :param value: The value to be removed.
        :return: True if the node is removed, False otherwise.
        """
        # Find the node to be removed and its parent node
        node = self._root
        parent_node = None
        while node is not None:
            if node.value == value:  # The node to be removed is found
                break
            elif value < node.value:  # Move to the left subtree
                parent_node = node
                node = node.left
            else:  # Move to the right subtree
                parent_node = node
                node = node.right

        # The node to be removed is not found
        if node is None:
            return False

        # Case 1: The node is a leaf node (no children)
        if node.right is None and node.left is None:
            if parent_node is None:  # The node is the root
                self._root = None
            elif parent_node.left == node:  # The node is a left child
                parent_node.left = None
            else:  # The node is a right child
                parent_node.right = None

        # Case 2: The node has one child
        elif node.left is None or node.right is None:
            # Get the child node
            child_node = node.left if node.left is not None else node.right

            if parent_node is None:  # The node is the root
                self._root = child_node
            elif parent_node.left == node:  # The node is a left child
                parent_node.left = child_node
            else:  # The node is a right child
                parent_node.right = child_node

        # Case 3: The node has two children
        else:
            # Find the in-order successor (the smallest node in the right subtree)
            successor = node.right
            successor_parent = node
            while successor.left is not None:
                successor_parent = successor
                successor = successor.left

            # Replace the node with the successor
            successor.left = node.left
            if successor is not node.right:
                successor_parent.left = successor.right
                successor.right = node.right

            if parent_node is None:  # The node is the root
                self._root = successor
            elif parent_node.left == node:  # The node is a left child
                parent_node.left = successor
            else:  # The node is a right child
                parent_node.right = successor

        return True

    def contains(self, value: object) -> bool:
        """
        Check if the BST contains a value.
        :param value: The value to check.
        :return: True if the BST contains the value, False otherwise.
        """
        node = self._root
        found = False
        while node is not None:
            if node.value == value:
                found = True
                break
            elif value < node.value:
                node = node.left
            else:
                node = node.right
        return found

    def inorder_traversal(self) -> Queue:
        """
        Execute an in-order traversal of the BST.

        :return: A queue of nodes in the order they were traversed.
        """
        node = self._root  # Start at the root
        inorder_queue = Queue()  # Create an empty queue
        in_stack = Stack()  # Create an empty stack

        # While there are still unvisited nodes
        while node is not None or in_stack.is_empty() is not True:
            # Go to the left most node of the current node
            while node is not None:
                in_stack.push(node)
                node = node.left

            # Backtrack from the empty subtree and visit the node at the top of the stack
            if in_stack.is_empty() is not True:
                node = in_stack.pop()
                inorder_queue.enqueue(node.value)  # Add the node to the queue
                node = node.right  # Visit the right subtree

        return inorder_queue

    def find_min(self) -> object:
        """
        Find the minimum value in the BST.

        :return: The minimum value in the BST. Returns None if the BST is empty.
        """
        if self.is_empty():
            return None

        node = self._root  # Start at the root
        # Go to the left most node (minimum value in a BST)
        while node.left is not None:
            node = node.left
        return node.value

    def find_max(self) -> object:
        """
        Find the maximum value in the BST.

        :return: The maximum value in the BST. Returns None if the BST is empty.
        """
        if self.is_empty():
            return None

        node = self._root  # Start at the root
        # Go to the right most node (maximum value in a BST)
        while node.right is not None:
            node = node.right
        return node.value

    def is_empty(self) -> bool:
        """
        Check if the BST is empty.
        :return: True if the BST is empty, False otherwise.
        """
        return self._root is None

    def make_empty(self) -> None:
        """
        Empty the BST.
        """
        self._root = None

if __name__ == '__main__':

    print("\nPDF - method add() example 1")
    print("----------------------------")
    test_cases = (
        (1, 2, 3),
        (3, 2, 1),
        (1, 3, 2),
        (3, 1, 2),
    )
    for case in test_cases:
        tree = BST(case)
        print(tree)

    print("\nPDF - method add() example 2")
    print("----------------------------")
    test_cases = (
        (10, 20, 30, 40, 50),
        (10, 20, 30, 50, 40),
        (30, 20, 10, 5, 1),
        (30, 20, 10, 1, 5),
        (5, 4, 6, 3, 7, 2, 8),
        (range(0, 30, 3)),
        (range(0, 31, 3)),
        (range(0, 34, 3)),
        (range(10, -10, -2)),
        ('A', 'B', 'C', 'D', 'E'),
        (1, 1, 1, 1),
    )
    for case in test_cases:
        tree = BST(case)
        print('INPUT  :', case)
        print('RESULT :', tree)

    print("\nPDF - method add() example 3")
    print("----------------------------")
    for _ in range(100):
        case = list(set(random.randrange(1, 20000) for _ in range(900)))
        tree = BST()
        for value in case:
            tree.add(value)
        if not tree.is_valid_bst():
            raise Exception("PROBLEM WITH ADD OPERATION")
    print('add() stress test finished')

    print("\nPDF - method remove() example 1")
    print("-------------------------------")
    test_cases = (
        ((1, 2, 3), 1),
        ((1, 2, 3), 2),
        ((1, 2, 3), 3),
        ((50, 40, 60, 30, 70, 20, 80, 45), 0),
        ((50, 40, 60, 30, 70, 20, 80, 45), 45),
        ((50, 40, 60, 30, 70, 20, 80, 45), 40),
        ((50, 40, 60, 30, 70, 20, 80, 45), 30),
    )
    for case, del_value in test_cases:
        tree = BST(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 2")
    print("-------------------------------")
    test_cases = (
        ((50, 40, 60, 30, 70, 20, 80, 45), 20),
        ((50, 40, 60, 30, 70, 20, 80, 15), 40),
        ((50, 40, 60, 30, 70, 20, 80, 35), 20),
        ((50, 40, 60, 30, 70, 20, 80, 25), 40),
    )
    for case, del_value in test_cases:
        tree = BST(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 3")
    print("-------------------------------")
    case = range(-9, 16, 2)
    tree = BST(case)
    for del_value in case:
        print('INPUT  :', tree, del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 4")
    print("-------------------------------")
    case = range(0, 34, 3)
    tree = BST(case)
    for _ in case[:-2]:
        root_value = tree.get_root().value
        print('INPUT  :', tree, root_value)
        tree.remove(root_value)
        if not tree.is_valid_bst():
            raise Exception("PROBLEM WITH REMOVE OPERATION")
        print('RESULT :', tree)

    print("\nPDF - method contains() example 1")
    print("---------------------------------")
    tree = BST([10, 5, 15])
    print(tree.contains(15))
    print(tree.contains(-10))
    print(tree.contains(15))

    print("\nPDF - method contains() example 2")
    print("---------------------------------")
    tree = BST()
    print(tree.contains(0))

    print("\nPDF - method inorder_traversal() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print(tree.inorder_traversal())

    print("\nPDF - method inorder_traversal() example 2")
    print("---------------------------------")
    tree = BST([8, 10, -4, 5, -1])
    print(tree.inorder_traversal())

    print("\nPDF - method find_min() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_min() example 2")
    print("---------------------------------")
    tree = BST([8, 10, -4, 5, -1])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_max() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method find_max() example 2")
    print("---------------------------------")
    tree = BST([8, 10, -4, 5, -1])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method is_empty() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method is_empty() example 2")
    print("---------------------------------")
    tree = BST()
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method make_empty() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)

    print("\nPDF - method make_empty() example 2")
    print("---------------------------------")
    tree = BST()
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)
