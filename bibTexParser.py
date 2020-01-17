import os
import argparse
from pylatexenc.latexencode import unicode_to_latex
from unidecode import unidecode

defEnc = 'utf-8-sig'
maxCitations = 1000

def getSubString(string, firstChar, secondChar,start=0):
    """
    Gives the substring of string between firstChar and secondChar. Starts looking from start. If it is unable to find a substring returns an empty string.
    """
    front = string.find(firstChar,start)
    back = string.find(secondChar,front+1)
    if front > -1 and back > -1:
        return (string[front+1:back],back)
    else:
        return ("",-1)


class entry:
    def __init__(self, stringEntry):
        self.attributes = {} #This holds all the information stored in a bibTex entry. 
        self.parseStringEntry(stringEntry)

    def parseStringEntry(self, stringEntry):
            """
            Assuming a string of the form:
            @article{RN14,\n   
            author = {Anderson, DM and Worster, M Grae and Davis, Stephen H},\n   
            title = {The case for a dynamic contact angle in containerless solidification},\n   
            journal = {Journal of crystal growth},\n   
            volume = {163},\n   
            number = {3},\n   
            pages = {329-338},\n   
            ISSN = {0022-0248},\n   
            year = {1996},\n   
            type = {Journal Article}\n}

            Give or take some additonal \ns. 
            """
            (subString,index) = getSubString(stringEntry,"@","{",0)
            self.attributes['flag'] = subString.strip()

            (subString,index) = getSubString(stringEntry,"{",",",0)
            self.attributes['key'] = subString.strip()

            while (subString,index) != ("",-1):
                (attribute,index) = getSubString(stringEntry,",","=",index)
                (subString,index) = getSubString(stringEntry,"{","}",index)
                if attribute != "" and subString != "": #This line seems redundant but it stops an empty string from being added to the dicitonary.
                    self.attributes[attribute.strip()] = subString.strip()

    def formatKey(self, form="author-year",delim="-"):
        """
        Given a form, returns a simplified (no fancy chars) string to be the new key. If no key can be formed given the form, the original key is returned.

        the syntax for form is bibTex entry attributes seprated by hypens, e.g. author-year will return a key with the first author, followed by the year. 

        For attributes which are composed of multiple words, like authors or titles, the first word will be used. 

        Words like "The" will SHOULD BE excluded. But this has not been incorportated yet.
        """
        newKey = ""
        for var in form.split(delim):
            if var in self.attributes:
                rawVar = self.attributes[var]

                commaLoc = rawVar.find(",")
                spaceLoc = rawVar.find(" ")
                if commaLoc == -1 and spaceLoc == -1: #If there is niether a comma or space
                    newKey += rawVar
                elif commaLoc > 0 and spaceLoc > 0:
                    if commaLoc < spaceLoc: #I'm pretty sure these can't be the same.
                        newKey += rawVar[:commaLoc] #if the comma is closer
                    else:
                        newKey += rawVar[:spaceLoc] #if the space is closer
                elif commaLoc > 0 and spaceLoc < 0: #if there is no space, but there is a comma
                    newKey += rawVar[:commaLoc]
                elif commaLoc < 0 and spaceLoc > 0: #if there is no comma but there is a space
                    newKey += rawVar[:spaceLoc]

        if newKey == "":
            return self.attributes["key"]
        else:
            return unidecode(newKey)

    def exportEntry(self,keyVal):
        stringEntry = f"@{self.attributes['flag']}{{{keyVal},\n"
        for var in self.attributes: #Itterating through the dictionary
            if not var == "key" and not var == "flag":
                stringEntry = stringEntry + f" {var} = {{{unicode_to_latex(self.attributes[var])}}},\n"
        stringEntry = stringEntry[:-2] + "\n}" #Trims empty entry from list b/c of the exit condition I used in the while loop.

        return stringEntry




class bib:
    def __init__(self, path, enc = defEnc):
        self.bib = []

        self.importBib(path, enc = enc)

    def importBib(self, path, enc = defEnc):
        count = 0 #definitely not infinite loop protection b/c I'm totally confident in my exit condition.

        with open(path,"r", encoding = enc) as f:
            raw = f.read() #Imports raw bibTex file as a string. 

        start = raw.find("@") #Find the first entry.
        end = raw.find("@",start + 1) #Find the second entry
        while start > -1 and count < maxCitations: #While there are still entries.
            self.bib.append(entry(raw[start:end])) #Create an entry with the portion of the string.

            start=end #repeat process with next entry.
            end = raw.find("@",start + 1)

            count += 1

    def exportBib(self, path, form = "author-year", delim = "-",enc = defEnc):
        keys = []
        with open(path,"w",encoding = enc) as f:
            for entry in self.bib:
                #this gets a formatted key.
                key = entry.formatKey(form=form,delim=delim)

                #This loop deal with potential duplicate keys by adding a number to the end of the string.
                count=2
                newKey = key
                while newKey in keys:
                    newKey = key + "-" + str(count)
                keys.append(newKey)

                stringEntry = entry.exportEntry(newKey)
                f.write(stringEntry+"\n\n")


if __name__ == '__main__':
    parse=argparse.ArgumentParser()
    parse.add_argument("-r", "--root", dest="root", help="path to bibTex file.")
    parse.add_argument("-o", "--output", dest="output", help="new filename path")
    args = parse.parse_args()

    if os.path.exists(args.root):
        biblio = bib(args.root)
        if not os.path.exists(args.output):
            biblio.exportBib(args.output)
        else:
            print("Output file already exists")
    else:
        print("Could not find root file.")

#"@article{RN14,author = {Anderson, DM and Worster, M Grae and Davis, Stephen H},title = {The case for a dynamic contact angle in containerless solidification},journal = {Journal of crystal growth},volume = {163},number = {3},pages = {329-338},ISSN = {0022-0248},year = {1996},type = {Journal Article}}"

#"@article{RN9,author = {Méndez-Velasco, Carlos and Goff, H Douglas},title = {Fat structure in ice cream: A study on the types of fat interactions},journal = {Food Hydrocolloids},volume = {29},number = {1},pages = {152-159},ISSN = {0268-005X},year = {2012},type = {Journal Article}}"