# Name: Ivan Ruiz
# OSU Email: ruiziv@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 4
# Due Date: 5/22/2023
# Description: This code creates a BST with various methods in addition to add and remove.


import random
from queue_and_stack import Queue, Stack


class BSTNode:
    """
    Binary Search Tree Node class
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """

    def __init__(self, value: object) -> None:
        """
        Initialize a new BST node
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.value = value   # to store node's data
        self.left = None     # pointer to root of left subtree
        self.right = None    # pointer to root of right subtree

    def __str__(self) -> str:
        """
        Override string method
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return 'BST Node: {}'.format(self.value)


class BST:
    """
    Binary Search Tree class
    """

    def __init__(self, start_tree=None) -> None:
        """
        Initialize new Binary Search Tree
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._root = None

        # populate BST with initial values (if provided)
        # before using this feature, implement add() method
        if start_tree is not None:
            for value in start_tree:
                self.add(value)

    def __str__(self) -> str:
        """
        Override string method; display in pre-order
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        values = []
        self._str_helper(self._root, values)
        return "BST pre-order { " + ", ".join(values) + " }"

    def _str_helper(self, node: BSTNode, values: []) -> None:
        """
        Helper method for __str__. Does pre-order tree traversal
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if not node:
            return
        values.append(str(node.value))
        self._str_helper(node.left, values)
        self._str_helper(node.right, values)

    def get_root(self) -> BSTNode:
        """
        Return root of tree, or None if empty
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._root

    def is_valid_bst(self) -> bool:
        """
        Perform pre-order traversal of the tree.
        Return False if nodes don't adhere to the bst ordering property.

        This is intended to be a troubleshooting method to help find any
        inconsistencies in the tree after the add() or remove() operations.
        A return of True from this method doesn't guarantee that your tree
        is the 'correct' result, just that it satisfies bst ordering.

        DO NOT CHANGE THIS METHOD IN ANY WAY
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

    # ------------------------------------------------------------------ #

    def add(self, value: object) -> None:
        """
        Add a new node to the Binary Search Tree (BST) with the provided value.

        :param value: number we are adding to BST

        :return None
        """
        # Create a new node
        new_node = BSTNode(value)
        node = self._root

        # If the tree is empty, the root becomes the new node
        if self._root is None:
            self._root = new_node
            return

        # Find the right place to insert the new node
        while node is not None:
            # If the new value is less than the current node
            if value < node.value:
                if node.left is None:
                    node.left = new_node
                    return
                else:
                    node = node.left

            # If the new value is greater than or equal to the current node
            elif value >= node.value:
                if node.right is None:
                    node.right = new_node
                    return
                else:
                    node = node.right

    def remove(self, value: object) -> bool:
        """
        Remove a node from the BST with the provided value.

        :param value: object of value that will be removed

        :returns: True if the node was found and removed, False otherwise
        """
        # Start from the root node
        node = self._root
        parent_node = None

        # Find the node to be removed
        while node is not None:
            if node.value == value:
                break
            # Go to the left subtree
            elif value < node.value:
                parent_node = node
                node = node.left
            # Go to the right subtree
            else:
                parent_node = node
                node = node.right

        if node is None:
            return False

        # No child case
        if node.right is None and node.left is None:
            if parent_node is None:
                self._root = None
            elif parent_node.left == node:
                parent_node.left = None
            else:
                parent_node.right = None

        # One child case
        elif node.left is None or node.right is None:
            if parent_node is None:
                if node.left is not None:
                    self._root = node.left
                else:
                    self._root = node.right
            elif parent_node.left == node:
                if node.left is not None:
                    parent_node.left = node.left
                else:
                    parent_node.left = node.right
            else:
                if node.left is not None:
                    parent_node.right = node.left
                else:
                    parent_node.right = node.right

        # Two children case, find the in-order successor and
        # replace it with the node to be removed
        else:
            # Find the in-order successor (the leftmost node in the right subtree)
            successor = node.right
            successor_parent = node
            while successor.left is not None:
                successor_parent = successor
                successor = successor.left

            # Replace the node to be removed with the in-order successor
            successor.left = node.left
            if successor is not node.right:
                successor_parent.left = successor.right
                successor.right = node.right

            # Update the parent nodes child reference
            if parent_node is None:
                self._root = successor
            elif parent_node.left == node:
                parent_node.left = successor
            else:
                parent_node.right = successor
        return True

    def contains(self, value: object) -> bool:
        """
        Check if the BST contains a given value.

        :param value: object of the value one is searching for

        :returns found: bool, True or False if found
        """
        node = self._root
        found = False

        # Traverse the tree, breaking the loop if the value is found
        while node is not None:
            if node.value == value:
                found = True
                break
            # Navigate left
            elif value < node.value:
                node = node.left
            # Navigate right
            else:
                node = node.right
        return found


    def inorder_traversal(self) -> Queue:
        """
        Inorder traversal of the BST, returning the values in a queue.

        :param None:

        :returns inorder_queue: A Queue
        """
        node = self._root
        inorder_queue = Queue()
        in_stack = Stack()

        # Continue until all nodes are visited
        while node is not None or in_stack.is_empty() is not True:

            # Move to the leftmost node, pushing each node onto the stack
            while node is not None:
                in_stack.push(node)
                node = node.left

            # If there are unvisited nodes, visit the next one
            if in_stack.is_empty() is not True:
                node = in_stack.pop()
                inorder_queue.enqueue(node.value)
                node = node.right

        return inorder_queue

    def find_min(self) -> object:
        """
        This function returns the minimum value in the Binary Search Tree (BST).

        :param None:

        :returns minimum: object
        """
        # If the tree is empty, there's no minimum value
        if self.is_empty():
            return None
        else:
            # Perform an in-order traversal
            in_order_que = self.inorder_traversal()

            # The first dequeued element from in_order_que is the minimum value
            minimum = in_order_que.dequeue()
            return minimum

    def find_max(self) -> object:
        """
        This function returns the maximum value in the Binary Search Tree (BST).

        :param None:

        returns max_val: object
        """
        # If the tree is empty, there's no maximum value
        if self.is_empty():
            return None
        else:
            # If the tree is not empty, perform an in-order traversal
            # to give a queue of values in ascending order
            in_order_que = self.inorder_traversal()

            # Push the dequeued elements from in_order_que into the stack
            max_stack = Stack()
            while not in_order_que.is_empty():
                number = in_order_que.dequeue()
                max_stack.push(number)

            # The top of the stack contains the maximum value
            max_val = max_stack.pop()
            return max_val

    def is_empty(self) -> bool:
        """
        Checks if the BST is empty

        :receives None:

        :returns True or False
        """
        if self._root is None:
            return True
        else:
            return False

    def make_empty(self) -> None:
        """
        Will make the bst empty

        :param None:

        :returns None:
        """
        self._root = None


# ------------------- BASIC TESTING -----------------------------------------

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
