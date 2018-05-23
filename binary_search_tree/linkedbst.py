"""
File: linkedbst.py
Author: Ken Lambert
"""

from binary_search_tree.abstractcollection import AbstractCollection
from binary_search_tree.bstnode import BSTNode
from binary_search_tree.linkedstack import LinkedStack
from binary_search_tree.linkedqueue import LinkedQueue
from math import log


class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            s = ""
            if node != None:
                s += recurse(node.right, level + 1)
                s += "| " * level
                s += str(node.data) + "\n"
                s += recurse(node.left, level + 1)
            return s

        return recurse(self._root, 0)

    def is_root(self, p=None):
        """
        check if p is root or not
        :param p: Node
        :return: bool
        """
        return p == self._root

    def is_leaf(self, p=None):
        """
        check if p is leaf or not
        :param p: Node
        :return: bool
        """
        if p.right is None and p.left is None:
            return True
        return False

    def _children(self, p):
        """
        return tuple with childrens of p
        :param p: Node
        :return: tuple
        """
        if p is not None:
            if p.left is not None and p.right is not None:
                return p.left, p.right
            elif p.left is None and p.right is not None:
                return [p.right]
            elif p.left is not None and p.right is None:
                return [p.left]
        return None

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right != None:
                    stack.push(node.right)
                if node.left != None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node != None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) != None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        def recurse(node):
            if node is None:
                return None
            elif item == node.data:
                return node
            elif item < node.data:
                return recurse(node.left)
            else:
                return recurse(node.right)

        return recurse(self._root)

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""

        # Helper function to search for item's position
        def recurse(node):
            # New item is less, go left until spot is found
            if item < node.data:
                if node.left == None:
                    node.left = BSTNode(item)
                else:
                    recurse(node.left)
            # New item is greater or equal,
            # go right until spot is found
            elif node.right == None:
                node.right = BSTNode(item)
            else:
                recurse(node.right)
                # End of recurse

        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
        # Otherwise, search for the item's spot
        else:
            recurse(self._root)

        self._size += 1

    def _add_right(self, p, k):
        """
        add right
        :param p: BSTNode
        :param k: int or str
        :return: None
        """
        p.right = BSTNode(k)
        self._size += 1

    def _add_left(self, p, k):
        """
        add left
        :param p: BSTNode
        :param k: int or str
        :return: None
        """
        self._size += 1
        p.left = BSTNode(k)

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def liftMaxInLeftSubtreeToTop(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            currentNode = top.left
            while not currentNode.right == None:
                parent = currentNode
                currentNode = currentNode.right
            top.data = currentNode.data
            if parent == top:
                top.left = currentNode.left
            else:
                parent.right = currentNode.left

        # Begin main part of the method
        if self.isEmpty(): return None

        # Attempt to locate the node containing the item
        itemRemoved = None
        preRoot = BSTNode(None)
        preRoot.left = self._root
        parent = preRoot
        direction = 'L'
        currentNode = self._root
        while not currentNode == None:
            if currentNode.data == item:
                itemRemoved = currentNode.data
                break
            parent = currentNode
            if currentNode.data > item:
                direction = 'L'
                currentNode = currentNode.left
            else:
                direction = 'R'
                currentNode = currentNode.right

        # Return None if the item is absent
        if itemRemoved == None: return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not currentNode.left == None \
                and not currentNode.right == None:
            liftMaxInLeftSubtreeToTop(currentNode)
        else:

            # Case 2: The node has no left child
            if currentNode.left == None:
                newChild = currentNode.right

                # Case 3: The node has no right child
            else:
                newChild = currentNode.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = newChild
            else:
                parent.right = newChild

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = preRoot.left
        return itemRemoved

    def replace(self, item, newItem):
        """
        If item is in self, replaces it with newItem and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe != None:
            if probe.data == item:
                oldData = probe.data
                probe.data = newItem
                return oldData
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self, p=None):
        '''
        Return the height of tree
        :param p:
        :return:int
        '''

        def height1(top):
            '''
            Helper function
            :param top:
            :return:
            '''
            if self.is_leaf(p):
                return 0
            else:
                if self._children(top) is None:
                    return 0
                return 1 + max(height1(c) for c in self._children(top))

        if p is None:
            p = self._root
        return height1(p)

    def isBalanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''
        return self.height() <= 2 * log(self._size + 1, 2) - 1

    def rangeFind(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''
        lst = list(self.inorder())
        new_lst = [i for i in lst if i > low and i < high]
        if len(new_lst) == 0:
            return None
        lst = []
        for i in new_lst:
            lst.append(self.find(i))
        return lst

    def rebalance(self):
        '''
        Rebalances the tree.
        :return:
        '''

        def recurse(p, lst):
            """
            make new tree
            :param p: BSTNode
            :param lst: list
            :return: None
            """
            while len(lst) != 0:
                if len(lst) % 2 == 0:
                    new_lst_1 = lst[0:len(lst) // 2]
                    new_lst_2 = lst[len(lst) // 2:]
                    lst = []
                else:
                    new_lst_1 = lst[0:len(lst) // 2 + 1]
                    new_lst_2 = lst[len(lst) // 2 + 1:]
                    lst = []
                item1 = new_lst_1.pop(len(new_lst_1) // 2)
                self._add_left(p, item1)
                recurse(self.find(item1), new_lst_1)
                if len(new_lst_2) != 0:
                    item2 = new_lst_2.pop(len(new_lst_2) // 2)
                    self._add_right(p, item2)
                    recurse(self.find(item2), new_lst_2)

        lst = list(self.inorder())
        self.clear()
        self._root = BSTNode(lst.pop(len(lst) // 2))
        recurse(self._root, lst)

    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return: str or int or None
        """
        lst = list(self.inorder())
        new_lst = [i for i in lst if i > item]
        if len(new_lst) == 0:
            return None
        return self.find(new_lst[0])

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        lst = list(self.inorder())
        new_lst = [i for i in lst if i < item]
        if len(new_lst) == 0:
            return None
        return self.find(new_lst[-1])
