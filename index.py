import re
import requests
import yaml
import json
import sys
import os

from yaml2object import YAMLObject
from to_cycle_dict import to_cycle_dict
from get_image_dict import get_image_dict,get_images

configYamlPath = 'config.yaml'

class ConfigYaml(metaclass=YAMLObject):
    source = configYamlPath
    namespace = 'dev'

    def add_install_file(self,input):
        ConfigYaml.install_file_cache.append(input)

    def expand_images(self,input):
        input_diff = [ x for x in input
            if not hash_key(x) in 
                map(hash_key,ConfigYaml.images)
        ]
        ConfigYaml.images.extend(input_diff)

    def add_images_cache(self,input):
        #! 用补偿模式可会有重复的
        if not hash_key(input) in map(hash_key,ConfigYaml.images_cache):
            ConfigYaml.images_cache.append(input)


    def save_yaml(self):
        # configYamlFile=open(configYamlPath, 'w')
        with open(f'{configYamlPath}', 'w') as configYamlFile:
            ConfigYaml.install_file_cache = list(set(ConfigYaml.install_file_cache))
            # ConfigYaml.images = list(set(ConfigYaml.images))

            yaml.dump(to_cycle_dict(ConfigYaml), configYamlFile)
            configYamlFile.close()
    def save_json_file(self):
        input_diff = [ x for x in ConfigYaml.images
            if not hash_key(x) in 
                map(hash_key,ConfigYaml.images_cache)
        ]
        cycle_dict =to_cycle_dict(input_diff)
        newdata = json.dumps(cycle_dict, indent=4)
        a=open('diff_images.json', 'w')
        a.write(newdata)
        a.close()

def hash_key(obj):
            return f"{obj['s_image']}{obj['t_image']}"

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
    ConfigYaml.save_json_file()

    #! pull image and save


