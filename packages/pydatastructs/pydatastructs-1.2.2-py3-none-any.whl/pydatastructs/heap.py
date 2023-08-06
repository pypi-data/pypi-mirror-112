#*****************************************************************************
# Programmer: Yoshio Hasegawa
# Class Name: Heap
#
# Revision     Date                        Release Comment
# --------  ----------  ------------------------------------------------------
#   1.0     07/09/2021   Initial Release
#
# File Description
# ----------------------------------------------------------------------------
# This is a parent class inherited by the Max Heap and Min Heap data 
# structures. It contains the _array property used by both MaxHeap and MinHeap,
# which is a list representing the heaps. It also contains some shared methods
# used to get or set/alter the data structure.
#
# Useful formulas:
# For a given node at index i...
# The parent node index = (i - 1) // 2
# The left child node index = (2 * i) + 1
# The right child node index = (2 * i) + 2
#
# Class Methods
# ----------------------------------------------------------------------------
#    Name                                       Description
# ----------                  ------------------------------------------------
# __init__                    Constructor
# get                         Returns the array
# _swap                       Swaps two values within the heap
#*****************************************************************************
# Imported Packages:
from typing import Optional

class Heap:
    """
    A class containing an _array property which contains a list. This class
    also contains methods used to get or set/alter the list. The contained
    methods are specific to a heap data structure. If no argument is given,
    the constructor assigns a new empty list to the _array property.
    """

    def __init__(self, collection: Optional[list]=None):
        """
        A class containing an _array property which contains a list. This class
        also contains methods used to get or set/alter the list. The contained
        methods are specific to a heap data structure. If no argument is given,
        the constructor assigns a new empty list to the _array property.

        Args:
            collection (Optional[list], optional): A list to initialize the _array
            property with. Defaults to None.

        Raises:
            TypeError: Raised when provided a non-list data type as an argument.
        """
        if isinstance(collection, list):
            self._array = collection
        elif collection is None:
            self._array = []
        else:
            raise TypeError('Argument \'collection\' must be of type list.')
    
    def get(self) -> list:
        """
        This method is used to return the array representing the heap.

        Returns:
            list: array containing all data represented in the heap.
        """
        return self._array
    
    def _swap(self, idx1: int, idx2: int) -> None:
        """
        This method is used to swap two values within the heap, at two 
        provided indices.

        Args:
            idx1 (int): Index location for the first value.
            idx2 (int): Index location for the second value.
        """
        temp_value = self._array[idx1]
        self._array[idx1] = self._array[idx2]
        self._array[idx2] = temp_value