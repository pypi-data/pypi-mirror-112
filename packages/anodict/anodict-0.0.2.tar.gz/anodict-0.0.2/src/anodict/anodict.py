from typing import TypeVar, Generic

_T = TypeVar('_T')


class _Constructor(Generic[_T]):
    @staticmethod
    def dict_to_class(_dict: dict, _class: _T, ignore_unannotated: bool = False,
                      nullify_missing: bool = False) -> _T:
        if not hasattr(_class, '__annotations__'):
            raise ValueError('Class must have annotated properties.')
        if not set(_dict.keys()).issubset(_class.__annotations__.keys()) and not ignore_unannotated:
            raise ValueError('Dict contains unannotated properties.')
        _dict = _dict.copy()
        # ignore unannotated properties
        for k in set(_dict.keys()).difference(_class.__annotations__.keys()):
            del _dict[k]
        # nullify missing properties
        if nullify_missing:
            for k in set(_class.__annotations__.keys()).difference(_dict.keys()):
                _dict[k] = None
        instance = _class()
        setattr(instance, '__dict__', _dict)
        return instance


dict_to_class = _Constructor.dict_to_class
