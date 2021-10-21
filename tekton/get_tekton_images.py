import yaml
import json
import sys
import os

class Tekton :
    def __init__(self, file_name, registry_user, registry_passwd):
        self.yaml_file = file_name
        self.arg_imgs = []
        self.split_str = "###"
        self.deployments = ["tekton-pipelines-controller", "tekton-pipelines-webhook"]
        self.kind_type = "Deployment"
        self.target_registry = "ccr.ccs.tencentyun.com/tektons/"
        self.repos = [  "controller", "kubeconfigwriter", "git-init",
                        "entrypoint","nop","imagedigestexporter", 
                        "pullrequest-init", "cloud-sdk", "base", "powershell", "webhook"]
        self.result = []
        self.registry_user = registry_user
        self.registry_passwd = registry_passwd

    def load_yaml(self, data):
        content = yaml.load(data)
        return content

    def load_json(self, data):
        content = json.loads(data)
        return content

    def get_images(self):
        f = open(self.yaml_file, 'r').read()
        for i in f.split("###")[:-1]:
            try:
                content = self.load_yaml(i.replace("###", ""))
                if content["kind"] == self.kind_type:
                    deploy_name = content["metadata"]["name"]
                    # 获取image
                    if deploy_name in self.deployments:
                        img = content["spec"]["template"]["spec"]["containers"][0]["image"]
                        self.arg_imgs.append(img)
                    # 获取参数中的images
                    if deploy_name == "tekton-pipelines-controller":
                        arg_img =  content["spec"]["template"]["spec"]["containers"][0]["args"]
                        for a in arg_img:
                            if not a.startswith("-"):
                                self.arg_imgs.append(a)
            except Exception as e:
                print(e)
        return self.arg_imgs

    def save_json_file(self, data, file_name):
        for i in self.arg_imgs:
            self.result.append({
                "s_image": i,
                "t_image": self.target_registry + i.split("/")[-1].split("@")[0]
                })
        newdata = json.dumps(self.result, indent=4)
        a=open(file_name, 'w')
        a.write(newdata)
        a.close()

    def sync_images(self):
        f = open("tekton_images.json", 'r').read()
        content = self.load_json(f)
        docker_login_cmd = "docker login -u {0} -p {1} {2}".format(
            self.registry_user,
            self.registry_passwd,
            self.target_registry.split("/")[0])
        os.system(docker_login_cmd)
        for item in content:
            print("[GetImages] {}".format(item))
            docker_pull_cmd = "docker pull {0}".format(item["s_image"])
            docker_tag_cmd = "docker tag {0} {1}".format(item["s_image"], item["t_image"])
            docker_push_cmd = "docker push {0}".format(item["t_image"])
            os.system(docker_pull_cmd + "&&" + docker_tag_cmd + "&&" + docker_push_cmd)
            print("[GetImagesDone] {}".format(item))
        
if __name__ == '__main__':
    tekton = Tekton("release1.yaml", sys.argv[1], sys.argv[2])
    images = tekton.get_images()
    tekton.save_json_file(images, "tekton_images.json")
    tekton.sync_images()
