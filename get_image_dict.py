import re
import requests
import yaml
import json
import sys
import os

def get_images(content):
    content = bytes.decode(content)
    #! STEP 1: ignore #
    ret = re.sub(r'#.*$', "", content)
    #! STEP 2: filter image
    ret = re.findall(f"image.*",ret)
    ret = "\n".join(ret)

    #! STEP 3: filter prefixs
    images = []
    prefixs = ['gcr.io/']
    for prefix in prefixs:
        prefix_rets = re.findall(f"[ \"]{prefix}[^\"\n ]*",ret)
        for prefix_ret in prefix_rets:
            tmp = re.sub(r'"', "", prefix_ret)
            tmp = re.sub(r' ', "", tmp)
            tmp = re.sub(r'\n', "", tmp)
            tmp = re.sub(r'@sha.*', "", tmp)
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