import urllib.request
import re
import os
import shutil
from fluent.syntax import ast
from fluent.syntax import serialize

def get_file_names(home_file):
    language_names = []
    for line in home_file:
        line = re.sub("\s+", " ", line)
        line = re.sub("^\s", "", line)
        parts = line.split(" ")
        if len(parts) > 2 and parts[0] == "<a" and parts[1] == "class=\"file\"":
            me = re.split("[><]", parts[4])
            language_names.append(me[1])
    return(language_names)


def cldr_to_ftl(langs, config):

    page_url = "" # stem of address for individual Region or Language pages
    find_str = "" # searched tag to extract data
    name_str = "" # stem of name of ftl variables

    if config == 0:
        page_url = "http://icu-project.org/trac/browser/trunk/icu4c/source/data/lang/"
        find_str = "Languages{"
        name_str = "language-name-{}"
    elif config == 1:
        page_url = "http://icu-project.org/trac/browser/trunk/icu4c/source/data/region/"
        find_str = "Countries{"
        name_str = "region-name-{}"



    directory = "ftl_files/"

    for lang in langs:
        new_directory = re.sub(".txt", "", lang)
        if not os.path.exists(directory + new_directory):
            os.makedirs(directory + new_directory)
        new_file = new_directory + "/resources.ftl"
        wout = open(directory + new_file, "a")
        if lang[-4:] == ".txt":
            source = urllib.request.urlopen(page_url + lang + "?format=txt")
            text = source.read().decode('utf-8', "strict")
            text_lines = text.split("\n")
            interior = 0
            catch = False
            for line in text_lines:
                line = re.sub("\ufeff", "", line)
                if bool(re.search("^//", line)) == False and bool(re.search("[(/**)(**/)]", line)) == False and line != '':
                    line = re.sub("\s+", " ", line)
                    line = re.sub("^\s", "", line)

                    if "{" in line and "}" not in line:
                        interior += 1
                        if find_str in line:
                            catch = True
                    elif "}" in line and "{" not in line:
                        interior -= 1
                        catch = False
                    elif len(re.findall("{", line)) < 2 and len(re.findall("}", line)) < 2:
                        if catch == True:
                            parts = re.split("[\{\}\"]", line)

                            res = ast.Resource()

                            l10n_id = ast.Identifier(name_str.format(parts[0]))
                            value = ast.Pattern([ast.TextElement(parts[2])])
                            msg = ast.Message(l10n_id, value)
                            res.body.append(msg)

                            s = serialize(res)
                            wout.write(s)
        wout.close()

if __name__== "__main__":
    if os.path.exists("ftl_files/"):
        shutil.rmtree('ftl_files/')

    language_page = urllib.request.urlopen("http://icu-project.org/trac/browser/trunk/icu4c/source/data/lang")
    language_text = language_page.read().decode('utf-8', "strict")
    language_lines = language_text.split("\n")
    languages = get_file_names(language_lines) # list of language names

    cldr_to_ftl(languages, 0)

    region_page = urllib.request.urlopen("http://icu-project.org/trac/browser/trunk/icu4c/source/data/region")
    region_text = region_page.read().decode('utf-8', "strict")
    region_lines = region_text.split("\n")
    regions = get_file_names(region_lines) # list of language names

    cldr_to_ftl(regions, 1)
