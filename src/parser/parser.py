import json, os, errno, shutil

##############################
#   Arguments
##############################

#print('Number of arguments:', len(sys.argv), 'arguments.')
#print('Argument List:', str(sys.argv))

##############################
#   Get Configuration
##############################

with open('../../config.json') as data_file:
    data = json.load(data_file)

directory = data["parse"]["target"]
root = data["format"]["root"]
posts = data["data"]["posts"]
navItems = data["data"]["navItems"]

##############################
#   Clear output
##############################

try:
    shutil.rmtree(directory)
except OSError as e:
    print('No directory to delete')

##############################
#   Create directory
##############################

try:
    directory = directory
    os.makedirs(directory)
except OSError as e:
    if e.errno != errno.EEXIST:
        raise

##############################
#   Get commons and append
##############################

with open("../../" + data["format"]["header"], "r") as f: header = f.read()
with open("../../" + data["format"]["footer"], "r") as f: footer = f.read()

file_list = [x for x in os.listdir("../../web/posts") if x.endswith(".html") and not x.endswith("-draft.html")]
print(file_list)

##############################
#   Prepare Header
##############################
navElement = '<li class="nav-item"><a class="nav-link" href="{link}">{title}</a></li>'

final_content = ''

for nav in navItems:
    temp = navElement.replace("{title}", nav["title"])

    if(nav["link"] + ".html" != root):
        temp = temp.replace("{link}", "post-" + nav["link"] + ".html")
    else:
        temp = temp.replace("{link}", nav["link"] + ".html")

    final_content = final_content + temp

header = header.replace("{navs}", final_content)



##############################
#   Prepare Posts
##############################
final_content = ''

for file in file_list:
    with open("../../web/posts/" + file, "r") as f: post_content = f.read()
    final_content = header + post_content + footer

    if(file != 'root.html'):
        with open(directory + '/post-' + file ,'w') as ofh:
            ofh.write(final_content)
    else:
        with open(directory + "/" + root,'w') as ofh:
            ofh.write(final_content)


def copyanything(src, dst):
    try:
        shutil.copytree(src, dst)
    except OSError as exc: # python >2.5
        if exc.errno == errno.ENOTDIR:
            shutil.copy(src, dst)
        else:
            raise


##############################
#   Copy Pages - Independent pages
##############################
copyanything("../../web/pages", directory + "/pages")


##############################
#   Copy snippets
##############################
copyanything("../../web/snippets", directory + "/snippets")

file_list = [x for x in os.listdir(directory + "/snippets") if not x.endswith(".html")]

print(file_list)

for file in file_list:
    os.rename(directory + '/snippets/' + file, directory + '/snippets/' + file.replace(".py", ".html"))


##############################
#   Copy resources
##############################
copyanything("../../web/resources", directory + "/resources")



##############################
#   Prepare post list
##############################

card_template = '<div class="card">' \
                '<div class="card-body">' \
                '<h4 class="card-title">{title}</h4>' \
                '<p class="card-text">{desc}</p>' \
                '{read_more}' \
                '</div>' \
                '</div>' \
                '<div class="clearfix">&nbsp;</div>'

read_more = '<a href="{link}" class="btn btn-info"">Read more</a>'

coming_soon = "<p class=\"text-info\">Coming Soon</p>"

final_content = ''

for post in reversed(posts):
    if ('ready' in post and not post['ready']):
        temp = card_template.replace("{read_more}", coming_soon)
    else:
        temp = card_template.replace("{read_more}", read_more)
    temp = temp.replace("{title}", post["title"])
    temp = temp.replace("{desc}", post["desc"])
    temp = temp.replace("{link}", "post-" + post["link"] + ".html")
    final_content = final_content + '\n' + temp

with open(directory + "/" + root,'w') as ofh:
    ofh.write(header + final_content + footer)
