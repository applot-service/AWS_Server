import os
import shutil

AWS_FOLDER_NAME = "./.aws-sam"
BUILD_FOLDER = os.path.abspath(AWS_FOLDER_NAME)
COMPONENT_FOLDER = os.path.abspath("./components")
DOMAIN_FOLDER = os.path.abspath("./domain")

#  1. Reset build folder
print("[1] Resetting build folder")
shutil.rmtree(BUILD_FOLDER, ignore_errors=True)

#  1. Build AWS folder
print("[2] Building AWS folder")
os.system("sam build --use-container")

#  3. Copy artefacts
print("[3] Copying modules")
shutil.copytree(DOMAIN_FOLDER, AWS_FOLDER_NAME + "/domain")
