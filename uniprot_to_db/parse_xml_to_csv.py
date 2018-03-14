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

proteinFile = open("proteiNames.csv", "w")
proteinFile.write("uniprotID" + "," + "fullName" +"," + "ShortName" + "\n")
protAltFile = open("proteiAlternate.csv", "w")
protAltFile.write("uniprotID" + "," + "alternateFullName" +","+"alternateShortName"+"\n")

geneFile = open("geneNames.csv", "w")
geneFile.write("uniprotID" +","+ "geneName" + "\n")

organismFile = open("organismNames.csv", "w")
organismFile.write("uniprotID" + "," + "scientificName" + "," + "commonName" + "\n")

taxonomyFile = open("taxonomyNames.csv", "w")
taxonomyFile.write("uniprotID" + "," + "ncbiTAXID" + "\n")
taxLinFile = open("taxonomyLineage.csv", "w")
taxLinFile.write("uniprotID" + "," + "taxon" + "\n")
#
#binaryInterFile = open("binaryInteractions.csv", "w")
#binaryInterFile.write("uniprotID" + "," + "inter1" + "," +"inter2" + "," + "id" +"," + "label" +"," + "orgDiffer" +"," + "experiment" + "\n")

subcellLocFile = open("subcellularLocations.csv", "w")
subcellLocFile.write("uniprotID" + "," + "location" + "," + "locationTopology" + "\n")

functionFile = open("functions.csv", "w")
functionFile.write("uniprotID" + "," + "textEvid" + "," + "textFunct" + "\n")

subunitFile = open("subunits.csv", "w")
subunitFile.write("uniprotID" + "," + "subunitEvid" + "," + "subunitTxt" + "\n")
#goFile = open("goAnnotations.txt", "w")
#protSeqFile = open("protSeq.txt", "w")


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
                geneName = geneN[0].text	
            geneFile.write(uniprotName.strip() + ","+ geneName.strip() +"\n")
        """
            find protein names; save in variable
        """
        protFullNames = element.findall(uri + 'protein')
        for protN in protFullNames:
            protFullName = ""
            protShortName = ""
            alterNameList = ""
            protFullAltName = ""
            protShortAltName = ""
            protFullAltNameList = []
            protShortAltNameList = []
            protRecomndNames = protN.findall(uri + 'recommendedName')
            if len(protRecomndNames) > 0:
                for protRName in protRecomndNames:
                    protFullNames = protRName.findall(uri + 'fullName')
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
                        protFullAltName = protAlt.text
                    protShortAltNames = protAltN.findall(uri + "shortName")
                    for protAltS in protShortAltNames:
                        protShortAltName = protAltS.text
                    protAltFile.write(str(uniprotName).rstrip().replace(",","") + "," +str(protFullAltName).rstrip().replace(",","") + "," + str(protShortAltName).rstrip().replace(",","") + "\n")
            proteinFile.write(str(uniprotName)+","+str(protFullName).rstrip().replace(",", "")+","+str(protShortName).rstrip().replace(",", "")+"\n")

        """
        parse scientific name, common name, taxonomy ID, and taxonomy lineage
        """
        organismName = element.findall(uri + 'organism')
        for org in organismName:
            scientificName = ""
            commonName = ""
            scientificNames = org.findall(uri + 'name')
            if len(scientificNames) > 0:
                if scientificNames[0].attrib['type'] == 'scientific':
                    scientificName = scientificNames[0].text
            if len(scientificNames) > 1:
                if 	len(scientificNames[1].text) > 0: 
                    if 	scientificNames[1].attrib['type'] == 'common':
                        commonName = scientificNames[1].text
            organismFile.write(str(uniprotName).rstrip()+","+str(scientificName).rstrip().replace(",", "")+","+str(commonName).rstrip().replace(",", "")+"\n")	

        """
        get ncbi taxnomy ID
        """
        taxonomyIDs = org.findall(uri + 'dbReference')
        if len(taxonomyIDs) > 0:
            ncbiTAXID = ""
            if taxonomyIDs[0].attrib['type'] == 'NCBI Taxonomy':
                ncbiTAXID = taxonomyIDs[0].get('id')
        taxonomyFile.write(str(uniprotName).rstrip()+","+str(ncbiTAXID).rstrip().replace(",", "") +"\n")
        """
        get taxon lineage
        """
        lineages = org.findall(uri + 'lineage')
        for lines in lineages:
            taxons = lines.findall(uri + 'taxon')
            taxon = ""
            for taxonName in taxons:
                taxon = taxonName.text
                taxLinFile.write(str(uniprotName).rstrip()+","+str(taxon).rstrip().replace(",", "") + "\n")
                # print taxon, uniprotName
        """
        get function text and function text evidence numbers
        """
        functionText = ""
        comments = element.findall(uri + 'comment')
        for comment in comments:
            if len(comment) > 0:
                if comment.attrib['type'] == 'function':
                    # print comment
                    textEvids = comment.findall(uri + 'text')
                    textEvid = ""
                    textFunct = ""
                    if len(textEvids) > 0: 
                        # print textEvids
                        for textE in textEvids:
                            textEvid = textE.get('evidence')
                            # print textEvid
                            textFunct = textE.text
                        functionFile.write(str(uniprotName).rstrip() + "," + str(textEvid).rstrip().replace(",","") + "," + str(textFunct).rstrip().replace(",","") + "\n")

            """
                get subunit text and subunit text evidence numbers
            """
            if comment.attrib['type'] == 'subunit':
                subnitEvids = comment.findall(uri + 'text')
                subunitEvid = ""
                subunitTxt = ""
                if len(subnitEvids) > 0: 
                    for subunitE in subnitEvids:
                        subunitEvid = subunitE.get('evidence')
                        subunitTxt = subunitE.text
                        if subunitEvid is not None:
                            if subunitTxt is not None:
                                subunitFile.write(str(uniprotName).rstrip() + "," + str(subunitEvid).rstrip().replace("," ,"") + "," + str(subunitTxt).rstrip().replace(",", "") + "\n")
                            else:
                                subunitFile.write(str(uniprotName).rstrip() + "," + str(subunitEvid).rstrip().replace("," ,"") + "\n")
#            """
#                get binary interaction information
#            """
#            if comment.attrib['type'] == 'interaction':
#                inter1 = ""
#                inter2 = ""
#                id = ""
#                label = ""
#                orgDiffer = ""
#                experiment = ""
#                if 'intactId' in comment[0].attrib:
#                    inter1 = comment[0].get('intactId')
#                if 'intactId' in comment[1].attrib:
#                    inter2 = comment[1].get('intactId')
#                ids = comment[1].findall(uri + 'id')
#                if len(ids) > 0:
#                    id = ids[0].text
#                labels = comment[1].findall(uri + 'label')
#                if len(labels) > 0:
#                    label = labels[0].text
#                orgDiffers = comment.findall(uri + 'organismsDiffer')
#                if len(orgDiffers) > 0:
#                    orgDiffer = orgDiffers[0].text
#                experiments = comment.findall(uri + 'experiments')
#                if len(experiments) > 0:
#                    experiment = experiments[0].text
#                binaryInterFile.write(str(uniprotName).rstrip() + "," + str(inter1).rstrip().replace(",", "") + "," + str(inter2).rstrip().replace(",", "") + "," + str(id).rstrip().replace(",", "") + "," + str(orgDiffer).rstrip().replace(",", "") + "," + str(experiment).rstrip().replace(",", "") + "\n")
#            """
#                get subcellular location 
#            """
#            if comment.attrib['type'] == 'subcellular location':
#                subLocations = comment.findall(uri + 'subcellularLocation')
#                for subLocation in subLocations:
#                    location = ""
#                    toplogyTexts = []
#                    topText = ""
#                    locations = subLocation.findall(uri + 'location')
#                    if len(locations) > 0:
#                        for loc in locations:
#                            location = loc.text
#                    topology = subLocation.findall(uri + 'topology') 
#                    if len(topology) > 0: 
#                        for top in topology:
#                            topText = top.text
#                    subcellLocFile.write(str(uniprotName).rstrip().replace(",", "") +"," + str(location).rstrip().replace(",", "") + "," + str(t).rstrip().replace(",", "") + "\n")
#
#        """
#        get go terms annotaiton 
#
#        """	
#        goID = ""
#        goTerm = ""
#        goEvidence = ""
#        goProj = ""
#        dbRefs = element.findall(uri + 'dbReference')
#        if len(dbRefs) > 0:
#         for f in range(0, len(dbRefs)):
#             if dbRefs[f].attrib['type'] == 'GO':
#                 goID = dbRefs[f].get('id')
#                 properties = dbRefs[f].findall(uri + 'property')
#                 for prop in properties:
#                    goID = ""
#                    goTerm = ""
#                    goEvidence = ""
#                    goProj = ""
#                    if prop.attrib['type'] == 'evidence':
#                        goEvidence = prop.get('value')
#                    if prop.attrib['type'] == 'term':
#                        goTerm = prop.get('value')
#                    if prop.attrib['type'] == 'project':
#                        goProj = prop.get('value')
#                    goFile.write(str(uniprotName).rstrip() + "," + str(goID).rstrip().replace(",", "") + "," + str(goTerm).rstrip().replace(",", "") + "," + str(goEvidence).rstrip().replace(",","") + "," + str(goProj).rstrip().replace(",","") + "\n")
#
        element.clear()

xmlFile.close()
geneFile.close()
proteinFile.close()
protAltFile.close()
organismFile.close()
taxonomyFile.close()
taxLinFile.close()
#binaryInterFile.close()
subcellLocFile.close()
functionFile.close()
subunitFile.close()
#goFile.close()
#protSeqFile.close()
