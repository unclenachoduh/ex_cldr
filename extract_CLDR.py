import urllib.request
import re
import os

home = urllib.request.urlopen("http://bugs.icu-project.org/trac/browser/trunk/icu4c/source/data/lang?order=name")
home_text = home.read().decode('utf-8', "strict")
home_lines = home_text.split("\n")
langs = [] # list of language docs
for line in home_lines:
    line = re.sub("\s+", " ", line)
    line = re.sub("^\s", "", line)
    parts = line.split(" ")
    if len(parts) > 2 and parts[0] == "<a" and parts[1] == "class=\"file\"":
        me = re.split("[><]", parts[4])
        langs.append(me[1])

directory = "ftl_files/"

for lang in langs:
    new_directory = re.sub(".txt", "", lang)
    if not os.path.exists(directory + new_directory):
        os.makedirs(directory + new_directory)
    new_file = new_directory + "/resources.ftl"
    wout = open(directory + new_file, "w+")
    if lang[-4:] == ".txt":
        source = urllib.request.urlopen("http://icu-project.org/trac/browser/trunk/icu4c/source/data/lang/" + lang + "?format=txt")
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
                    if "Languages{" in line:
                        catch = True
                elif "}" in line and "{" not in line:
                    interior -= 1
                    catch = False
                elif len(re.findall("{", line)) < 2 and len(re.findall("}", line)) < 2:
                    if catch == True:
                        parts = re.split("[\{\}\"]", line)
                        wout.write("language-name-" + parts[0] + " = " + parts[2] + "\n")
