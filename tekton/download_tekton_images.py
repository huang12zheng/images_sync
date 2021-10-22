import json 
import os

class Tekton:
    def __init__(self):
        self.json_file = "tekton_images.json"
        self.target_registry = "ccr.ccs.tencentyun.com/tektons/"
        # self.registry_user = registry_user
        # self.registry_passwd = registry_passwd

    def load_json(self, data):
        content = json.loads(data)
        return content

    def down_images(self):
        f = open(self.json_file, 'r').read()
        content = self.load_json(f)

        # docker_login_cmd = "docker login -u {0} -p {1} {2}".format(
        #             self.registry_user,
        #             self.registry_passwd,
        #             self.target_registry.split("/")[0])
        for item in content:
            print("[GetImages] {}".format(item["t_image"]))
            docker_pull_cmd = "docker pull {0}".format(item["t_image"])
            # docker_tag_cmd = "docker tag {0} {1}".format(item["t_image"], item["s_image"].split("@")[0])
            os.system(docker_pull_cmd + "&&" + docker_tag_cmd )
            print("[GetImagesDone] {}".format(item))

if __name__ == '__main__':
    t = Tekton().down_images()