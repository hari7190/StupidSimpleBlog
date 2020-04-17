# Author : Hari

import subprocess
import json
import os
import errno
import shutil


# Get Details
with open('../../config.json') as config_file:
    data = json.load(config_file)

outputDirectory = data["parse"]["target"]

with open('../../secrets.json') as secret_file:
    data = json.load(secret_file)

destDirectory = data["remotes"][0]["path"]
remoteUser = data["remotes"][0]["user"]
remoteHost = data["remotes"][0]["remotehost"]

p = subprocess.Popen(["scp", "-pr", outputDirectory + "/.", remoteUser + "@" + remoteHost + ":" + destDirectory + "/"])

sts = os.waitpid(p.pid, 0)