<h1 align="center">Python Data Structures</h1>
<h4 align="center">For all of your data structure needs</h4>

# Table of Contents
1. [About](#about)
2. [Getting Started](#getting-started)
3. [Data Structures](#data-structures)
    * [Stack](#stack)
    * [Queue](#queue)
    * [Tree](#tree)
    * [Binary Search Tree](#binary-search-tree)
    * [Linked List](#linked-list)
4. [Contact](#contact)

# About
A Python package that contains common data structures. Data structures within this package also contain associated search and sorting algorithms. The intention of this package is mostly a learning endeavor but, it may also be used for various build purposes. I hope you find it easy to understand and interact with. If you have any questions or comments, please feel free to [reach out](#contact).

# Getting Started
Further information regarding this package can be found on the Python Package Index website, [pypi.org/pydatastructs](https://pypi.org/project/pydatastructs/).
## Installation
To get started, install the package:
```console
user@machine:~/$ pip install pydatastructs
```

Then, import it into your project:
```python
from pydatastructs import Stack, Queue, Tree, BinarySearchTree, LinkedList
my_stack = Stack(collection=[1, '2', {'3': 3}])
my_queue = Queue(collection=[4.4, [5], (6)])
my_tree = Tree(value='I am Groot')
my_binarysearchtree = BinarySearchTree(value=10)
my_linkedlist = LinkedList(value='HEAD')
```

# Data Structures
## Stack
A list or array based data structure with last-in-first-out (LIFO) properties.
### Methods
- get()
- length()
- is_empty()
- push()
- pop()
- merge_sort()
## Queue
A list or array based data structure with first-in-first-out (FIFO) properties.
### Methods
- get()
- length()
- is_empty()
- enqueue()
- dequeue()
- merge_sort()
## Tree
A node based data structure where each node contains a value property and a children property. The children property is a collection of child nodes. Finally, each node itself is a tree or sub-tree.
### Methods
- add()
- contains()
- depth_first_traversal()
- breadth_first_traversal()
## Binary Search Tree
A node based data structure where each node contains a value property and, a left and right property. The left and right properties point to potential child nodes. The left node's value will always be less than the parent node's value. The right node's value will always be greater than the parent node's value. Finally, each node itself is a tree or sub-tree.
### Methods
- insert()
- contains()
- depth_first_traversal()
- breadth_first_traversal()
## Linked List
A node based data structure containing a head and tail property. The head points to the root node and, the tail points to the last node in the linked list. Each node has a value property and a next property, which points to the next node in the linked list.
### Methods
- append()
- remove_head()
- find_node()

# Contact
For support, feedback or, to report a bug, you may contact the maintainer:
- Yoshio Hasegawa: [GitHub](https://github.com/yoshiohasegawa), [LinkedIn](https://www.linkedin.com/in/yoshiohasegawa/)

## License
Distributed under the MIT License.