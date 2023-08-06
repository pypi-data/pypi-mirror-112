# Good:
#  - no KeyErrors
#  - setable
#  - setting [key]=dict() the dict() is NestedDict
# bad:
#  - every read also writes
class NestedDict(dict):
    def __getitem__(self, key):
        # print(f'{self}.__getitem__({key = })')
        if key not in self:
            value = NestedDict()
            self.__setitem__(key, value)
            # return self[key]
            return value
            # return NestedDict()
            # return self.setdefault(key, NestedDict())
        value = self.get(key)
        if isinstance(value, dict):
            value = NestedDict(value)
            # self.__setitem__(key, value)
        return value

    # def __setitem__(self, k, v) -> None:
    #     print(f'{self}.__setitem__({k = }, {v = })')
    #     super().__setitem__(k, v)
    #     print(f'\t→ {self}')



