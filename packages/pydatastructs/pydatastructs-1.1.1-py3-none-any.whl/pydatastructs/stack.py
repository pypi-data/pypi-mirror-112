#*****************************************************************************
# Programmer: Yoshio Hasegawa
# Class Name: Stack
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
# Imported Packages:
from typing import TypeVar

T = TypeVar('T')

class Stack:
    """
    An iterable data structure or collection that may contain multiple data types.
    If no argument is given, the constructor creates a new empty stack.
    """

    def __init__(self, collection=[]):
        """
        An iterable data structure or collection that may contain multiple data types.
        If no argument is given, the constructor creates a new empty stack.

        Args:
            collection (list, optional): A list to initialize the stack with. Defaults to [].
        """
        if isinstance(collection, list):
            self._stack = collection
        else:
            raise TypeError('Argument \'collection\' must be of type list.')
    
    def get(self) -> list:
        """
        This method is used to return the stack.

        Returns:
            list: Stack containing all data.
        """
        return self._stack
    
    def length(self) -> int:
        """
        This method is used to get the length of the stack.

        Returns:
            int: The number of items in the stack.
        """
        return len(self._stack)
    
    def is_empty(self) -> bool:
        """
        This method is used to check whether the stack is empty or not.

        Returns:
            bool: True if the stack is empty. Otherwise, False.
        """
        if self._stack == []:
            return True
        else:
            return False

    def push(self, val: T) -> None:
        """
        This method is used to add items to the top of the stack.

        Args:
            val (T): An item of any data type.
        """
        self._stack.append(val)
    
    def pop(self) -> T:
        """
        This method is used to remove an item from the top of the stack.

        Raises:
            IndexError: Raised when there are no items to remove.

        Returns:
            T: The removed item.
        """
        if self._stack == []:
            raise IndexError('Index out of range, the stack is empty.')
        else:
            item = self._stack.pop()
            return item