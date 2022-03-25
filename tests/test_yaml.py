from sparrow import yaml_load

res = yaml_load("./yaml/test1.yaml", rel_path=True)

assert isinstance(res["str_num"], str)
