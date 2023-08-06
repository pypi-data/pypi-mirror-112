#*****************************************************************************
# Programmer: Yoshio Hasegawa
# Class Name: MinHeap
# Parent Class: Heap
#
# Revision     Date                        Release Comment
# --------  ----------  ------------------------------------------------------
#   1.0     07/09/2021   Initial Release
#
# File Description
# ----------------------------------------------------------------------------
# This is a class for the Min Heap data structure. It is a complete binary
# tree, where all parent node's values are less than or equal to their child
# node's values. This data structure is represented by an array and, each node
# is represented by the value of an element in the array.
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
# __build                     Heapifies the min heap after removal of a node
# insert                      Adds a node in the appropriate place
# remove_min                  Removes and returns the min value node
#*****************************************************************************
# Importing parent class List
from pydatastructs.heap import Heap
# Imported Packages:
from typing import TypeVar, Optional

T = TypeVar('T')

class MinHeap(Heap):
    """
    A complete binary tree data structure represented as an array. Every parent
    node's value is less than or equal to their child node's values. If no
    argument is given, the constructor creates a new empty min heap. If an
    argument is provided, the constructor will alter (heapify) the collection
    to ensure that the min heap properties hold.
    """

    def __init__(self, collection: Optional[list]=None):
        """
        A complete binary tree data structure represented as an array. Every parent
        node's value is less than or equal to their child node's values. If no
        argument is given, the constructor creates a new empty min heap. If an
        argument is provided, the constructor will alter (heapify) the collection
        to ensure that the min heap properties hold.

        Args:
            collection (Optional[list], optional): A list to initialize the min heap
            with. Defaults to None.
        """
        if isinstance(collection, list):
            super().__init__(collection=[])
            # If a valid collection is provided,
            # construct the min heap with the collection
            for value in collection:
                self.insert(value)
        elif collection is None:
            super().__init__(collection=[])
        else:
            raise TypeError('Argument \'collection\' must be of type list.')
    
    def __build(self) -> None:
        """
        This method is used to re-build the min heap when an element is removed,
        to ensure that the min heap properties hold.
        """
        parent_idx = 0
        left_idx = 1
        right_idx = 2
        length = len(self._array)

        # While the bottom/end of the min heap has not been reached
        while left_idx < length or right_idx < length:

            # initialize the child_idx to the child with the smaller value
            if right_idx < length:
                child_idx = right_idx if self._array[left_idx] > self._array[right_idx] else left_idx
            else:
                child_idx = left_idx

            # Swap the parent and child if the child's value is smaller than the parent's value
            if self._array[child_idx] < self._array[parent_idx]:
                self._swap(parent_idx, child_idx)
                parent_idx = child_idx
                right_idx = (2 * child_idx) + 2
                left_idx = (2 * child_idx) + 1
            # Otherwise, break out of the while loop
            else:
                break
    
    def insert(self, value: T) -> None:
        """
        This method adds a child node to this min heap in the appropriate place.

        Args:
            value (T): The value to be added to this min heap.
        """
        if self._array == []:
            self._array.append(value)
        else:
            parent_idx = (len(self._array) - 1) // 2
            curr_idx = len(self._array)
            self._array.append(value)
 
            # While the value to be inserted is less than it's parent,
            # keep swapping the parent and child from the bottom up until
            # the min heap properties hold or, until swapped with the root node.
            while value < self._array[parent_idx] and parent_idx >= 0:
                temp_value = self._array[parent_idx]
                self._array[parent_idx] = value
                self._array[curr_idx] = temp_value
                curr_idx = parent_idx
                parent_idx = (parent_idx - 1) // 2

    def remove_min(self) -> Optional[T]:
        """
        This method removes and returns the min value from the min heap and,
        re-builds the heap so that the min heap properties hold.

        Returns:
            Optional[T]: The min value, or None if there are no nodes in the min heap.
        """
        if self._array == []:
            return None
        else:
            # Remove top node
            value = self._array[0]
            self._array = self._array[1:]
            # If nodes remaing in the min heap...
            if self._array:
                # Move end node to the top
                end_node = self._array.pop()
                self._array = [end_node] + self._array
                # Rebuild the heap (heapify)
                self.__build()
            # Return the top node
            return value
                
