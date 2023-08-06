#*****************************************************************************
# Programmer: Yoshio Hasegawa
# Class Name: BinarySearchTree
#
# Revision     Date                        Release Comment
# --------  ----------  ------------------------------------------------------
#   1.0     07/06/2021   Initial Release
#
# File Description
# ----------------------------------------------------------------------------
# This is a class for the Binary Search Tree data structure. It is a data 
# structure containing nodes. When this class is instantiated, the root node
# is created. Each node has a value property and, a left and right property.
# The left and right properties point to the left and right child nodes. The 
# left child node will always have a value that is less than its parent's 
# value. Additionally, the right child node will always have a value that is
# greater than its parent's value. Each child node is a sub-binarysearchtree.
#
# Class Methods
# ----------------------------------------------------------------------------
#    Name                                       Description
# ----------                  ------------------------------------------------
# __init__                    Constructor
# insert                      Adds a node in the appropriate place
# contains                    Verifies if a value is in the tree, or not
# depth_first_traversal       Runs a callback on every node, depth first
# breadth_first_traversal     Runs a callback on every node, breadth first
#*****************************************************************************
# Importing PEP 563 -- Postponed Evaluation of Annotations
from __future__ import annotations
# Imported Packages:
from typing import TypeVar, Optional, Callable

T = TypeVar('T')

class BinarySearchTree:
    """
    A node-based data structure where each node has a value and, left and right
    properties that point to child nodes (child nodes can be None). The left
    node\'s value will always be less than the parent node\'s value. The right node\'s
    value will always be greater than the parent node\'s value.
    """

    def __init__(self, value: T):
        """
        A node-based data structure where each node has a value and, left and right
        properties that point to child nodes (child nodes can be None). The left
        node\'s value will always be less than the parent node\'s value. The right node\'s
        value will always be greater than the parent node\'s value.

        Args:
            value (T): A value to initialize the root node value property with.
        """
        self.value = value
        self.left: Optional[BinarySearchTree] = None
        self.right: Optional[BinarySearchTree] = None
    
    def insert(self, value: T) -> BinarySearchTree:
        """
        This method adds a child node to this Binary Search Tree in the appropriate place.

        Args:
            value (T): A value to initialize the created child node with.

        Returns:
            BinarySearchTree: This entire Binary Search Tree (root node).
        """
        def traverse(node: BinarySearchTree) -> BinarySearchTree:
            if value == node.value:
                return self
            elif value < node.value:
                if node.left:
                    return traverse(node.left)
                else:
                    node.left = BinarySearchTree(value)
                    return self
            elif value > node.value:
                if node.right:
                    return traverse(node.right)
                else:
                    node.right = BinarySearchTree(value)
                    return self
        
        return traverse(self)
    
    def contains(self, value: T) -> bool:
        """
        This method verifies whether a value is within this Binary Search Tree, or not.

        Args:
            value (T): The value to search for.

        Returns:
            bool: True if the value was found. Otherwise, False.
        """
        def traverse(node: BinarySearchTree) -> bool:
            if value == node.value:
                return True
            elif value < node.value:
                if node.left:
                    return traverse(node.left)
                else:
                    return False
            elif value > node.value:
                if node.right:
                    return traverse(node.right)
                else:
                    return False
        
        return traverse(self)

    def depth_first_traversal(self, callback: Callable[[BinarySearchTree], None]) -> None:
        """
        This method is used to run a callback function on every node within this tree
        in a depth first manner, in order.

        Args:
            callback (Callable[[BinarySearchTree], None]): The callback function to be run on each node.
        """
        nodes_to_visit = []
        nodes_to_visit.append(self)

        while nodes_to_visit:
            temp_node = nodes_to_visit.pop()
            callback(temp_node)

            # Appending child nodes in reverse order (right then left) to traverse
            # depth first, from left to right. More specifically, the nodes will be visited 
            # in ascending order based on The visual example provided below.
            # tree: 
            #            1
            #        /      \
            #      2         5
            #   /    \     /   \
            #  3      4   6     7
            if temp_node.right:
                nodes_to_visit.append(temp_node.right)
            if temp_node.left:
                nodes_to_visit.append(temp_node.left)
    
    def breadth_first_traversal(self, callback: Callable[[BinarySearchTree], None]) -> None:
        """
        This method is used to run a callback function on every node within this tree
        in a breadth first manner, in order.

        Args:
            callback (Callable[[BinarySearchTree], None]): The callback function to be run on each node.
        """
        nodes_to_visit = []
        nodes_to_visit.append(self)

        while nodes_to_visit:
            temp_node = nodes_to_visit.pop()
            callback(temp_node)

            # Enqueuing child nodes in order (left then right) to traverse
            # breadth first, from left to right. More specifically, the nodes will be visited 
            # in ascending order based on The visual example provided below.
            # tree: 
            #            1
            #        /      \
            #      2         3
            #   /    \     /   \
            #  4      5   6     7
            if temp_node.left:
                nodes_to_visit = [temp_node.left] + nodes_to_visit
            if temp_node.right:
                nodes_to_visit = [temp_node.right] + nodes_to_visit