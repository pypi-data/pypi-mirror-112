# Bubble Sort Python

Bubble Sort Python is a Python module for dealing with bubble sort needs in python. Although python already has an in-built sort mechanism — `sort()` I thought this would be a fun project!

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install Bubble Sort Python.

```bash
pip install bubble-sorter
```

## Usage

##Basic Sorting

```python
from bubble_sorter import *

sort(2, 1, 3, 19, 8, 4) # returns [1, 2, 3, 4, 8, 19]
sort('goose', 'duck', 'cow', 'chicken', 'horse') # returns ['chicken', 'cow', 'duck', 'goose', 'horse']
rev_sort(2, 1, 3, 19, 8, 4, order = 'desc') # returns [19, 8, 4, 3, 2, 1]

```

##Using Speed Test

```python
from bubble_sorter import *

speed_test(n) # n is a positional argument and is the number of values you want to sort in the speed test. The function tells you the amount of time it took to complete the test sort.
```

## More Options: type, range, order, verbose
``` python
speed_test(n, type = 'str') 
speed_test(n, type = 'int') # default

# type is a keyword argument. You can make it equal to 'str' or 'int' which is the default. Using type = 'str' sorts random words from a collection of the 10,000 most common English words. type = 'int' sorts n numbers between 0 and 99 if no range is specified.

speed_test(n, range = (1, 10)) # this sorts n numbers between 1 and 10 and returns the time taken

# range is a keyword argument. You can make it equal to any tuple. The default is (0, 99). It defines the range of random numbers that will be generated for the speed test.

speed_test(n, order = 'asc') # default
speed_test(n, order = 'desc')

# order is a keyword argument. You can make it equal to 'asc' (ascending order) or 'desc' (descending order). The default is 'asc'. It defines the order in which the list will be sorted. 

speed_test(n, verbose = True)
speed_test(n, verbose = False) # default

# verbose is a keyword argument. You can make it equal to True or False. The default is False and does not print the sorted list. Use it to print or not pront the sorted list. 

```

## Support/Contributions
Raise an issue [here](https://github.com/MasterJindu/Bubble-Sort-Python/issues)

## License
[MIT](https://github.com/MasterJindu/Bubble-Sort-Python/blob/main/LICENSE)