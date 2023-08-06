#*****************************************************************************
# Programmer: Yoshio Hasegawa
# Class Name: List
#
# Revision     Date                        Release Comment
# --------  ----------  ------------------------------------------------------
#   1.0     07/07/2021   Initial Release
#
# File Description
# ----------------------------------------------------------------------------
# This is a parent class inherited by the Stack and Queue data structures. It
# contains the _data property used by both Stack and Queue, which is a list.
# It also contains some shared methods used to get or set/alter the data
# structure.
#
# Class Methods
# ----------------------------------------------------------------------------
#    Name                                       Description
# ----------                  ------------------------------------------------
# __init__                    Constructor
# get                         Returns the collection
# length                      Returns the number of items in the collection
# is_empty                    Verifies if the collection is empty, or not
# merge_sort                  Sorts the collection in asc or desc order
#*****************************************************************************
# Imported Packages:
from typing import Optional

class List:
    """
    A class containing a _data property which contains a list. This class
    also contains methods used to get or set/alter the list. The contained
    methods are specific to a stack or queue data structure. If no argument
    is given, the constructor creates a new empty list.
    """

    def __init__(self, collection: Optional[list]=None):
        """
        A class containing a _data property which contains a list. This class
        also contains methods used to get or set/alter the list. The contained
        methods are specific to a stack or queue data structure. If no argument
        is given, the constructor creates a new empty list.

        Args:
            collection (Optional[list], optional): A list to initialize the _data
            property with. Defaults to None.

        Raises:
            TypeError: Raised when provided a non-list data type as an argument.
        """
        if isinstance(collection, list):
            self._data = collection
        elif collection is None:
            self._data = []
        else:
            raise TypeError('Argument \'collection\' must be of type list.')
    
    def get(self) -> list:
        """
        This method is used to return the collection.

        Returns:
            list: collection containing all data.
        """
        return self._data
    
    def length(self) -> int:
        """
        This method is used to get the length of the collection.

        Returns:
            int: The number of items in the collection.
        """
        return len(self._data)
    
    def is_empty(self) -> bool:
        """
        This method is used to check whether the collection is empty or not.

        Returns:
            bool: True if the collection is empty. Otherwise, False.
        """
        if self._data == []:
            return True
        else:
            return False
    
    def merge_sort(self, order: str='asc') -> None:
        """
        This method is used to sort the collection in ascending or descending order.
        The sorting algorithm used in this case is the merge sort method.

        Args:
            order (str, optional): The order in which to sort the collection. Defaults to 'asc'.
            Acceptable values are 'asc' and 'desc' only.

        Raises:
            TypeError: Raised when provided a non-string data type as an argument.
            ValueError: Raised when provided with a value other than 'asc' or 'desc'.
        """
        if not isinstance(order, str):
            raise TypeError('Argument \'order\' must be of type string.')
        if order not in ['asc', 'desc']:
            raise ValueError('Argument \'order\' must equal either \'asc\' or \'desc\'.')

        # This function begins the sorting algorithm by splitting the collection
        # in half recursively until it reaches a list of 1 element. 
        # Then, the function passes both left and right sides to the 
        # merge_collections function to be merged back together.
        def split_and_sort(collection: list) -> list:
            length = len(collection)
            # Note that the base case is the collection length equaling one 
            # because, by definition a list of 1 element is sorted.
            if length == 1:
                return collection
            else:
                half = length // 2
                left = collection[:half]
                right = collection[half:]
                sorted_left = split_and_sort(left)
                sorted_right = split_and_sort(right)
                return merge_collections(sorted_left, sorted_right, order)
        
        # This function merges the left and right sides together in
        # either ascending or descending order.
        def merge_collections(left: list, right: list, order: str) -> list:
            sorted_list = []

            # Continue merging until either left or right is empty.
            while left and right:
                if order == 'asc':
                    if left[0] <= right[0]:
                        sorted_list.append(left[0])
                        left = left[1:]
                    else:
                        sorted_list.append(right[0])
                        right = right[1:]
                else:
                    if left[0] >= right[0]:
                        sorted_list.append(left[0])
                        left = left[1:]
                    else:
                        sorted_list.append(right[0])
                        right = right[1:]

            # Any remaining elements from either left or right can be 
            # safely extended to the end since, any remaining values will
            # already be sorted correctly.
            if left or right:
                sorted_list.extend(left + right)
            
            return sorted_list
        
        # Begin the sorting algorithm if _data is not empty.
        if self._data == []:
            return
        else:
            sorted_data = split_and_sort(self._data)
            self._data = sorted_data