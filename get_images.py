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
        ConfigYaml.images.extend(input)
        ConfigYaml.images = list(set(ConfigYaml.images))

    def save_yaml(self):
        # configYamlFile=open(configYamlPath, 'w')
        with open(configYamlPath+'1', 'w') as configYamlFile:
            ConfigYaml.install_file_cache = list(set(ConfigYaml.install_file_cache))
            ConfigYaml.images = list(set(ConfigYaml.images))

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

    images = list(set(images))
    return images



def to_generial_image(i):
    i.split("/")[-1].split("@")[0]

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
            ConfigYaml.expand_images(get_images(install_yaml.content))
            ConfigYaml.add_install_file(install_file.url)

    ConfigYaml.save_yaml()

    #! pull image and save


