# from yaml2object import YAMLObject
from yaml2object import YAMLObject
import yaml

def to_cycle_dict(obj):
    if isinstance(obj,list):
        return handle_list(obj)

    dic = {}
    for fieldkey in dir(obj):
        fieldvaule = getattr(obj, fieldkey)
        if not fieldkey == "source" and not fieldkey.startswith("__") and not callable(fieldvaule) and not fieldkey.startswith("_"):
            if isinstance(fieldvaule,list):
                ret_list = handle_list(fieldvaule)
                dic[fieldkey] = ret_list
            else:
                dic[fieldkey] = fieldvaule
    return dic

def handle_list(input):
    ret_list = []
    for item in input:
        tmp_dict = to_cycle_dict(item)
        if len(tmp_dict.keys()) == 0:
            ret_list.append(item)
        else:
            ret_list.append(to_cycle_dict(item))
    return ret_list

# class Config(metaclass=YAMLObject):
#     source = 'config.yaml'

    

# if __name__ == '__main__':
#     # Config.install_files[0].item
#     strv = str(Config)
#     d = to_cycle_dic(Config)
#     with open('test.yaml','w') as file:
#     #     # file.write
#         yaml.dump(d, file)


#     print('\n');
