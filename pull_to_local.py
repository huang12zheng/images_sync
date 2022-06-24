import json
import re
from index import ConfigYaml
import os

import_command = 'microk8s ctr image import '

if __name__ == '__main__':
    #! cache file
    f = open("diff_images.json", 'r').read()
    content = json.loads(f)
    
    #! get config
    for image in ConfigYaml.images_cache:
        #! run docker command
        print("[GetImages] {}".format(image))
        saveImage=re.sub("@.*","",image["s_image"])
        if saveImage in content:
            print('Pass: {saveImage}')
            continue
        docker_pull_cmd = "sudo docker pull {0}".format(image["t_image"])
        docker_tag_cmd = "sudo docker tag {0} {1}".format(image["t_image"], saveImage)
        docker_rm_cmd = "sudo docker rmi {0}".format(image["t_image"])

        docker_save_cmd = f"sudo docker save {saveImage} > ~/.docker_image.tmp.tar"
        ctr_image_import = f'{import_command} ~/.docker_image.tmp.tar'

        # docker_push_cmd = "docker push {0}".format(image["t_image"])
        ret = os.system(docker_pull_cmd + "&&" + docker_tag_cmd + "&&" + docker_rm_cmd + '&&'
            + docker_save_cmd + '&&' + ctr_image_import
        )
        if ret == 0:
            print("[GetImagesDone] {}".format(image))
            content.append(saveImage)
        else:
            print("[Error] {}".format(image))
    with open("diff_images.json", 'w') as file:
        file.write(content)