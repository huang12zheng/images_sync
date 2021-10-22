# tekton_images_sync
Tekton 部署镜像同步到腾讯云CCR


## 镜像仓库

腾讯云： ccr.ccs.tencentyun.com/tektons

```
controller
kubeconfigwriter
git-init
entrypoint
nop
imagedigestexporter
pullrequest-init
cloud-sdk
base
powershell
webhook

```

## 镜像信息

参考v0.29.0-release.yaml

```
gcr.io/tekton-releases/github.com/tektoncd/pipeline/cmd/controller:v0.29.0@sha256:72f79471f06d096cc53e51385017c9f0f7edbc87379bf415f99d4bd11cf7bc2b
gcr.io/tekton-releases/github.com/tektoncd/pipeline/cmd/kubeconfigwriter:v0.29.0@sha256:6d058f2203b9ab66f538cb586c7dc3b7cc31ae958a4135dd99e51799f24b06c9
gcr.io/tekton-releases/github.com/tektoncd/pipeline/cmd/git-init:v0.29.0@sha256:c0b0ed1cd81090ce8eecf60b936e9345089d9dfdb6ebdd2fd7b4a0341ef4f2b9
gcr.io/tekton-releases/github.com/tektoncd/pipeline/cmd/entrypoint:v0.29.0@sha256:66958b78766741c25e31954f47bc9fd53eaa28263506b262bf2cc6df04f18561
gcr.io/tekton-releases/github.com/tektoncd/pipeline/cmd/nop:v0.29.0@sha256:6a037d5ba27d9c6be32a9038bfe676fb67d2e4145b4f53e9c61fb3e69f06e816
gcr.io/tekton-releases/github.com/tektoncd/pipeline/cmd/imagedigestexporter:v0.29.0@sha256:e38dd0d32253fce5aaf1e501c0bc71facc3720564b7e97055921cc5390d612e0
gcr.io/tekton-releases/github.com/tektoncd/pipeline/cmd/pullrequest-init:v0.29.0@sha256:d28202fb8b33a1d4c05f261ef8dcbcdcf3b469887d4dad256ce91f73c917420e
gcr.io/google.com/cloudsdktool/cloud-sdk@sha256:27b2c22bf259d9bc1a291e99c63791ba0c27a04d2db0a43241ba0f1f20f4067f
gcr.io/distroless/base@sha256:aa4fd987555ea10e1a4ec8765da8158b5ffdfef1e72da512c7ede509bc9966c4
mcr.microsoft.com/powershell:nanoserver@sha256:b6d5ff841b78bdf2dfed7550000fd4f3437385b8fa686ec0f010be24777654d6
gcr.io/tekton-releases/github.com/tektoncd/pipeline/cmd/webhook:v0.29.0@sha256:46d5b90a7f4e9996351ad893a26bcbd27216676ad4d5316088ce351fb2c2c3dd
```



## 使用方法

1. 下载action最新一次构建中的制品；

```
tekton_images.json
```

3. 运行脚本下载镜像: 

```
# 脚本位置
https://github.com/zeyangli/tekton_images_sync/blob/main/tekton/download_tekton_images.py
python3 download_tekton_images.py
```
5. 手动更新release.yaml中的镜像，然后kubectl apply release.yaml  （后续有时间再优化脚本，实现自动更新release.yaml）


