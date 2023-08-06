from unittest import TestCase
from src import anodict


class Person:
    name: str
    age: int


class Employee:
    profession: str
    salary: float


class TestDictToClass(TestCase):
    def test_simple(self):
        o = anodict.dict_to_class({
            "name": "bob",
            "age": 23
        }, Person)
        self.assertEquals(o.name, "bob")
        self.assertEquals(o.age, 23)

    def test_ignore_unannotated(self):
        o = anodict.dict_to_class({
            "name": "bob",
            "age": 23,
            "height": 165
        }, Person, ignore_unannotated=True)
        self.assertEquals(o.name, "bob")
        self.assertEquals(o.age, 23)
        self.assertFalse(hasattr(o, 'height'))

    def test_nullify(self):
        o = anodict.dict_to_class({
            "name": "bob",
        }, Person, nullify_missing=True)
        self.assertEquals(o.name, "bob")
        self.assertEquals(o.age, None)
