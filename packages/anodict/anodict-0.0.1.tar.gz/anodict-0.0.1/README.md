# anodict: annotated dict

Convert a `dict` to an annotated object.

```python
import anodict


class Person:
    name: str
    age: int

person = anodict.dict_to_class({
    "name": "bob",
    "age": 23
}, Person)

print("name:", person.name)
print("age:", person.age)
```

will give:

```
name: bob
age: 23
```