# Script for bug 1433694

*[Link to bug](https://bugzilla.mozilla.org/show_bug.cgi?id=1433694)*

## Description

This script downloads all of the CLDR files available from the [ICU Project website]( http://bugs.icu-project.org/trac/browser/trunk/icu4c/source/data/lang?order=name),  extracts the language ID data, and converts it to Fluent format.

## Running the script

This script is meant to be ran in the terminal with Python 3.

`python3 extract_CLDR.py`

## Output

The folder "ftl_files" contains the extracted data. Each file contains the variable/value pairs from the CLDR files with the label "Languages". The format for each pair is `var = value`.
