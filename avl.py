import random
from queue_ import Queue
from stack import Stack
from bst import BSTNode, BST

class AVLNode(BSTNode):
    def __init__(self, value: object) -> None:
        """
        Initialize an AVL node with a given value. 
        The node also has attributes for the parent (initially None) and the height (initially 0).
        
        :param value: The value to be stored in the node.
        """
        super().__init__(value)
        self.parent = None  # The parent of this node, initially None
        self.height = 0  # The height of the node within the tree, initially 0

    def __str__(self) -> str:
        """
        Define the string representation of the AVL node.
        The string returned is 'AVL Node: ' followed by the node value.
        
        :return: String representation of the AVL node.
        """
        return 'AVL Node: {}'.format(self.value)

class AVL(BST):
    def __init__(self, start_tree=None) -> None:
        """
        Initialize an AVL tree. If a start_tree is provided, it is used to initialize the AVL tree.
        
        :param start_tree: A list of values to initialize the AVL tree.
        """
        super().__init__(start_tree)

    def __str__(self) -> str:
        """
        Generate a string representation of the AVL tree using pre-order traversal.
        
        :return: String representation of the AVL tree.
        """
        values = []
        super()._str_helper(self._root, values)
        return "AVL pre-order { " + ", ".join(values) + " }"

    def print_tree(self):
        """
        Print the AVL tree by calling the helper function _print_tree_helper starting from the root.
        """
        self._print_tree_helper(self._root, "")

    def _print_tree_helper(self, node, indent):
        """
        Recursive helper function to print the AVL tree. It first traverses to the right child, 
        prints the node value, then traverses to the left child. 
        
        :param node: The current node to be printed.
        :param indent: The current indentation for the printed tree.
        """
        if node is None:
            return
        self._print_tree_helper(node.right, indent + "    ")
        spacing = indent + " "
        if node.right:
            print(spacing + " /")
        else:
            print(spacing + " .")
        print(indent + str(node.value))
        spacing = indent + " "
        if node.left:
            print(spacing + " \\")
        else:
            print(spacing + " .")
        self._print_tree_helper(node.left, indent + "    ")

    def is_valid_avl(self) -> bool:
        """
        Checks if the tree is a valid AVL tree. The tree is valid if all nodes respect the AVL tree property, 
        that is, the heights of the two child subtrees of any node differ by at most one.
        
        :return: True if the tree is a valid AVL tree, otherwise False.
        """
        stack = Stack()
        stack.push(self._root)  # Starting from the root
        while not stack.is_empty():
            node = stack.pop()  # Get the next node from the stack
            if node:
                left_height = self._get_height(node.left)
                right_height = self._get_height(node.right)
                balance_factor = left_height - right_height
                # Check the AVL tree property
                if balance_factor < -1 or balance_factor > 1:
                    print(f"Error: Node {node.value} has an invalid balance factor ({balance_factor})")
                    return False
                if node.parent:  # If this node has a parent
                    if node.value < node.parent.value:  # This node should be the left child of its parent
                        check_node = node.parent.left
                    else:  # This node should be the right child of its parent
                        check_node = node.parent.right
                    if check_node != node:  # Check if this node is properly linked with its parent
                        print(f"Error: Node {node.value} is not properly linked with its parent")
                        return False
                else:  # This node has no parent
                    if node != self._root:  # If it's not the root, there is an error
                        print(f"Error: Node {node.value} is not the root but has no parent")
                        return False
                # Add the children of this node to the stack
                stack.push(node.right)
                stack.push(node.left)
        return True

    def add(self, value: object) -> None:
        """
        Adds a new node with the specified value to the AVL tree. If the value already exists, the function returns without
        adding a new node. After adding a new node, the tree is rebalanced to maintain the AVL tree property.

        :param value: The value to add to the tree.
        """
        new_node = AVLNode(value)  # Create the new node
        node = self._root
        parent_node = None
        while node:  # Find the correct location for the new node
            parent_node = node
            if value < node.value:
                node = node.left
            elif value > node.value:
                node = node.right
            else:
                return  # Value already exists in the tree
        new_node.parent = parent_node  # Set the parent of the new node
        if parent_node is None:  # If the tree was empty, the new node is now the root
            self._root = new_node
        elif value < parent_node.value:  # Insert the new node to the correct position
            parent_node.left = new_node
        else:
            parent_node.right = new_node
        self._rebalance(new_node)  # Rebalance the tree

    def remove(self, value: object) -> bool:
        """
        Removes a node with the specified value from the AVL tree. If the value doesn't exist, the function returns False.
        After removing a node, the tree is rebalanced to maintain the AVL tree property.

        :param value: The value to remove from the tree.
        :return: True if the node was successfully removed, otherwise False.
        """
        node = self._root  # Starting from the root
        parent_node = None
        # Find the node with the given value
        while node is not None:
            if node.value == value:
                break
            parent_node = node  # Keep track of the parent node
            if value < node.value:  # Go to the left child
                node = node.left
            else:  # Go to the right child
                node = node.right
        if node is None:  # The value is not found in the tree
            return False
        if node.left is None and node.right is None:  # The node is a leaf node
            if parent_node is None:  # The tree only has one node
                self._root = None
            else:  # Remove the node from its parent
                if parent_node.left == node:
                    parent_node.left = None
                else:
                    parent_node.right = None
            # Rebalance the tree after removing the node
            self._rebalance(parent_node)
        elif node.left is None or node.right is None:  # The node has one child
            new_node = node.left if node.left is not None else node.right
            if parent_node is None:  # The node is the root
                self._root = new_node
            else:  # Replace the node with its child in the parent
                if parent_node.left == node:
                    parent_node.left = new_node
                else:
                    parent_node.right = new_node
            if new_node is not None:
                new_node.parent = parent_node
            # Rebalance the tree after replacing the node
            self._rebalance(new_node)
        else:  # The node has two children
            # Find the in-order successor of the node
            successor = node.right
            successor_parent = node
            while successor.left is not None:
                successor_parent = successor
                successor = successor.left
            # Replace the node's value with its successor's value
            node.value = successor.value
            # Remove the successor from its parent
            if successor_parent.left == successor:
                successor_parent.left = successor.right
            else:
                successor_parent.right = successor.right
            if successor.right is not None:
                successor.right.parent = successor_parent
            # Rebalance the tree after removing the successor
            self._rebalance(successor_parent)
        return True

    def _balance_factor(self, node: AVLNode) -> int:
        """
        Computes the balance factor of a node. The balance factor of a node is the height of its left subtree 
        minus the height of its right subtree.

        :param node: The node to compute the balance factor for.
        :return: The balance factor of the node.
        """
        if node is None:
            return 0
        left_height = self._get_height(node.left)
        right_height = self._get_height(node.right)
        return left_height - right_height

    def _get_height(self, node: AVLNode) -> int:
        """
        Computes the height of a node. The height of a node is the number of edges in the longest path from the node to a leaf.

        :param node: The node to compute the height for.
        :return: The height of the node.
        """
        if node is None:
            return -1
        else:
            return node.height

    def _rotate_left(self, node: AVLNode) -> AVLNode:
        """
        Performs a left rotation at a node.

        :param node: The node to perform the rotation at.
        :return: The new parent after the rotation.
        """
        child = node.right
        node.right = child.left
        if node.right:
            node.right.parent = node
        child.left = node
        child.parent = node.parent
        if node.parent:
            if node.parent.left == node:
                node.parent.left = child
            else:
                node.parent.right = child
        else:
            self._root = child  # Update the root if necessary
        node.parent = child
        # Update the heights of the affected nodes
        self._update_height(node)
        self._update_height(child)
        return child

    def _rotate_right(self, node: AVLNode) -> AVLNode:
        """
        Performs a right rotation at a node.

        :param node: The node to perform the rotation at.
        :return: The new parent after the rotation.
        """
        child = node.left
        node.left = child.right
        if node.left:
            node.left.parent = node
        child.right = node
        child.parent = node.parent
        if node.parent:
            if node.parent.left == node:
                node.parent.left = child
            else:
                node.parent.right = child
        else:
            self._root = child  # Update the root if necessary
        node.parent = child
        # Update the heights of the affected nodes
        self._update_height(node)
        self._update_height(child)
        return child

    def _update_height(self, node: AVLNode) -> None:
        """
        Updates the height of a node. 

        :param node: The node to update the height for.
        """
        node.height = max(self._get_height(node.left), self._get_height(node.right)) + 1

    def _rebalance(self, node: AVLNode) -> None:
        """
        Rebalances the tree at a node.

        :param node: The node to start the rebalancing from.
        """
        while node is not None:
            self._update_height(node)
            # Check the balance factor of the node
            if self._balance_factor(node) < -1:
                # Left rotate at the node if its right subtree is higher and its right child's right subtree is higher or equal
                if self._balance_factor(node.right) <= 0:
                    node = self._rotate_left(node)
                else:  # Right-left rotate at the node if its right subtree is higher and its right child's left subtree is higher
                    node.right = self._rotate_right(node.right)
                    node = self._rotate_left(node)
            elif self._balance_factor(node) > 1:
                # Right rotate at the node if its left subtree is higher and its left child's left subtree is higher or equal
                if self._balance_factor(node.left) >= 0:
                    node = self._rotate_right(node)
                else:  # Left-right rotate at the node if its left subtree is higher and its left child's right subtree is higher
                    node.left = self._rotate_left(node.left)
                    node = self._rotate_right(node)
            node = node.parent  # Move up to the parent node

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
        tree = AVL(case)
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
        ((1, 2, 3), 1),  
        ((1, 2, 3), 2),  
        ((1, 2, 3), 3),  
        ((50, 40, 60, 30, 70, 20, 80, 45), 0),
        ((50, 40, 60, 30, 70, 20, 80, 45), 45),  
        ((50, 40, 60, 30, 70, 20, 80, 45), 40),  
        ((50, 40, 60, 30, 70, 20, 80, 45), 30),  
    )
    for case, del_value in test_cases:
        tree = AVL(case)
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