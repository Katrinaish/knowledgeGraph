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
proteinFile = open("proteiNames.txt", "w")

uri = '{http://uniprot.org/uniprot}'
# count = 0
for event, element in parser:
    if element.tag == uri + 'entry':
        """
            find uniprot name; name under accession nums 
        """
        uniprotName = ""
        uniprotNames = element.findall(uri + 'name')
        if len(uniprotNames) > 0:
            uniprotName = uniprotNames[0].text

            """
                find gene names tag; save in variable
            """
		geneNames = element.findall(uri + 'gene')
		for geneN in geneNames:
			geneName = ""
			gene = geneN.findall(uri + 'name')
			if len(gene) > 0:
				# not sure if want to check primary/secondary; for now ignore
				# if geneN[0].attrib['type'] == 'primary':
				geneName = geneN[0].text	
				if len(geneName) > 0:
					geneFile.write(uniprotName + ","+ geneName +"\n")
		# print geneName
            """
                find protein names; save in variable
            """
		protFullNames = element.findall(uri + 'protein')
		for protN in protFullNames:
			protFullName = ""
			protShortName = ""
			alterNameList = ""
			protFullAltNameList = []
			protShortAltNameList = []
			protRecomndNames = protN.findall(uri + 'recommendedName')
			if len(protRecomndNames) > 0:
				for protRName in protRecomndNames:
					protFullNames = protRName.findall(uri + 'fullName')
					#Need to parse full name for all protefullanmes; check if more than one in for loop
					for protFullName in protFullNames:
						protFullName = protFullName.text
					protShortNames = protRName.findall(uri + 'shortName')
					for protShortName in protShortNames:
						protShortName = protShortName.text
			protAltNames = protN.findall(uri + "alternativeName")
			if len(protAltNames) > 0:
				for protAltN in protAltNames:
					protFullAltNames = protAltN.findall(uri + "fullName")
					for protAlt in protFullAltNames:
						protFullAltNameList.append(protAlt.text)
					protShortAltNames = protAltN.findall(uri + "shortName")
					for protAltS in protShortAltNames:
						protShortAltNameList.append(protAltS.text)
				for p in protFullAltNameList:
					protAltFile.write(str(uniprotName).rstrip().replace(",","") + "," +str(p).rstrip().replace(",","") + "\n")

			if len(protFullName) > 0:
				if len(protShortName) > 0:
					proteinFile.write(str(uniprotName)+","+str(protFullName).rstrip().replace(",", "")+","+str(protShortName).rstrip().replace(",", "")+"\n")
				else:
					proteinFile.write(str(uniprotName)+","+str(protFullName).rstrip().replace(",", "")+"\n")
    element.clear()

xmlFile.close()
goFile.close()
protSeqFile.close()
