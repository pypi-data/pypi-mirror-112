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
# left child node will always have a value that is less than its parents 
# value. Additionally, the right child node will always have a value that is
# greater than its parents value. Each child node is a sub-binarysearchtree.
#
# Class Methods
# ----------------------------------------------------------------------------
#    Name                                       Description
# ----------                  ------------------------------------------------
# __init__                    Constructor
#*****************************************************************************
# Importing PEP 563 -- Postponed Evaluation of Annotations
from __future__ import annotations
# Imported Packages:
from typing import TypeVar

T = TypeVar('T')

class BinarySearchTree:
    """
    A node-based data structure where each node has a value and, left and right
    properties that point to child nodes (child nodes can be None). The left
    nodes value will always be less than the parent nodes value. The right nodes
    value will always be greater than the parent nodes value. If no argument is
    given, the constructor creates a root node with a value of None.
    """

    def __init__(self, value: T=None):
        """
        A node-based data structure where each node has a value and, left and right
        properties that point to child nodes (child nodes can be None). The left
        nodes value will always be less than the parent nodes value. The right nodes
        value will always be greater than the parent nodes value. If no argument is
        given, the constructor creates a root node with a value of None.

        Args:
            value (T, optional): A value to initialize the root node value property with. Defaults to None.
        """
        self.value = value
        self.left = None
        self.right = None
    
    def insert(self, value: T=None) -> BinarySearchTree:
        """
        This method adds a child node to this Binary Search Tree in the appropriate place.

        Args:
            value (T, optional): A value to initialize the created child node with. Defaults to None.

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