#*****************************************************************************
# Programmer: Yoshio Hasegawa
# Class Name: Queue
# Parent Class: List
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
# enqueue                     Adds an item to the end of the queue
# dequeue                     Removes an item from the front of the queue
#*****************************************************************************
# Importing parent class List
from pydatastructs.list import List
# Imported Packages:
from typing import TypeVar, Optional

T = TypeVar('T')

class Queue(List):
    """
    An iterable data structure or collection that may contain multiple data types.
    If no argument is given, the constructor creates a new empty queue.
    """

    def __init__(self, collection: Optional[list]=None):
        """
        An iterable data structure or collection that may contain multiple data types.
        If no argument is given, the constructor creates a new empty queue.

        Args:
            collection (Optional[list], optional): A list to initialize the queue with.
            Defaults to None.
        """
        super().__init__(collection=collection)
    
    def enqueue(self, val: T) -> None:
        """
        This method is used to add items to the end (left) of the queue.

        Args:
            val (T): An item of any data type.
        """
        self._data = [val] + self._data
    
    def dequeue(self) -> T:
        """
        This method is used to remove an item from the front (right) of the queue.

        Raises:
            IndexError: Raised when there are no items to remove.

        Returns:
            T: The removed item.
        """
        if self._data == []:
            raise IndexError('Index out of range, the queue is empty.')
        else:
            item = self._data.pop()
            return item