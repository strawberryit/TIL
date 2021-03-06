#-*- coding: utf-8 -*-
import re
import string
import glob
import os.path
import io


header = """
# TIL
> Today I Learned
오늘 배운 내용을 간결하게 정리하여 모아둔다.
---
"""

footer = """
---
## Rules
* Directory and file would be lowercase.
* Follow GFM(Github Flavored Markdown)
## Usage
### Generate `README.md`
```
$ python3 build.py
```
### Run in Local
Use [Docker](https://www.docker.com) and [Gollum](https://github.com/gollum/gollum). Details are [here](https://github.com/AWEEKJ/TIL/blob/master/docker/gollum-via-docker.md).
## Other TIL Collections
Inspired by
* [@thoughtbot](https://github.com/thoughtbot/til)
* [@jbranchaud](https://github.com/jbranchaud/til)
* [@milooy](https://github.com/milooy/TIL)
* [@channprj](https://github.com/channprj/TIL)
"""

###################################


def make_pretty_name(name):
    pretty_name = re.sub(r'-', ' ', name)
    return string.capwords(pretty_name)


readme = io.open('README.md', 'r+', encoding='utf-8')
readme.write(header)
readme.write("## Categories\n")

files = sorted(glob.glob('**', recursive=True))
directories = []

for file in files:
    if os.path.isdir(file):
        directories.append(file)

# 목록에서 제외 할 디렉토리
def is_exclude_dir(directory):
    return directory == 'drafts' \
        or directory.endswith('/image') \
        or directory.endswith('/files')

directories = [d for d in directories if not is_exclude_dir(d)]

for directory in directories:
    readme.write("* [" + directory.capitalize() + "](#" + directory + ")\n")

readme.write("\n---\n")

for directory in directories:
    readme.write("\n## " + directory.capitalize() + "\n")
    sub_files = glob.glob(directory + '/*.md')
    for sub_file in sub_files:
        readme.write("* [" + make_pretty_name(os.path.basename(sub_file)) + "](" + sub_file + ")\n")

readme.write(footer)
readme.close
