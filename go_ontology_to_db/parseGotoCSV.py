"""
@name: kschlum
@date: 02-07-18
@description: take xml from uniprot and conver to csv file to insert into SQL db
each csv file is attribute from uniport db. ie. protein, subcellular location
"""


import time
import	sys
from xml.etree import ElementTree as ET

xmlFile = open(sys.argv[1])

parser = ET.iterparse(xmlFile)
goFile = open("goAnnotationsUpdated.txt", "w")
protSeqFile = open("protSeqUpdated.txt", "w")


uri = '{http://uniprot.org/uniprot}'
# count = 0
for event, element in parser:
    if element.tag == uri + 'entry':
#        uniprotName = ""
#        uniprotNames = element.findall(uri + 'name')
#        if len(uniprotNames) > 0:
#            uniprotName = uniprotNames[0].text

        """
            get primary accession number
        """
        primaryUniprotAccessID = ""
        uniprotAccessIDs = element.findall(uri + 'accession')
        if len(uniprotAccessIDs) > 0:
        #            print "primaryUniprotAccessID"
            primaryUniprotAccessID = uniprotAccessIDs[0].text

            """
            get go terms annotaiton 

            """	
        dbRefs = element.findall(uri + 'dbReference')
        if len(dbRefs) > 0:
            for f in range(0, len(dbRefs)):
                 if dbRefs[f].attrib['type'] == 'GO':
                    goID = ""
                    goTerm = ""
                    goEvidence = ""
                    goProj = ""
                    goID = dbRefs[f].get('id').rstrip()
                    properties = dbRefs[f].findall(uri + 'property')
                    for prop in properties:
                            if prop.attrib['type'] == 'evidence':
                                goEvidence = prop.get('value')
                            if prop.attrib['type'] == 'term':
                                goTerm = prop.get('value')
                            if prop.attrib['type'] == 'project':
                                goProj = prop.get('value')
                    if goID is not None:
                        goFile.write(str(primaryUniprotAccessID).rstrip() + "," + str(goID).rstrip().replace(",", "") + "," + str(goTerm).rstrip().replace(",", "") + "," + str(goEvidence).rstrip().replace(",","") + "," + str(goProj).rstrip().replace(",","") + "\n")
        element.clear()

xmlFile.close()
goFile.close()
protSeqFile.close()
