# anodict: annotated dict

[![Pyversions](https://img.shields.io/pypi/pyversions/anodict.svg?style=flat-square)](https://pypi.org/project/anodict/)

Convert a `dict` to an annotated object.

# Usage

## Installation

```shell
pip install anodict
```

## Example

```python
import anodict


class Person:
    name: str
    age: int

person = anodict.dict_to_class({
    "name": "bob",
    "age": 23
}, Person)

print("type:", type(person))
print("name:", person.name)
print("age:", person.age)
```

will give:

```
type: <class '__main__.Person'>
name: bob
age: 23
```