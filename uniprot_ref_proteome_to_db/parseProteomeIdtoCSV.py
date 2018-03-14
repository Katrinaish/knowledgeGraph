"""
@name: kschlum
@date: 02-07-18
@description: take xml from uniprot and convert to csv file to insert into SQL
each csv file is attribute from uniport db.
attributes:
ids in other dbs
uniprot proteome DB

"""


import time
import	sys
from xml.etree import ElementTree as ET

xmlFile = open(sys.argv[1])

parser = ET.iterparse(xmlFile)
proteomeIDFile = open("uniprotProteomeIDs.csv", "w")
proteomeIDFile.write("primaryAccessID" + "," + "proteomeID" + "\n")


uri = '{http://uniprot.org/uniprot}'
for event, element in parser:
    if element.tag == uri + 'entry':

        uniprotAccessID = ""
        primaryUniprotAccessID = ""
        uniprotAccessIDs = element.findall(uri + 'accession')
        if len(uniprotAccessIDs) > 0:
            primaryUniprotAccessID = uniprotAccessIDs[0].text

            """
            get proteome id

            """ 
            proteomeID = ""	
            dbRefs = element.findall(uri + 'dbReference')
            if len(dbRefs) > 0:
             for f in range(0, len(dbRefs)):
                if dbRefs[f].attrib['type'] == 'Proteomes':
                    proteomeID = dbRefs[f].get('id').replace(",", "")
        proteomeIDFile.write(primaryUniprotAccessID.strip().replace(",", "") + "," + proteomeID.strip().replace(",", "") + "\n") 

        element.clear()

xmlFile.close()
proteomeIDFile.close()
