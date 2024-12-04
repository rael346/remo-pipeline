Place your configs here.

A config is a json file with file regex(pattern specific to the object being parsed which can be used to select the correct config type), grain path(an xpath to the object we need to grab a list of from within the xml. e.g. we have an xml with book tags just beneath the root, and we need to parse each book. Therefore the grain path is the path to a book from the root.) and a list of column  dictionaries which have a name(column name) and a path(the xpath from the grain to the column).

Import get_configs() from configs.py to grab all the configs you have dumped in this directory. The name of the file without the extension becomes the key that retrieves the config for each file from the dictionary returned by get_configs().