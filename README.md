
# Borg Sort

Borg Sort is a custom sorting algorithm that I made at 4 in the morning because I was missing my girlfriend. It combines splitting, local sorting, and merging to complete sorting. 
This github provides the resources necessary to import my algorithm as a python package to impliment for your project.

## Installation

Install command:

```
pip install git+https://github.com/webwizarding/borg_sort.git
```

## Usage

```python
from borg_sort import borg_sort

data = [5, 3, 8, 4, 2, 7, 1, 10]
sorted_data = borg_sort(data)
print(sorted_data)
```

## License

 [LICENSE](LICENSE)
