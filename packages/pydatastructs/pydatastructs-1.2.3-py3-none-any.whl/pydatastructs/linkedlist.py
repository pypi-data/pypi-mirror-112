#*****************************************************************************
# Programmer: Yoshio Hasegawa
# Class Name: LinkedList
#
# Revision     Date                        Release Comment
# --------  ----------  ------------------------------------------------------
#   1.0     07/05/2021   Initial Release
#
# File Description
# ----------------------------------------------------------------------------
# This is a class for the Linked List data structure. It is a data structure 
# containing nodes. When this class is instantiated, the head node is created
# only if a value is provided. Additionally, if a value is provided, the tail 
# property will be assigned to the head node since there will only be one node
# to begin with. Otherwise, the head and tail properties are are assigned
# None. Each node has a value property and, a next property which points to
# the next node. 
#
# Class Methods
# ----------------------------------------------------------------------------
#    Name                                       Description
# ----------                  ------------------------------------------------
# __init__                    Constructor
# append                      Adds a node to the end of the linked list
# remove_head                 Removes the head from the linked list
# find_node                   Finds the node with a given value
#*****************************************************************************
# Imported Packages:
from typing import TypeVar, Union, Optional

T = TypeVar('T')

class Node:
    """
    A node object that contains a value and next property.
    """
    def __init__(self, value: T = None):
        """
        A node object that contains a value and next property.

        Args:
            value (T, optional): A value to initialize the node value property
            with. Defaults to None.
        """
        self.value = value
        self.next: Optional[Node] = None


class LinkedList:
    """
    A node-based data structure that contains a head and tail property. The
    head property points to the head node and, the tail points to the tail
    node. Each node has a value and a next property. If no argument is given,
    the constructor assigns None to the head and tail properties.
    """

    def __init__(self, value: T=None):
        """
        A node-based data structure that contains a head and tail property. The
        head property points to the head node and, the tail points to the tail
        node. Each node has a value and a next property. If no argument is given,
        the constructor assigns None to the head and tail properties.

        Args:
            value (T, optional): A value to initialize the head node value property
            with. Defaults to None.
        """
        if value:
            self.head = Node(value)
            self.tail = self.head
        else:
            self.head = None
            self.tail = None
    
    def append(self, value: T=None) -> None:
        """
        This method is used to add a new node to the end of the linked list. If the linked list is empty,
        the new node will become the head and tail.

        Args:
            value (T, optional): A value to initialize the new node value property with. Defaults to None.
        """
        new_node = Node(value)
        if self.head == None:
            self.head = new_node
            self.tail = self.head
        else:
            self.tail.next = new_node
            self.tail = new_node
    
    def remove_head(self) -> Optional[Node]:
        """
        This method is used to remove and return the head of the linked list. Once this method is called,
        the head property will shift and point to the next node in the linked list. If the linked list
        is empty, None will be returned. If the linked list only contains one node, the node will
        be removed and returned. Then, the head and tail property will be assigned None.

        Returns:
            Optional[Node]: The removed head, or None if there are no nodes in the linked list.
        """
        if self.head == None:
            return None
        else:
            removed_head = self.head
            self.head = self.head.next
            if self.head == None:
                self.tail = None
            return removed_head
    
    def find_node(self, value: T) -> Optional[Node]:
        """
        This method finds and returns the first node with the provided value within this linked list.
        Or, if such node does not exist this method will return None.

        Args:
            value (T): The value to search for.

        Returns:
            Optional[Node]: The node with the specified value,
            or None if there are no nodes with the specified value in the linked list.
        """
        def traverse(node) -> Union[Node, bool]:
            if node.value == value:
                return node
            elif node.next:
                return traverse(node.next)
            else:
                return None
            
        if self.head == None:
            return None
        else:
            return traverse(self.head)