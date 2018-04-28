# Script for bug 1433694

*[Link to bug](https://bugzilla.mozilla.org/show_bug.cgi?id=1433694)*

## Description

This script downloads all of the CLDR files available from the [ICU Project website]( http://icu-project.org/trac/browser/trunk/icu4c/source/data/lang), extracts the language ID data, and converts it to Fluent format.

## Running the script

This script is meant to be ran in the terminal with Python 3.

`python3 extract_CLDR.py`

It takes roughly 4 minutes to execute.

## Output

The folder `ftl_files/` contains the extracted data. Each folder is labeled with the language or region name from the CLDR data and contains a file with the variable/value pairs from the CLDR for language and region.

The format for each pair is `var = value`.

In addition to extracting CLDR data from the ICU Project website, this script also allows for overlay of FTL data from FTL files that are saved in the `/overlays` directory under the respective `/languages` or `/regions` subfolder. The overlaid data will overwrite existing variables with the same name or append new variables to the extracted CLDR data. The script does not differentiate between variable types in the overlay feature. Therefore, if a variable for some value that is not Language or Region is located in the `/overlays` directory, it will be added to the associated `resources.ftl` file.

The files in the `/overlays` directory are toys with arbitrary data.
# Script for bug 1433694

*[Link to bug](https://bugzilla.mozilla.org/show_bug.cgi?id=1433694)*

## Description

This script downloads all of the CLDR files available from the [ICU Project website]( http://icu-project.org/trac/browser/trunk/icu4c/source/data/lang), extracts the language ID data, and converts it to Fluent format.

## Running the script

This script is meant to be ran in the terminal with Python 3.

`python3 extract_CLDR.py`

It takes roughly 4 minutes to execute.

## Output

The folder `ftl_files/` contains the extracted data. Each folder is labeled with the language or region name from the CLDR data and contains a file with the variable/value pairs from the CLDR for language and region.

The format for each pair is `var = value`.

In addition to extracting CLDR data from the ICU Project website, this script also allows for overlay of FTL data from FTL files that are saved in the `/overlays` directory under the respective `/languages` or `/regions` subfolder. The overlaid data will overwrite existing variables with the same name or append new variables to the extracted CLDR data. The script does not differentiate between variable types in the overlay feature. Therefore, if a variable for some value that is not Language or Region is located in the `/overlays` directory, it will be added to the associated `resources.ftl` file.

The files in the `/overlays` directory are toys with arbitrary data.
