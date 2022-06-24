import os
import sys
import json

from index import ConfigYaml

class Docker:
    def __init__(self, registry_user, registry_passwd,target_registry):
        self.registry_user = registry_user
        self.registry_passwd = registry_passwd
        self.target_registry = target_registry;
        self.result = []

    def sync_images(self):
        f = open("diff_images.json", 'r').read()
        content = json.loads(f)

        docker_login_cmd = "docker login -u {0} -p {1} {2}".format(
            self.registry_user,
            self.registry_passwd,
            self.target_registry)
        os.system(docker_login_cmd)
        for item in content:
            print("[GetImages] {}".format(item))
            docker_pull_cmd = "docker pull {0}".format(item["s_image"])
            docker_tag_cmd = "docker tag {0} {1}".format(item["s_image"], item["t_image"])
            docker_push_cmd = "docker push {0}".format(item["t_image"])
            ret = os.system(docker_pull_cmd + "&&" + docker_tag_cmd + "&&" + docker_push_cmd)
            if ret == 0:
                print("[GetImagesDone] {}".format(item))
                ConfigYaml.add_images_cache(item)
            else:
                print("[Error] {}".format(item))
        ConfigYaml.save_yaml()

if __name__ == '__main__':
    # tekton = Docker(sys.argv[1], sys.argv[2],sys.argv[3])
    tekton = Docker("805104533", "hz520self","ccr.ccs.tencentyun.com")
    # tekton = Docker('1','2','3')
    tekton.sync_images()