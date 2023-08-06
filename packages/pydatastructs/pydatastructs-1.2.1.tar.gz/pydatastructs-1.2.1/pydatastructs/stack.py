#*****************************************************************************
# Programmer: Yoshio Hasegawa
# Class Name: Stack
# Parent Class: List
#
# Revision     Date                        Release Comment
# --------  ----------  ------------------------------------------------------
#   1.0     07/05/2021   Initial Release
#
# File Description
# ----------------------------------------------------------------------------
# This is a class for the Stack data structure. It is an iterable data
# structure where items can be added (push) and removed (pop). Items are added
# to the top of the stack and, items are removed from the top of the stack.
#
# Class Methods
# ----------------------------------------------------------------------------
#    Name                                       Description
# ----------                  ------------------------------------------------
# __init__                    Constructor
# get                         Returns the stack collection
# length                      Returns the number of items in the stack
# is_empty                    Verifies if the stack is empty, or not
# push                        Adds an item to the top of the stack
# pop                         Removes an item from the top of the stack
#*****************************************************************************
# Importing parent class List
from .list import List
# Imported Packages:
from typing import TypeVar

T = TypeVar('T')

class Stack(List):
    """
    An iterable data structure or collection that may contain multiple data types.
    If no argument is given, the constructor creates a new empty stack.
    """

    def __init__(self, collection: list=[]):
        """
        An iterable data structure or collection that may contain multiple data types.
        If no argument is given, the constructor creates a new empty stack.

        Args:
            collection (list, optional): A list to initialize the stack with. Defaults to [].
        """
        List.__init__(self, collection=collection)

    def push(self, val: T) -> None:
        """
        This method is used to add items to the top of the stack.

        Args:
            val (T): An item of any data type.
        """
        self._data.append(val)
    
    def pop(self) -> T:
        """
        This method is used to remove an item from the top of the stack.

        Raises:
            IndexError: Raised when there are no items to remove.

        Returns:
            T: The removed item.
        """
        if self._data == []:
            raise IndexError('Index out of range, the stack is empty.')
        else:
            item = self._data.pop()
            return item