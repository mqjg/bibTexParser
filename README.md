# bibTexParser
Import bibTex files and have excess the the different attributes of each entry. Conveinet for reformating the keys.

version 1: Two classes exists:

entry is a bibTex entry. It is initailized with a raw string of the entry it will be representing. It then parses out the differnt attributes and stores them in similar named class variables.

bib is a holder for a bunch of entries. It has one variable bib.bib which is a list of entries. It is intialized with a path to the bibTex file. It then creates a list of entry objects.
