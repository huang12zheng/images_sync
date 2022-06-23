import re
import requests
import yaml
import json
import sys
import os

from yaml2object import YAMLObject
from to_cycle_dict import to_cycle_dict

configYamlPath = 'config.yaml'

class ConfigYaml(metaclass=YAMLObject):
    source = configYamlPath
    namespace = 'dev'

    def add_install_file(self,input):
        ConfigYaml.install_file_cache.append(input)

    def expand_images(self,input):
        def hash_key(obj):
            return f"{obj['s_image']}{obj['t_image']}"
        # ConfigYaml.images.extend(input)
        input_diff = [ x for x in input
            if not hash_key(x) in 
                map(hash_key,ConfigYaml.images)
        ]
        ConfigYaml.images.extend(input_diff)

    def save_yaml(self):
        # configYamlFile=open(configYamlPath, 'w')
        with open(f'1{configYamlPath}', 'w') as configYamlFile:
            ConfigYaml.install_file_cache = list(set(ConfigYaml.install_file_cache))
            # ConfigYaml.images = list(set(ConfigYaml.images))

            yaml.dump(to_cycle_dict(ConfigYaml), configYamlFile)
            configYamlFile.close()

def get_images(content):
    content = bytes.decode(content)
    #! STEP 1: ignore #
    ret = re.sub(r'#.*$', "", content)
    #! STEP 2: filter image
    ret = re.findall(f"image.*",ret)
    ret = "".join(ret)

    #! STEP 3: filter prefixs
    images = []
    prefixs = ['gcr.io/']
    for prefix in prefixs:
        prefix_rets = re.findall(f"[ \"]{prefix}.*?(?:[ \"\n])",ret)
        for prefix_ret in prefix_rets:
            tmp = re.sub(r'"', "", prefix_ret)
            tmp = re.sub(r' ', "", tmp)
            images.append(tmp)
    return images

def get_image_dict(target,images):
    ret_list = list(
        map(lambda x: {'s_image':x,'t_image':to_target_image(target,x)},images)
    )
    return ret_list

def to_target_image(target,i):
    return os.path.join(target,to_generial_image(i))

def to_generial_image(i):
    return i.split("/")[-1].split("@")[0]

if __name__ == '__main__':
    #! Loop install file for request, and then get all image.
    for install_file in ConfigYaml.install_files:
        #! Cut branches optimization 1, only handle new url
        if ConfigYaml.install_file_cache.count(install_file.url) != 0:
            continue


        install_yaml = requests.get(install_file.url)
        if install_yaml.status_code != 200:
            print(f"request error:{install_yaml.status_code}:{install_file.url}")
        else:
            ret_images = get_image_dict(install_file.target_registry,get_images(install_yaml.content))
            ConfigYaml.expand_images(ret_images)
            ConfigYaml.add_install_file(install_file.url)

    ConfigYaml.save_yaml()

    #! pull image and save


