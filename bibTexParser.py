defEnc = 'utf-8-sig'
maxCitations = 1000

class entry:
    def __init__(self, stringEntry):
        self.key = None
        self.author = None
        self.title = None
        self.journal = None
        self.year = None
        self.type = None

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
        attributes = vars(self) #This gets a dictionary of all the class variables and thier assocatied values.
        for var in attributes: #Itterating through the dictionart
            if var == "key":
                init = stringEntry.find("@") #The key isn't labeled so the closest thing is the @ at the start of the bibTex entry.
                if init > -1:
                    front = stringEntry.find("{",init)+1 #look for the front bracket before the key
                    back = stringEntry.find(",",init) #Look for the comma after the key.
                    attributes[var] = stringEntry[front:back] #Set the key to part of the string.
            else:
                init = stringEntry.find(var) #Find the posistion of the label.
                if init > -1:
                    front = stringEntry.find("{",init)+1 #Look for the front bracket of the label's entry.
                    back = stringEntry.find("}",init) #Look for the back bracket of the label's entry.
                    attributes[var] = stringEntry[front:back] #Set the label to part of the string.


class bib:
    def __init__(self, path, enc = defEnc):
        self.bib = []

        self.importFile(path, enc = enc)

    def importFile(self, path, enc):
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







if __name__ == '__main__':
    print("Whoa, slow down there cowboy.")

"""
testStringEntry = "@article{RN14,\n   author = {Anderson, DM and Worster, M Grae and Davis, Stephen H},\n   title = {The case for a dynamic contact angle in containerless solidification},\n   journal = {Journal of crystal growth},\n   volume = {163},\n   number = {3},\n   pages = {329-338},\n   ISSN = {0022-0248},\n   year = {1996},\n   type = {Journal Article}\n}\n\n"

testEntry = entry(testStringEntry)

print(f"{testEntry.key} {testEntry.year}")

testBib = bib("C:\\Users\\mathe\\Desktop\\CrystalComets.bib")
"""
