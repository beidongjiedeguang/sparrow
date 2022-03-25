import copy
import ml_collections


referenced_dict = {"inner_float": 3.14}
d = {
    "referenced_dict_1": referenced_dict,
    "referenced_dict_2": referenced_dict,
    "list_containing_dict": [{"key": "value"}],
}

# We can initialize on a dictionary
cfg = ml_collections.ConfigDict(d)

print(cfg)
