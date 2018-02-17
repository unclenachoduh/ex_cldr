import urllib.request
import re

home = urllib.request.urlopen("http://bugs.icu-project.org/trac/browser/trunk/icu4c/source/data/lang?order=name")
home_text = home.read().decode('utf-8', "strict")
wout = open("home.html", "w+")
home_lines = home_text.split("\n")
langs = [] # list of language docs
for line in home_lines:
    line = re.sub("\s+", " ", line)
    line = re.sub("^\s", "", line)
    # print(line)
    parts = line.split(" ")
    if len(parts) > 2 and parts[0] == "<a" and parts[1] == "class=\"file\"":
        me = re.split("[><]", parts[4])
        # print(me[1])
        langs.append(me[1])

for lang in langs:
    # print("\n\n\n\n" + lang + "\n\n\n\n")
    new_file = re.sub(".txt", ".ftl", lang)
    wout = open("ftl_files/" + new_file, "w+")
    if lang[-4:] == ".txt":
        source = urllib.request.urlopen("http://icu-project.org/trac/browser/trunk/icu4c/source/data/lang/" + lang + "?format=txt")
        text = source.read().decode('utf-8', "strict")
        text_lines = text.split("\n")
        interior = 0
        catch = False
        for line in text_lines:
            line = re.sub("\ufeff", "", line)
            # print("BASIC", line)
            if bool(re.search("^//", line)) == False and bool(re.search("[(/**)(**/)]", line)) == False and line != '':
                line = re.sub("\s+", " ", line)
                line = re.sub("^\s", "", line)

                # print("NOT COMMENT")

                if "{" in line and "}" not in line:
                    interior += 1
                    if "Languages{" in line:
                        catch = True
                elif "}" in line and "{" not in line:
                    interior -= 1
                    catch = False
                elif len(re.findall("{", line)) < 2 and len(re.findall("}", line)) < 2:
                    # print(line)
                    if catch == True:
                        parts = re.split("[\{\}\"]", line)
                        # print(parts)
                        # print("PAIR:", parts[0], "=", parts[2])
                        wout.write(parts[0] + " = " + parts[2] + "\n")



# wout = open("es.txt", "w+")
# wout.write(text)
