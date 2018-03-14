"""
@name: kschlum
@date: 02-07-18
@description: take xml from uniprot and convert to csv file to insert into SQL db
each csv file is attribute from uniport db. 
attributes:
ids in other dbs
db:
ensembl
NCBI RefSeq
Intact
kegg
reactome
String
USC 
NCBI
"""


import time
import	sys
from xml.etree import ElementTree as ET

xmlFile = open(sys.argv[1])

parser = ET.iterparse(xmlFile)
allNamesFile = open("allNamesTrembl.csv", "w")
allNamesFile.write("uniprotID"+","+"primaryAccessID" + "," + "alterAccessIDList" +  "," + "geneName" + "," + "protFullName" + "," + "protShortName" + "," + "protFullAltNameList" + "," + "protShortAltNameList" + "," + "ncbiTAXID" + "," + "ensemblIDs" + "," + "ensemblMolID" + "," + "ensemblGeneIDs" + "," + "ensemblProteinIDs" + "," + "ncbiGeneID" + "," + "intActID"+ "," + "KEGGIds" + "," + "reactIDs" + "," + "reactPathwayValues" + "," + "refSeqIDs" + "," + "refSeqNucs" + "," + "stringID" + "," + "ucscID" + "," +  "emblID" + "," + "emblProtSeqID" + "\n")


uri = '{http://uniprot.org/uniprot}'
# count = 0
for event, element in parser:
    if element.tag == uri + 'entry':
        """
            find uniprot name; name under accession nums 
        """
        alterAccessIDList = []
        uniprotNames = element.findall(uri + 'name')
        if len(uniprotNames) > 0:
            uniprotName = uniprotNames[0].text

        uniprotAccessID = ""
        primaryUniprotAccessID = ""
        uniprotAccessIDs = element.findall(uri + 'accession')
        if len(uniprotAccessIDs) > 0:
#            print "primaryUniprotAccessID"
            primaryUniprotAccessID = uniprotAccessIDs[0].text
#            print primaryUniprotAccessID
            for accessID in uniprotAccessIDs[1:]:
                alterAccessIDList.append(accessID.text.replace(",", ""))
#                print "uniprotName"
#                print uniprotName
#        allNamesFile.write("\"" + uniprotName + "\"" + "," + "\"" +primaryUniprotAccessID+ "\"" +  "," + "\"" + str(uniprotNameList) + "\"" + "\n")


        geneNames = element.findall(uri + 'gene')
        for geneN in geneNames:
            geneName = ""
            gene = geneN.findall(uri + 'name')
            if len(gene) > 0:
                geneName = geneN[0].text.replace(",", "")	
#            allNamesFile.write(uniprotName.strip() + ","+ geneName.strip() +"\n")
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
                        protFullName = protFullName.text.replace(",", "")
                    protShortNames = protRName.findall(uri + 'shortName')
                    for protShortName in protShortNames:
                        protShortName = protShortName.text.replace(",", "")
            protAltNames = protN.findall(uri + "alternativeName")
            if len(protAltNames) > 0:
                for protAltN in protAltNames:
                    protFullAltNames = protAltN.findall(uri + "fullName")
                    for protAlt in protFullAltNames:
                        protFullAltNameList.append(protAlt.text.replace(",", ""))
                    protShortAltNames = protAltN.findall(uri + "shortName")
                    for protAltS in protShortAltNames:
                        protShortAltNameList.append(protAltS.text.replace(",", ""))
#                    protAltFile.write(str(uniprotName).rstrip().replace(",","") + "," +str(protFullAltName).rstrip().replace(",","") + "," + str(protShortAltName).rstrip().replace(",","") + "\n")
#            proteinFile.write(str(uniprotName)+","+str(protFullName).rstrip().replace(",", "")+","+str(protShortName).rstrip().replace(",", "")+"\n")

        """
        get ncbi taxnomy ID
        """
        organismName = element.findall(uri + 'organism')
        for org in organismName:
            taxonomyIDs = org.findall(uri + 'dbReference')
            if len(taxonomyIDs) > 0:
                ncbiTAXID = ""
                if taxonomyIDs[0].attrib['type'] == 'NCBI Taxonomy':
                    ncbiTAXID = taxonomyIDs[0].get('id').replace(",", "")
#        taxonomyFile.write(str(uniprotName).rstrip()+","+str(ncbiTAXID).rstrip().replace(",", "") +"\n")
        
            """
            get ensembl information

            """	
            geneID = ""	
            ensemblIDs = []
            ensemblMolIDs = []
            ensemblGeneIDs = []
            ensemblProteinIDs = []
            intactID = ""
            KEGGID = ""
            reactIDs = []
            reactPthwayVals = []
            refSeqIDs = []
            refSeqNucs = []
            refSeqProts = []
            stringID = ""
            ucscID = ""
            emblIDS = []
            emblProtSeqIDs = []
            emblProtStatus = []
            emblProtMolType = []
            emblMrnaIDs = []
            dbRefs = element.findall(uri + 'dbReference')
            if len(dbRefs) > 0:
             for f in range(0, len(dbRefs)):
                if dbRefs[f].attrib['type'] == 'Ensembl':
                    # print dbRefs[f].attrib
                    ensemblIDs.append(dbRefs[f].get('id').replace(",", ""))
                    #get molecular IDs
                    molecularIDs = dbRefs[f].findall(uri + 'molecule')
                    for molecularID in molecularIDs:
                        ensemblMolIDs.append(molecularID.get('id').replace(",", ""))
                    #get property protein and gene Ids
                    properties = dbRefs[f].findall(uri + 'property')
                    for prop in properties:
                        if prop.attrib['type'] == 'protein sequence ID':
                             ensemblProteinIDs.append(prop.get('value').replace(",", ""))
                        if prop.attrib['type'] == 'gene ID':
                             ensemblGeneIDs.append(prop.get('value').replace(",", ""))
                """
                get NCBI gene Refseq information

                """
                if dbRefs[f].attrib['type'] == 'GeneID':
                    geneID = dbRefs[f].get('id').replace(",", "")
                """
                    get intact information
                """
                if dbRefs[f].attrib['type'] == 'IntAct':
                    intactID = dbRefs[f].get('id').replace(",", "")    
                """
                    get kegg information
                """
                if dbRefs[f].attrib['type'] == 'KEGG':
                    KEGGID = dbRefs[f].get('id').replace(",", "")   

                """
                    get reactome ids, and pathway names
                """
                 
                if dbRefs[f].attrib['type'] == 'Reactome':
                    reactIDs.append(dbRefs[f].get('id').replace(",", ""))
                    #get property protein and reactome values
                    properties = dbRefs[f].findall(uri + 'property')
                    for prop in properties:
                        if prop.attrib['type'] == 'pathway name':
                             reactPthwayVals.append(prop.get('value').replace(",", ""))
                """
                    get Refseq sequences information
                """
                if dbRefs[f].attrib['type'] == 'RefSeq':
                    refSeqIDs.append(dbRefs[f].get('id').replace(",", ""))   
                 
                    #get property values
                    properties = dbRefs[f].findall(uri + 'property')
                    for prop in properties:
                        if prop.attrib['type'] == 'nucleotide sequence ID':
                             refSeqNucs.append(prop.get('value').replace(",", ""))
                """
                    get string id
                """
                if dbRefs[f].attrib['type'] == 'STRING':
                    stringID = dbRefs[f].get('id').replace(",", "")   
                """
                    get USC data
                """
                if dbRefs[f].attrib['type'] == 'UCSC':
                    ucscID = dbRefs[f].get('id').replace(",", "")   
                    #property info jsut have organism name value so ignoring for now 
                    #get property values
#                    properties = dbRefs[f].findall(uri + 'property')
#                    for prop in properties:
#                        if prop.attrib['type'] == 'organism name':
#                             refSeqNucs.append(prop.get('value'))

                """
                    get embl information
                """
                if dbRefs[f].attrib['type'] == 'EMBL':
                    emblIDS.append(dbRefs[f].get('id').replace(",", ""))
                    #get property protein and reactome values
                    properties = dbRefs[f].findall(uri + 'property')
                    for prop in properties:
                        if prop.attrib['type'] == 'protein sequence ID':
                             emblProtSeqIDs.append(prop.get('value').replace(",", ""))
                        

        allNamesFile.write("\"" + uniprotName + "\"" + "," + "\"" +primaryUniprotAccessID+ "\"" +  "," + "\"" + "|".join(alterAccessIDList) + "\"" + "," + "\"" + geneName + "\"" + "," + "\"" + protFullName + "\"" + "," + "\"" + protShortName + "\"" + ","+ "\"" + "|".join(protFullAltNameList) + "\"" + "," + "\"" + "|".join(protShortAltNameList) + "\"" + "," + "\"" + ncbiTAXID + "\"" + "," + "\"" + "|".join(ensemblIDs) + "\"" + "," + "\"" + "|".join(ensemblMolIDs) + "\"" + "," + "\"" + "|".join(ensemblGeneIDs) + "\""  + "," + "\"" + "|".join(ensemblProteinIDs) + "\""+ "," + "\"" + geneID + "\"" + "," + "\"" + intactID + "\"" + "," + "\"" + KEGGID + "\"" + "," + "\"" + "|".join(reactIDs) + "\"" + "," + "\"" + "|".join(reactPthwayVals) + "\"" + "," + "\"" + "|".join(refSeqNucs) + "\"" + "," + "\"" + "|".join(refSeqNucs) + "\"" + "," + "\"" + stringID + "\"" + "," + "\"" + ucscID + "\"" + "," + "\"" + "|".join(emblIDS) + "\"" + "," + "\"" + "|".join(emblProtSeqIDs) + "\"" + "\n")

        
#
#        """"
#        print protein sequences 
#        """	
#        protSeqs = element.findall(uri + 'sequence')
#        for protSeq in protSeqs:
#            protSeqTxt = ""
#            protSeqL = ""
#            protSeqM = ""
#            protCkSum = ""
#            protMod = ""
#            protVer = ""
#            if 'length' in protSeq.attrib:
#                protSeqL = protSeq.get('length')
#            if 'mass' in protSeq.attrib:
#                protSeqM = protSeq.get('length')
#            if 'checksum' in protSeq.attrib:
#                protCkSum = protSeq.get('checksum')
#            if 'modified' in protSeq.attrib:
#                protMod = protSeq.get('modified')	
#            if 'version' in protSeq.attrib:
#                protVer = protSeq.get('version')
#            protSeqTxt	= protSeq.text
#            if protSeqTxt is not None:
#                if protSeqL is not None:
#                    if protSeqM is not None: 
#                        if protCkSum is not None:
#                            if protMod is not None:
#                                if protVer is not None:
#                                    protSeqFile.write(str(uniprotName).rstrip() + "," + str(protSeqTxt).rstrip().replace(",", "") + "," + str(protSeqL).rstrip().replace(",", "") + "," + str(protSeqM).rstrip().replace(",", "") + "," + protCkSum.rstrip().replace(",", "") + "," + str(protMod).rstrip().replace(",", "") + "," + str(protVer).rstrip().replace(",", "") + "\n")
#                                else:
#                                    protSeqFile.write(str(uniprotName).rstrip() + "," + str(protSeqTxt).rstrip().replace(",", "") + "," + str(protSeqL).rstrip().replace(",", "") + "," + str(protSeqM).rstrip().replace(",", "") + "," + protCkSum.rstrip().replace(",", "") + "," + str(protMod).rstrip().replace(",", "") +  "\n")
#                            else:
#                                protSeqFile.write(str(uniprotName).rstrip() + "," + str(protSeqTxt).rstrip().replace(",", "") + "," + str(protSeqL).rstrip().replace(",", "") + "," + str(protSeqM).rstrip().replace(",", "") + "," + protCkSum.rstrip().replace(",", "") + "\n")
#                        else:
#                            protSeqFile.write(str(uniprotName).rstrip() + "," + str(protSeqTxt).rstrip().replace(",", "") + "," + str(protSeqL).rstrip().replace(",", "") + "," + str(protSeqM).rstrip().replace(",", "") + "\n")
#                    else:
#                        protSeqFile.write(str(uniprotName).rstrip() + "," + str(protSeqTxt).rstrip().replace(",", "") + "," + str(protSeqL).rstrip().replace(",", "")  + "\n")
#                else:
#                    protSeqFile.write(str(uniprotName).rstrip() + "," + str(protSeqTxt).rstrip().replace(",", "") + "\n")
#                
#            print protSeqL, protSeqM, protCkSum, protMod, protVer 
#            print protSeqTxt
        element.clear()

xmlFile.close()
allNamesFile.close()
