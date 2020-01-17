# bibTexParser
Import bibTex files and have excess the the different attributes of each entry. Conveinet for reformating the keys. Mostly created because the default endnote bibTex output uses the archive order (the order you added things to the endnote doc) as the keys which is pretty useless.

version 1: Two classes exists:

entry is a bibTex entry. It is initailized with a raw string of the entry it will be representing. It then parses out the differnt attributes and stores them in similar named class variables.

bib is a holder for a bunch of entries. It has one variable bib.bib which is a list of entries. It is intialized with a path to the bibTex file. It then creates a list of entry objects.

version 2: reformatting and exporting methods added.

the entry class now has a function exportEntry((str) keyVal) which returns a string bibTex entry. The value given for keyVal will be in the key posistion.

This function is used in the bib class function exportBib(path) which exports a file containing all the entries stored in bib.bib. The keys are autoformatted to be firstAuthorYear. 

Current issues is that accents and stuff are not in latex format. So they still won't be properly imported in latex. 

v6
Formatting for latex symbols is autmatically implemented when a file is processed. Keys are autmatically formatted in unicode characters. The format of the key can now be formatted be providing a pattern "x-y-z" where z,y, and z are attributes of the entry. Non-existant attributes will not be added to the key. 
