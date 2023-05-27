# Name: Ivan Ruiz
# OSU Email: ruiziv@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 4
# Due Date: 5/22/2023
# Description: This file creates  an AVL with various methods in addition to add and remove.


import random
from queue_and_stack import Queue, Stack
from bst import BSTNode, BST


class AVLNode(BSTNode):
    """
    AVL Tree Node class. Inherits from BSTNode
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    def __init__(self, value: object) -> None:
        """
        Initialize a new AVL node
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        # call __init__() from parent class
        super().__init__(value)

        # new variables needed for AVL
        self.parent = None
        self.height = 0

    def __str__(self) -> str:
        """
        Override string method
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return 'AVL Node: {}'.format(self.value)


class AVL(BST):
    """
    AVL Tree class. Inherits from BST
    """

    def __init__(self, start_tree=None) -> None:
        """
        Initialize a new AVL Tree
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        # call __init__() from parent class
        super().__init__(start_tree)

    def __str__(self) -> str:
        """
        Override string method
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        values = []
        super()._str_helper(self._root, values)
        return "AVL pre-order { " + ", ".join(values) + " }"

    def is_valid_avl(self) -> bool:
        """
        Perform pre-order traversal of the tree. Return False if there
        are any problems with attributes of any of the nodes in the tree.

        This is intended to be a troubleshooting 'helper' method to help
        find any inconsistencies in the tree after the add() or remove()
        operations. Review the code to understand what this method is
        checking and how it determines whether the AVL tree is correct.

        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        stack = Stack()
        stack.push(self._root)
        while not stack.is_empty():
            node = stack.pop()
            if node:
                # check for correct height (relative to children)
                left = node.left.height if node.left else -1
                right = node.right.height if node.right else -1
                if node.height != 1 + max(left, right):
                    return False

                if node.parent:
                    # parent and child pointers are in sync
                    if node.value < node.parent.value:
                        check_node = node.parent.left
                    else:
                        check_node = node.parent.right
                    if check_node != node:
                        return False
                else:
                    # NULL parent is only allowed on the root of the tree
                    if node != self._root:
                        return False
                stack.push(node.right)
                stack.push(node.left)
        return True

    # ------------------------------------------------------------------ #

    def add(self, value: object) -> None:
        """
        Insert a new node with given value into the AVL tree.

        :param value: object of value that will be added

        :returns None
        """

        # Create a new node
        new_node = AVLNode(value)
        node = self._root

        # Check if the tree is empty
        if self._root is None:
            self._root = new_node
            return

        # Traverse the tree to find the correct position for new_node
        while node:
            if value < node.value:
                if node.left is None:
                    node.left = new_node
                    new_node.parent = node
                    break
                else:
                    node = node.left
            elif value > node.value:
                if node.right is None:
                    node.right = new_node
                    new_node.parent = node
                    break
                else:
                    node = node.right
            else:
                return

        # Moves up the tree starting from the newly inserted node, rebalancing as it goes
        node = new_node
        parent = node.parent
        while parent:
            self._rebalance(parent)
            parent = parent.parent

    def remove(self, value: object) -> bool:
        """
        Remove a node with the given value from the AVL tree.

        :param value: object of value to be removed

        :returns: True if the node was found and removed, False otherwise.
        """

        # Start from the root node
        node = self._root
        parent_node = None

        # Find the node to be removed
        while node is not None:
            if node.value == value:
                break
            elif value < node.value:
                parent_node = node
                node = node.left
            else:
                parent_node = node
                node = node.right

        if node is None:
            return False

        if node.right is None and node.left is None:
            if parent_node is None:
                self._root = None
            elif parent_node.left == node:
                parent_node.left = None
            else:
                parent_node.right = None

        elif node.left is None or node.right is None:
            new_node = node.left if node.left is not None else node.right
            if parent_node is None:
                self._root = new_node
            elif parent_node.left == node:
                parent_node.left = new_node
            else:
                parent_node.right = new_node
            new_node.parent = parent_node
            self._update_height(new_node)

        else:
            successor = node.right
            successor_parent = node
            while successor.left is not None:
                successor_parent = successor
                successor = successor.left

            # Attach the left subtree of the node to the successor
            successor.left = node.left
            if node.left is not None:
                node.left.parent = successor

            # If the successor is not the right child of the node,
            # update the parent's left child and attach the right subtree of the node to the successor
            if successor is not node.right:
                if successor_parent is not node:
                    successor_parent.left = successor.right
                if successor.right is not None:
                    successor.right.parent = successor_parent
                successor.right = node.right

            # If the node's right child is not None,
            # update its parent pointer to point to the successor
            if node.right is not None:
                node.right.parent = successor

            # Perform rebalancing starting from the successor's parent
            self._rebalance(successor_parent)

            # Adjust the parent's child pointer to point to the successor
            if parent_node is None:
                self._root = successor
            elif parent_node.left == node:
                parent_node.left = successor
            else:
                parent_node.right = successor
            successor.parent = parent_node  # End of 'else' block

        node_to_balance = parent_node if parent_node is not None else self._root
        while node_to_balance is not None:
            self._rebalance(node_to_balance)
            self._update_height(node_to_balance)
            node_to_balance = node_to_balance.parent

        return True


    def _balance_factor(self, node: AVLNode) -> int:
        """
        Calculates the balance factor

        :param node: AVLNode

        :returns the difference betweent the right and left height in int
        """
        if node is None:
            return 0
        left_height = self._get_height(node.left)
        right_height = self._get_height(node.right)
        return right_height - left_height

    def _get_height(self, node: AVLNode) -> int:
        """
        Returns the height of the node

        :param node: AVLNode

        :returns node.height: int
        """
        if node is None:
            return -1
        else:
            return node.height

    def _rotate_left(self, node: AVLNode) -> AVLNode:
        """
        Perform a left rotation on a given node.

        :param node: AVLNode

        :returns child: AVLNode
        """
        # Reassign child nodes for rotation
        child = node.right
        node.right = child.left

        # Reassign parents if necessary
        if node.right:
            node.right.parent = node
        child.left = node
        child.parent = node.parent

        # Reassign the child to the node's parent if exists
        if node.parent:
            if node.parent.left == node:
                node.parent.left = child
            else:
                node.parent.right = child

        # Reassign node's parent to child
        # Update heights of the node and child
        node.parent = child
        self._update_height(node)
        self._update_height(child)

        return child

    def _rotate_right(self, node: AVLNode) -> AVLNode:
        """
        Perform a right rotation on a given node.

        :param node: AVLNode

        :returns child: AVLNode
        """

        # Reassign child nodes for rotation
        child = node.left
        node.left = child.right

        # Reassign parents if necessary
        if node.left:
            node.left.parent = node
        child.right = node
        child.parent = node.parent

        # Reassign the child to the node's parent if exists
        if node.parent:
            if node.parent.left == node:
                node.parent.left = child
            else:
                node.parent.right = child

        # Reassign node's parent to child
        node.parent = child

        # Update heights of the node and child
        self._update_height(node)
        self._update_height(child)

        return child

    def _update_height(self, node: AVLNode) -> None:
        """
        Updates the height of the node

        :param node: AVLNode

        :returns none
        """

        node.height = max(self._get_height(node.left), self._get_height(node.right)) + 1


    def _rebalance(self, node: AVLNode) -> None:
        """
        Corrects the balance of the given node in the AVL tree.

        :param node: AVLNode

        :returns none
        """

        # Calculate the height of left and right child nodes.
        left_height = self._get_height(node.left)
        right_height = self._get_height(node.right)

        # If the left subtree is heavier.
        if right_height - left_height < -1:
            # Left-right case: perform a left rotation on left child.
            if self._balance_factor(node.left) > 0:
                node.left = self._rotate_left(node.left)
                node.left.parent = node
            # Perform a right rotation on current node.
            new_subtree_root = self._rotate_right(node)
            # If new root, update self._root
            if new_subtree_root.parent is None:
                self._root = new_subtree_root

        # If the right subtree is heavier.
        elif right_height - left_height > 1:
            # Right-left case: perform a right rotation on right child.
            if self._balance_factor(node.right) < 0:
                node.right = self._rotate_right(node.right)
                node.right.parent = node
            # Perform a left rotation on current node.
            new_subtree_root = self._rotate_left(node)
            # If new root, update self._root
            if new_subtree_root.parent is None:
                self._root = new_subtree_root
        # If balanced, simply update the height.
        else:
            self._update_height(node)

# ------------------- BASIC TESTING -----------------------------------------


if __name__ == '__main__':

    print("\nPDF - method add() example 1")
    print("----------------------------")
    test_cases = (
        (1, 2, 3),  # RR
        (3, 2, 1),  # LL
        (1, 3, 2),  # RL
        (3, 1, 2),  # LR
    )
    for case in test_cases:
        tree = AVL(case)
        print(tree)

    print("\nPDF - method add() example 2")
    print("----------------------------")
    test_cases = (
        (10, 20, 30, 40, 50),   # RR, RR
        (10, 20, 30, 50, 40),   # RR, RL
        (30, 20, 10, 5, 1),     # LL, LL
        (30, 20, 10, 1, 5),     # LL, LR
        (5, 4, 6, 3, 7, 2, 8),  # LL, RR
        (range(0, 30, 3)),
        (range(0, 31, 3)),
        (range(0, 34, 3)),
        (range(10, -10, -2)),
        ('A', 'B', 'C', 'D', 'E'),
        (1, 1, 1, 1),
    )
    for case in test_cases:
        tree = AVL(case)
        print('INPUT  :', case)
        print('RESULT :', tree)

    print("\nPDF - method add() example 3")
    print("----------------------------")
    for _ in range(100):
        case = list(set(random.randrange(1, 20000) for _ in range(900)))
        tree = AVL()
        for value in case:
            tree.add(value)
        if not tree.is_valid_avl():
            raise Exception("PROBLEM WITH ADD OPERATION")
    print('add() stress test finished')

    print("\nPDF - method remove() example 1")
    print("-------------------------------")
    test_cases = (
        ((1, 2, 3), 1),  # no AVL rotation
        ((1, 2, 3), 2),  # no AVL rotation
        ((1, 2, 3), 3),  # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 0),
        ((50, 40, 60, 30, 70, 20, 80, 45), 45),  # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 40),  # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 30),  # no AVL rotation
    )
    for case, del_value in test_cases:
        tree = AVL(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 2")
    print("-------------------------------")
    test_cases = (
        ((50, 40, 60, 30, 70, 20, 80, 45), 20),  # RR
        ((50, 40, 60, 30, 70, 20, 80, 15), 40),  # LL
        ((50, 40, 60, 30, 70, 20, 80, 35), 20),  # RL
        ((50, 40, 60, 30, 70, 20, 80, 25), 40),  # LR
    )
    for case, del_value in test_cases:
        tree = AVL(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 3")
    print("-------------------------------")
    case = range(-9, 16, 2)
    tree = AVL(case)
    for del_value in case:
        print('INPUT  :', tree, del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 4")
    print("-------------------------------")
    case = range(0, 34, 3)
    tree = AVL(case)
    for _ in case[:-2]:
        root_value = tree.get_root().value
        print('INPUT  :', tree, root_value)
        tree.remove(root_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 5")
    print("-------------------------------")
    for _ in range(100):
        case = list(set(random.randrange(1, 20000) for _ in range(900)))
        tree = AVL(case)
        for value in case[::2]:
            tree.remove(value)
        if not tree.is_valid_avl():
            raise Exception("PROBLEM WITH REMOVE OPERATION")
    print('remove() stress test finished')

    print("\nPDF - method contains() example 1")
    print("---------------------------------")
    tree = AVL([10, 5, 15])
    print(tree.contains(15))
    print(tree.contains(-10))
    print(tree.contains(15))

    print("\nPDF - method contains() example 2")
    print("---------------------------------")
    tree = AVL()
    print(tree.contains(0))

    print("\nPDF - method inorder_traversal() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print(tree.inorder_traversal())

    print("\nPDF - method inorder_traversal() example 2")
    print("---------------------------------")
    tree = AVL([8, 10, -4, 5, -1])
    print(tree.inorder_traversal())

    print("\nPDF - method find_min() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_min() example 2")
    print("---------------------------------")
    tree = AVL([8, 10, -4, 5, -1])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_max() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method find_max() example 2")
    print("---------------------------------")
    tree = AVL([8, 10, -4, 5, -1])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method is_empty() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method is_empty() example 2")
    print("---------------------------------")
    tree = AVL()
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method make_empty() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)

    print("\nPDF - method make_empty() example 2")
    print("---------------------------------")
    tree = AVL()
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)
