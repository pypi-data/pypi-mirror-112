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
# contains                    Verifies if a value is in the sub-tree, or not
#*****************************************************************************
# Imported Packages:
from typing import TypeVar

T = TypeVar('T')

class Tree:
    """
    A node-based data structure where each node has a value and children property.
    If no argument is given, the constructor creates a root node with a value of None.
    An empty children collection is created regardless of an argument being provided.
    """

    def __init__(self, value: T=None):
        """
        A node-based data structure where each node has a value and children property.
        If no argument is given, the constructor creates a root node with a value of None.
        An empty children collection is created regardless of an argument being provided.

        Args:
            value (T, optional): A value to initialize the root node value property with. Defaults to None.
        """
        self.value = value
        self.children = []
    
    def add(self, value: T=None) -> None:
        """
        This method adds a child node to the children collection owned by this node.

        Args:
            value (T, optional): A value to initialize the created child node with. Defaults to None.
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