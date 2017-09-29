import json, os, errno, shutil, sys
from time import gmtime, strftime
##############################
#   Arguments
##############################

#print('Number of arguments:', len(sys.argv), 'arguments.')
#print('Argument List:', str(sys.argv))

##############################
#   Get Configuration
##############################
def printMessage(message, type):
    print("----------------" + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime()) + "------------------------")
    print(message)
    #print("-----------------------------------------------------------")


printMessage("Parser initiating","info")

with open('../../config.json') as data_file:
    data = json.load(data_file)

directory = data["parse"]["target"]
root = data["format"]["root"]
posts = data["data"]["posts"]
navItems = data["data"]["navItems"]

printMessage("Configuration loaded","info")

##############################
#   Clear output
##############################

try:
    shutil.rmtree("../../" + directory)
except OSError as e:
    print('No directory to delete')


printMessage("Cleaning target","info")

##############################
#   Create directory
##############################

try:
    directory = "../../" + directory
    os.makedirs(directory)
except OSError as e:
    if e.errno != errno.EEXIST:
        raise

printMessage("Target prepped","info")

##############################
#   Get commons and append
##############################

with open("../../" + data["format"]["header"], "r") as f: header = f.read()
with open("../../" + data["format"]["footer"], "r") as f: footer = f.read()

file_list = [x for x in os.listdir("../../web/posts") if x.endswith(".html") and not x.endswith("-draft.html")]


printMessage(file_list,"info")

##############################
#   Prepare Header
##############################
navElement = '<li class="nav-item">' \
'<a class="nav-link" href="{link}">{title}</a>' \
'</li>'

final_content = ''

for nav in navItems:
    temp = navElement.replace("{title}", nav["title"])
    temp = temp.replace("{link}", "post-" + nav["link"] + ".html")
    final_content = final_content + temp

header = header.replace("{navs}", final_content)

printMessage("Header prepped","info")
##############################
#   Prepare Posts
##############################
final_content = ''

for file in file_list:
    with open("../../web/posts/" + file, "r") as f: post_content = f.read()
    final_content = header + post_content + footer

    if(file.endswith("-norename.html")):
        with open(directory + '/' + file.replace("-norename.html", ".html") ,'w') as ofh:
            ofh.write(final_content)
    else:
        with open(directory + '/post-' + file ,'w') as ofh:
            ofh.write(final_content)

def copyanything(src, dst):
    try:
        shutil.copytree(src, dst)
    except OSError as exc: # python >2.5
        if exc.errno == errno.ENOTDIR:
            shutil.copy(src, dst)
        else: raise

printMessage("Posts parsed and compiled","info")

##############################
#   Copy resources
##############################

copyanything("../../web/resources", directory + "/resources")

printMessage("Resources copied","info")

##############################
#   Prepare post list
##############################

card_template = '<div class="card">' \
                '<div class="card-body">' \
                '<h4 class="card-title">{title}</h4>' \
                '<p class="card-text">{desc}</p>' \
                '<a href="{link}" class="btn btn-info"">Read more</a>' \
                '</div>' \
                '</div>' \
                '<div class="clearfix">&nbsp;</div>'

final_content = ''

for post in posts:
    temp = card_template.replace("{title}", post["title"])
    temp = temp.replace("{desc}", post["desc"])
    temp = temp.replace("{link}", "post-" + post["link"] + ".html")
    final_content = final_content + temp

with open(directory + "/" + root,'w') as ofh:
    ofh.write(header + final_content + footer)

printMessage("Root prepped and compiled","info")


printMessage("Completed","info")