from collections import defaultdict

# Looks like no difference between this and inheriting simple dict
class NestedDefaultDict(defaultdict):
    def __init__(self, obj=()) -> None:
        super().__init__(NestedDefaultDict, obj)

    def __getitem__(self, k):
        v = self.get(k)
        print(f'{self}.__getitem__({k = }) → {v = }')
        if isinstance(v, dict):
            v = NestedDefaultDict(v)
            self.__setitem__(k, v)
            return v

        return super().__getitem__(k)

    def __setitem__(self, k, v) -> None:
        print(f'{self}.__setitem__({k = }, {v = })')
        if isinstance(v, dict):
            v = NestedDefaultDict(v)
        super().__setitem__(k, v)

    def __repr__(self) -> str:
        return str(dict(self))



"""document = {
    "products":   {
        "EndpointSecure": {
            # "provisioned": True,
            "max_devices": 5
            }
        }
    }
bad_account = NestedDefaultDict(document)
print(bad_account, '\n')
if bad_account["products"]["EndpointSecure"]["provisioned"]:
    ...
if bad_account["bad"]["worse"]:
    ...

bad_account["bad"]["worse"] = {'hello':'world'}
print(bad_account["bad"]["worse"]['hello'])
print(bad_account["bad"]["worse"]['hello']) # fails

print('\n', bad_account)"""