
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
protSeqFile = open("protSeqUpdated2_21.txt", "w")
protSeqFile.write("accessionID" + "," + "length" + "," + "mass" + "," + "checksum" + "," + "modified" + "," + "version" + "," + "sequence" + "\n")

""""
parse out the protein sequence and proteing length, mass, checksum, modified and version information
<sequence length="255" mass="29174" checksum="07817CCBD1F75B26" modified="2004-07-05" version="1">
"""
uri = '{http://uniprot.org/uniprot}'
# count = 0
for event, element in parser:
    if element.tag == uri + 'entry':

        """
            get primary accession number
        """
        primaryUniprotAccessID = ""
        uniprotAccessIDs = element.findall(uri + 'accession')
        if len(uniprotAccessIDs) > 0:
        #            print "primaryUniprotAccessID"
            primaryUniprotAccessID = uniprotAccessIDs[0].text

        sequences = element.findall(uri + 'sequence')
        if len(sequences) > 0:
            for sequence in sequences:
                protSeqTxt = ""
                protSeqL = ""
                protSeqM = ""
                protCkSum = ""
                protMod = ""
                protVer = ""
                if sequence.get('length') is not None:
                    protSeqL = sequence.get('length').strip().replace(",", " ")
                if sequence.get('mass') is not None:
                    protSeqM = sequence.get('mass').strip().replace(",", " ")
                if sequence.get('checksum') is not None:
                    protCkSum = sequence.get('checksum').strip().replace(",", " ")
                if sequence.get('modified') is not None:
                    protMod = sequence.get('modified').strip().replace("," , " ")
                if sequence.get('version') is not None:
                    protVer = sequence.get('version').strip().replace("," , " ")
                if sequence.text is not None:
                    protSeqTxt	= sequence.text.strip().replace('\n', '')
                protSeqFile.write(primaryUniprotAccessID+","+protSeqL+","+protSeqM+","+protCkSum+","+protMod+","+protVer+","+protSeqTxt+"\n")

        element.clear()
protSeqFile.close()
