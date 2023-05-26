import unittest
from main import *

class TestAVLTree(unittest.TestCase):

    def setUp(self):
        self.avl_tree = AVL()

    def test_add(self):
        values = [3, 4, 8, 9, 15, 17, 19, 23, 24, 25, 26, 28]
        for value in values:
            self.avl_tree.add(value)
        self.assertEqual(str(self.avl_tree), "AVL pre-order { 23, 9, 4, 3, 8, 17, 15, 19, 25, 24, 26, 28 }")

    def test_remove(self):
        values = [3, 4, 8, 9, 15, 17, 19, 23, 24, 25, 26, 28]
        for value in values:
            self.avl_tree.add(value)
        self.avl_tree.remove(23)
        self.assertEqual(str(self.avl_tree), "AVL pre-order { 24, 9, 4, 3, 8, 17, 15, 19, 26, 25, 28 }")
    
    def test_contains(self):
        values = [3, 4, 8, 9, 15, 17, 19, 23, 24, 25, 26, 28]
        for value in values:
            self.avl_tree.add(value)
        self.assertTrue(self.avl_tree.contains(15))
        self.assertFalse(self.avl_tree.contains(1))

    def test_is_valid_avl(self):
        values = [3, 4, 8, 9, 15, 17, 19, 23, 24, 25, 26, 28]
        for value in values:
            self.avl_tree.add(value)
        self.assertTrue(self.avl_tree.is_valid_avl())
    
    def test_get_height(self):
        values = [3, 4, 5]
        for value in values:
            self.avl_tree.add(value)
        self.assertEqual(self.avl_tree._get_height(self.avl_tree._root), 1)

    def test_get_height_(self):
        values = [3, 4, 8, 9, 15, 17, 19, 23, 24, 25, 26, 28]
        for value in values:
            self.avl_tree.add(value)
        self.assertEqual(self.avl_tree._get_height(self.avl_tree._root), 3)

    def test_balance_factor(self):
        values = [3, 4, 8, 9, 15, 17, 19, 23, 24, 25, 26, 28]
        for value in values:
            self.avl_tree.add(value)
        self.assertEqual(self.avl_tree._balance_factor(self.avl_tree._root), 0)

    def test_rotate_left(self):
        self.avl_tree.add(1)
        self.avl_tree.add(2)
        self.avl_tree.add(3)
        assert str(self.avl_tree) == "AVL pre-order { 2, 1, 3 }"

    def test_rotate_right(self):
        self.avl_tree.add(3)
        self.avl_tree.add(2)
        self.avl_tree.add(1)
        assert str(self.avl_tree) == "AVL pre-order { 2, 1, 3 }"

if __name__ == '__main__':
    unittest.main()