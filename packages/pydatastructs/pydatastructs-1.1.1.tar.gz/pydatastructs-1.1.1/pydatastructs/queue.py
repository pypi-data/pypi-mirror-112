#*****************************************************************************
# Programmer: Yoshio Hasegawa
# Class Name: Queue
#
# Revision     Date                        Release Comment
# --------  ----------  ------------------------------------------------------
#   1.0     07/05/2021   Initial Release
#
# File Description
# ----------------------------------------------------------------------------
# This is a class for the Queue data structure. It is an iterable data
# structure where items can be added (enqueue) and removed (dequeue). Items 
# are added to the end of the queue and, items are removed from the from of
# the queue.
#
# Class Methods
# ----------------------------------------------------------------------------
#    Name                                       Description
# ----------                  ------------------------------------------------
# __init__                    Constructor
# get                         Returns the queue collection
# length                      Returns the number of items in the queue
# is_empty                    Verifies if the queue is empty, or not
# enqueue                     Adds an item to the end of the queue
# dequeue                     Removes an item from the front of the queue
#*****************************************************************************
# Imported Packages:
from typing import TypeVar

T = TypeVar('T')

class Queue:
    """
    An iterable data structure or collection that may contain multiple data types.
    If no argument is given, the constructor creates a new empty queue.
    """

    def __init__(self, collection=[]):
        """
        An iterable data structure or collection that may contain multiple data types.
        If no argument is given, the constructor creates a new empty queue.

        Args:
            collection (list, optional): A list to initialize the queue with. Defaults to [].
        """
        if isinstance(collection, list):
            self._queue = collection
        else:
            raise TypeError('Argument \'collection\' must be of type list.')
    
    def get(self) -> list:
        """
        This method is used to return the queue.

        Returns:
            list: Queue containing all data.
        """
        return self._queue
    
    def length(self) -> int:
        """
        This method is used to get the length of the queue.

        Returns:
            int: The number of items in the queue.
        """
        return len(self._queue)
    
    def is_empty(self) -> bool:
        """
        This method is used to check whether the queue is empty or not.

        Returns:
            bool: True if the queue is empty. Otherwise, False.
        """
        if self._queue == []:
            return True
        else:
            return False
    
    def enqueue(self, val: T) -> None:
        """
        This method is used to add items to the end (left) of the queue.

        Args:
            val (T): An item of any data type.
        """
        self._queue = [val] + self._queue
    
    def dequeue(self) -> T:
        """
        This method is used to remove an item from the front (right) of the queue.

        Raises:
            IndexError: Raised when there are no items to remove.

        Returns:
            T: The removed item.
        """
        if self._queue == []:
            raise IndexError('Index out of range, the queue is empty.')
        else:
            item = self._queue.pop()
            return item