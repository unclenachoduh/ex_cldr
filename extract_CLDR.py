#test
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
            if me[1] not in language_names:
                language_names.append(me[1])
    return(language_names)

def retreive_values(lang, page_url, find_str, name_str):
    values = []

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
                    values.append(s)
    return values


def cldr_to_ftl(common, languages, regions):

    page_url = "" # stem of address for individual Region or Language pages
    find_str = "" # searched tag to extract data
    name_str = "" # stem of name of ftl variables



    # TODO: language extraction

    # TODO: language overlay

    # TODO: Region extraction

    # TODO: region overlay

    directory = "ftl_files/"

    page_url = "http://icu-project.org/trac/browser/trunk/icu4c/source/data/region/"
    find_str = "Countries{"
    name_str = "region-name-{}"

    for fff in common:
        if fff[-4:] == ".txt":
            values = retreive_values(fff, page_url, find_str, name_str)

            page_url = "http://icu-project.org/trac/browser/trunk/icu4c/source/data/lang/"
            find_str = "Languages{"
            name_str = "language-name-{}"

            values2 = retreive_values(fff, page_url, find_str, name_str)

            new_directory = re.sub(".txt", "", fff)
            if not os.path.exists(directory + new_directory):
                os.makedirs(directory + new_directory)
            new_file = new_directory + "/resources.ftl"
            wout = open(directory + new_file, "a")

            for v in values:
                wout.write(v)
            for v2 in values2:
                wout.write(v2)

    for fff in languages:
        if fff[-4:] == ".txt":
            values = retreive_values(fff, page_url, find_str, name_str)

            new_directory = re.sub(".txt", "", fff)
            if not os.path.exists(directory + new_directory):
                os.makedirs(directory + new_directory)
            new_file = new_directory + "/resources.ftl"
            wout = open(directory + new_file, "a")

            for v in values:
                wout.write(v)

    for fff in regions:
        if fff[-4:] == ".txt":

            page_url = "http://icu-project.org/trac/browser/trunk/icu4c/source/data/region/"
            find_str = "Countries{"
            name_str = "region-name-{}"

            values = retreive_values(fff, page_url, find_str, name_str)

            new_directory = re.sub(".txt", "", fff)
            if not os.path.exists(directory + new_directory):
                os.makedirs(directory + new_directory)
            new_file = new_directory + "/resources.ftl"
            wout = open(directory + new_file, "a")

            for v in values:
                wout.write(v)

def overlay(path):

    directory = "ftl_files/"
    dir_list = os.listdir(path)
    for file_name in dir_list:
        over_lines = open(path + file_name).readlines()

        over_dict = {}

        for over_line in over_lines:
            piece = over_line.split(" = ")
            over_dict[piece[0]] = over_line

        parts = file_name.split(".")
        lang = parts[0]
        file_loc = directory + lang + "/resources.ftl"

        if os.path.exists(file_loc):
            old_lines = open(file_loc).readlines()

            wout = open(file_loc, "w+")

            for old_line in old_lines:
                piece = old_line.split(" = ")

                if piece[0] in over_dict:
                    wout.write(over_dict[piece[0]])
                    if over_dict[piece[0]] in over_lines:
                        over_lines.remove(over_dict[piece[0]])

                else:
                    wout.write(old_line)

            for left_over in over_lines:
                wout.write(left_over)

            wout.c
        else:lose()


        else:
            os.makedirs(directory + lang + "/")
            wout = open(file_loc, "w+")
            for over_line in over_lines:
                wout.write(over_line)
            wout.close()

if __name__== "__main__":

####################################
# Nuke old files
    if os.path.exists("ftl_files/"):
        shutil.rmtree('ftl_files/')

    language_page = urllib.request.urlopen("http://icu-project.org/trac/browser/trunk/icu4c/source/data/lang")
    language_lines = language_page.read().decode('utf-8', "strict").split("\n")
    languages_tmp = get_file_names(language_lines) # list of language names

    region_page = urllib.request.urlopen("http://icu-project.org/trac/browser/trunk/icu4c/source/data/region")
    region_lines = region_page.read().decode('utf-8', "strict").split("\n")
    regions = get_file_names(region_lines) # list of language names

    # print("languages:", len(languages_tmp), "regions:", len(regions), "total:", len(languages_tmp) + len(regions))

################################################
# Create three lists: common, languages, regions
    common = []
    languages = []

    count = 0
    for l in languages_tmp:
        count += 1
        if l in regions:
            common.append(l)
            regions.remove(l)
            # print(count, l)
        else:
            # print(count, l, "******")
            languages.append(l)

    # print("languages:", len(languages), "regions:", len(regions), "common:", len(common)*2, "total:", len(languages) + len(regions) + len(common)*2)




    cldr_to_ftl(common, languages, regions)

    if os.path.exists("overlays/languages"):
        overlay("overlays/languages/")

    if os.path.exists("overlays/regions/"):
        overlay("overlays/regions/")
