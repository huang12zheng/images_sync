# index.py
* reget images from install_file
please remove url in `install_file_cache`

* images
it is all you need to download
# sync_images.py


> please check dir .github

# apply file
use `sed -i 's/@sha[^"]*//g' tekton-latest.yaml ` to make digest loss
> curl https://storage.googleapis.com/tekton-releases/pipeline/latest/release.yaml -o tekton-latest.yaml