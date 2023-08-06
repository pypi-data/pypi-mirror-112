# nindex

Classes to provide efficient indexing and slicing operations into a list of objects by certain attribute key.

## Installation

```bash
pip install ninstall
```

## Usage

1. Create your list of objects:
```python
class Item():
    def __init__(self, value, name):
        self.value = value
        self.name = name

items = [
    Item(1, "alpha"),
    Item(3, "beta"),
    Item(8, "gamma"),
    Item(22, "delta")
]
```

2. Wrap the list in a new Index, and specify which attribute will be the key:
```python
from nindex import Index
itemindex = Index(items, "value")
```

3. Quickly look up objects by attribute key:
```python
 # Look for the object with this exact value
item = itemindex[3]
print(item.name)
# 'beta'

# Look for the closest object with less than or equal to this value
item = itemindex.le(20)
print(item.name)
# 'gamma'

# Look for all objects with values in the given range
items = itemindex[2:22] #
for item in items:
    print(item.name)
# 'beta'
# 'gamma'
```

## Limitations

This with *only* work if:
- The list is sorted
- The list doesn't change
- The keyed attributes don't change
- The keyed attributes contain no duplicate values
