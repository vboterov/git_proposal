import glob
import os
import sys

path = sys.argv[1]
env = sys.argv[2]
if os.path.isfile(path):
    files = [path]
else:
    files = glob.glob(path + "/*")
for file in files:
    with open(file, "r") as f:
        contents = f.read()
        contents = contents.replace('"env_name": "dev"', f'"env_name": "{env}"')

    with open("dist/" + file, "w+") as out:
        out.write(contents)
