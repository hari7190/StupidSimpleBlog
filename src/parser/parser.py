import json
import os, errno
import shutil, sys

from pprint import pprint

#Get Config

with open('../../config.json') as data_file:
    data = json.load(data_file)

directory=data["parse"]["target"]

#Delete current output folder
try:
    shutil.rmtree("../../" + directory)
except OSError as e:
    print('No directory to delete')

#Create directory

try:
    directory="../../" + directory
    os.makedirs(directory)
except OSError as e:
    if e.errno != errno.EEXIST:
        raise

#Get commons and append

with open("../../" + data["format"]["header"], "r") as f: header = f.read()
with open("../../" + data["format"]["footer"], "r") as f: footer = f.read()

file_list = [x for x in os.listdir("../../web/posts") if x.endswith(".html")]
print(file_list)

for file in file_list:
    with open("../../web/posts/" + file, "r") as f: post_content = f.read()
    final_content = header + post_content + footer

    with open(directory + '/post-' + file ,'w') as ofh:
        ofh.write(final_content)

