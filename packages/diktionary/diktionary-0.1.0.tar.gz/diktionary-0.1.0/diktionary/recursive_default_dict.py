"""from collections import defaultdict

# Good:
#  - no KeyErrors
#  - setable
# Bad:
#  - setting [key] = dict(), the dict() isn't recursive_dict
recursive_dict_constructor = lambda: defaultdict(recursive_dict_constructor)
bad_account = recursive_dict_constructor()
if bad_account["products"]["EndpointSecure"]["provisioned"]:
    ...
if bad_account["bad"]["worse"]:
    ...

bad_account["bad"]["worse"] = {'hello':'world'}
print(bad_account["bad"]["worse"]['hello'])
print(bad_account["bad"]["worse"]['helloz']) # fails

exit()
bad_account_data = {
    "account_id": "yosi",
    "products":   {
        "EndpointSecure": {
            "max_devices": 5
            }
        }
    }

# def recursive_dict_constructor(**data):
#     return defaultdict(lambda: recursive_dict_constructor(**data), **data)
# recursive_dict_constructor = lambda **data: defaultdict(recursive_dict_constructor, **data)
recursive_dict_constructor = lambda: defaultdict(recursive_dict_constructor)
bad_account = recursive_dict_constructor()
if bad_account["products"]["EndpointSecure"]["provisioned"]:
    ...
if bad_account["bad"]["worse"]:
    ...

# if bad_account["products"]["NetworkSecure"]["provisioned"]:
#     ...



# recursive_dict["products"]["EndpointSecure"] = {"hello": "world"}
# print(recursive_dict["products"]["EndpointSecure"]["hello"])  # -> world
"""