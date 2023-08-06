#*****************************************************************************
# Programmer: Yoshio Hasegawa
# Class Name: Tree
#
# Revision     Date                        Release Comment
# --------  ----------  ------------------------------------------------------
#   1.0     07/05/2021   Initial Release
#
# File Description
# ----------------------------------------------------------------------------
# This is a class for the Tree data structure. It is a data structure 
# containing nodes. When this class is instantiated, the root node is created.
# Each node has a value property and, a collection of child nodes within the
# children property. Each child node is a sub-tree. There is no limit to the
# number of child nodes for each parent node.
#
# Class Methods
# ----------------------------------------------------------------------------
#    Name                                       Description
# ----------                  ------------------------------------------------
# __init__                    Constructor
# add                         Adds a node to the children collection
# contains                    Verifies if a value is in the tree, or not
# depth_first_traversal       Runs a callback on every node, depth first
# breadth_first_traversal     Runs a callback on every node, breadth first
#*****************************************************************************
# Importing PEP 563 -- Postponed Evaluation of Annotations
from __future__ import annotations
# Imported Packages:
from typing import TypeVar, List, Callable

T = TypeVar('T')

class Tree:
    """
    A node-based data structure where each node has a value and children property.
    When thic class is instantiated, an empty children collection is created.
    """

    def __init__(self, value: T):
        """
        A node-based data structure where each node has a value and children property.
        When thic class is instantiated, an empty children collection is created.

        Args:
            value (T): A value to initialize the root node value property with.
        """
        self.value = value
        self.children: List[Tree] = []
    
    def add(self, value: T) -> None:
        """
        This method adds a child node to the children collection owned by this node.

        Args:
            value (T): A value to initialize the created child node with.
        """
        child_node = Tree(value)
        self.children.append(child_node)
    
    def contains(self, value: T) -> bool:
        """
        This method verifies whether a value is within this Tree, or not.

        Args:
            value (T): The value to search for.

        Returns:
            bool: True if the value was found. Otherwise, False.
        """
        def traverse(children: list) -> bool:
            for node in children:
                if node.value == value:
                    return True
                else: 
                    if traverse(node.children):
                        return True
        
        if self.value == value:
            return True
        elif traverse(self.children):
            return True
        else:
            return False
    
    def depth_first_traversal(self, callback: Callable[[Tree], None]) -> None:
        """
        This method is used to run a callback function on every node within this tree
        in a depth first manner, in order.

        Args:
            callback (Callable[[Tree], None]): The callback function to be run on each node.
        """
        nodes_to_visit = []
        nodes_to_visit.append(self)

        while nodes_to_visit:
            temp_node = nodes_to_visit.pop()
            callback(temp_node)

            # Appending child nodes in reverse order (right to left) to traverse
            # depth first, from left to right. More specifically, the nodes will be visited 
            # in ascending order based on The visual example provided below.
            # tree: 
            #            1
            #        /      \
            #      2         5
            #   /    \     /   \
            #  3      4   6     7
            for idx in range(len(temp_node.children) -1, -1, -1):
                nodes_to_visit.append(temp_node.children[idx])
    
    def breadth_first_traversal(self, callback: Callable[[Tree], None]) -> None:
        """
        This method is used to run a callback function on every node within this tree
        in a breadth first manner, in order.

        Args:
            callback (Callable[[Tree], None]): The callback function to be run on each node.
        """
        nodes_to_visit = []
        nodes_to_visit.append(self)

        while nodes_to_visit:
            temp_node = nodes_to_visit.pop()
            callback(temp_node)

            # Enqueuing child nodes in order (left to right) in order to traverse
            # breadth first, from left to right. More specifically, the nodes will be visited 
            # in ascending order based on The visual example provided below.
            # tree: 
            #            1
            #        /      \
            #      2         3
            #   /    \     /   \
            #  4      5   6     7
            for node in temp_node.children:
                nodes_to_visit = [node] + nodes_to_visit
