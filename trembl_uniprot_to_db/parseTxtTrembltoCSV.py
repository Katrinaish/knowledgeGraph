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
import sys
from collections import defaultdict
#import psycopg2
#from config import config

fname = sys.argv[1]
def to_name(d):
    name = ''
    if len(d) > 0:
        name = d[0]
    return name

def to_array(d):
    array = '{}'
    if d:
        array = '{"'+d[0]
        if len(d) > 1:
            for i in range(1,len(d)):
                array += '","'+d[i]
        array += '"}'
    return array

def to_join(d):
    final = d
#    print len(d)
    if len(d) > 3:
        final = "|".join(d)
    return final
 
allNamesFile = open('allNamesUpdatedTremblOne.csv', 'w')
allNamesFile.write('uniprotID,primaryAccessID,alterAccessIDListArray,geneName,geneSynonymList, geneOrfNameList, geneLocusNameList,protFullName,'
                    'protShortName,protFullAltNameListArray,protShortAltNameList,'
                    'ncbiTAXID,ensemblIDsArray,ensemblMolIDsArray,ensemblGeneIDsArray,ensemblProteinIDsArray,'
                    'geneID,intActID,KEGGIds,reactIDsArray,reactPathwayValsArray,refSeqIDsArray,'
                    'refSeqNucsArray,stringID,ucscID,emblIDsArray,emblProtSeqIDsArray,\n')

def add_object(d):
    uniprotName = str(d['ID'][0]).strip()
    primaryUniprotAccessID = to_name(d['AC'])
    if len(d['AC']) > 1: 
        alterAccessIDListArray = to_array(d['AC'])
    else:
        alterAccessIDListArray = "{}" 
    geneName = to_name(d['GN'])
    if len(d['GNSyn']) > 1:
        geneSynonymList = to_array(d['GNSyn'])
    else:
        geneSynonymList = to_name(d['GNSyn']) 
    geneOrfNameList = to_array(d['GNORF'])
    geneLocusNameList = to_array(d['GNOLN'])
    protFullName = to_name(d['DERF'])
    protShortName = to_name(d['DERS'])
    protFullAltNameListArray= to_array(d['DEAF'])
    protShortAltNameListArray = to_array(d['DEAS'])
    ncbiTAXID = to_name(d['OXID'])
    ensemblIDsArray = to_array(d['DREnsembl'])
    ensemblMolIDsArray = to_array(d['DREnsemblMolID'])
    ensemblGeneIDsArray = to_array(d['DREnsemblGeneID'])
    ensemblProteinIDsArray = to_array(d['DREnsemblProteinID'])
    geneID = to_name(d['DRGeneID'])
    intactID = to_name(d['DRIntAct'])
    KEGGID = to_name(d['DRKEGG'])
    reactIDsArray = to_array(d['DRReactome'])
    reactPthwayValsArray = to_array(d['DRReactomePN'])
    refSeqIDsArray = to_array(d['DRRefSeq'])
    refSeqNucsArray = to_array(d['DRRefSeqNSID'])
    stringID = to_name(d['DRSTRING'])
    ucscID = to_name(d['DRUCSC'])
    emblIDsArray = to_array(d['DREMBL'])
    emblProtSeqIDsArray = to_array(d['DREMBLProtSeqID'])
   
    allNamesFile.write("\"" + uniprotName + "\"" + "," + 
                       "\"" +primaryUniprotAccessID+ "\"" +  "," + 
                       "\"" + to_join(alterAccessIDListArray) + "\"" + "," + 
                       "\"" + geneName + "\"" + "," +
                       "\"" + geneSynonymList + "\"" + "," +
                       "\"" + geneOrfNameList + "\"" + "," +
                       "\"" + geneLocusNameList + "\"" + "," +
                       "\"" + protFullName + "\"" + "," + 
                       "\"" + protShortName + "\"" + ","+ 
                       "\"" + to_join(protFullAltNameListArray) + "\"" + "," + 
                       "\"" + to_join(protShortAltNameListArray) + "\"" + "," + 
                       "\"" + ncbiTAXID + "\"" + "," + 
                       "\"" + to_join(ensemblIDsArray) + "\"" + "," + 
                       "\"" + to_join(ensemblMolIDsArray) + "\"" + "," + 
                       "\"" + to_join(ensemblGeneIDsArray) + "\""  + "," + 
                       "\"" + to_join(ensemblProteinIDsArray) + "\""+ "," + 
                       "\"" + geneID + "\"" + "," + 
                       "\"" + intactID + "\"" + "," + 
                       "\"" + KEGGID + "\"" + "," + 
                       "\"" + to_join(reactIDsArray) + "\"" + "," + 
                       "\"" + to_join(reactPthwayValsArray) + "\"" + "," + 
                       "\"" + to_join(refSeqIDsArray) + "\"" + "," + 
                       "\"" + to_join(refSeqNucsArray) + "\"" + "," + 
                       "\"" + stringID + "\"" + "," + 
                       "\"" + ucscID + "\"" + "," + 
                       "\"" + to_join(emblIDsArray) + "\"" + "," + 
                       "\"" + to_join(emblProtSeqIDsArray) + "\"" + "\n")
    # insert records
#    cur.execute(sql,(primaryUniprotAccessID,
#                     uniprotName, 
#                     geneName,
#                     geneSynonymList,
#                     geneOrfNameList,
#                     geneLocusNameList,
#                     protFullName,
#                     protShortName, 
#                     ncbiTAXID,
#                     geneID,
#                     intactID,
#                     stringID,
#                     ucscID,
#                     emblIDSArray,
#                     emblProtSeqIDsArray,
#                     protFullAltNameListArray,
#                     protShortAltNameListArray,
#                     alterAccessIDListArray,
#                     ensemblMolIDsArray,
#                     ensemblIDsArray,
#                     ensemblGeneIDsArray,
#                     ensemblProteinIDsArray,
#                     KEGGID, 
#                     reactIDsArray,
#                     reactPthwayValsArray,
#                     refSeqIDsArray,
#                     refSeqNucsArray))

start = time.time()
count = 0
#sys.path.insert(0, "/home/kpe/data/goTerms/obo")
fname = sys.argv[1]
#fname = '/mnt/knowledgeGraphData/tremblUniprot/uniprot_trembl.dat'
#fname = 'uniprot-2.txt'

#""" create table in the PostgreSQL database"""
#commands = (
#    """
#    DROP TABLE IF EXISTS trembl_vertices;
#    """,
#    """
#    CREATE TABLE trembl_vertices (
#        name_id SERIAL PRIMARY KEY,
#        primary_accessID VARCHAR(255) NOT NULL,
#        uniprot_ID VARCHAR(255) NOT NULL,
#        geneName TEXT NOT NULL,
#        geneSynonymList VARCHAR[], 
#        geneOrfNameList VARCHAR[], 
#        geneLocusNameList VARCHAR[], 
#        protFullName TEXT,
#        protShortName VARCHAR(255),
#        ncbiTAXID VARCHAR(255),
#        ncbiGeneID VARCHAR(255),
#        intActID VARCHAR(255),
#        stringID VARCHAR(255), 
#        ucscID VARCHAR(255), 
#        emblID VARCHAR[], 
#        emblProtSeqID VARCHAR[],
#        protFullAltNameListArray VARCHAR[],
#        protShortAltNameList VARCHAR[],
#        alterAccessIDList VARCHAR[],
#        ensemblMolID VARCHAR[],
#        ensemblIDs VARCHAR[],
#        ensemblGeneIDs VARCHAR[],
#        ensemblProteinIDs VARCHAR[],
#        KEGGIds TEXT,
#        reactIDs VARCHAR[],
#        reactPathwayValues VARCHAR[], 
#        refSeqIDs VARCHAR[], 
#        refSeqNucs VARCHAR[] 
#    )
#    """)
#sql = """INSERT INTO trembl_vertices(primary_accessID, uniprot_ID, geneName, geneSynonymList, 
#        geneOrfNameList, geneLocusNameList, protFullName, protShortName, ncbiTAXID, 
#        ncbiGeneID, intActID, stringID, ucscID, emblID, emblProtSeqID, protFullAltNameListArray, 
#        protShortAltNameList, alterAccessIDList, ensemblMolID, ensemblIDs, ensemblGeneIDs, 
#        ensemblProteinIDs, KEGGIds, reactIDs, reactPathwayValues, refSeqIDs, refSeqNucs)
#         VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
#conn = None
#try:
#    # read the connection parameters
#    params = config()
#    # connect to the PostgreSQL server
#    conn = psycopg2.connect(**params)
#    cur = conn.cursor()
#    # create table
#    for command in commands:
#        cur.execute(command)
current = defaultdict(list)
priorLine = ""
with open(fname) as f:
    for line in f:
        line = line.rstrip()
        if line.startswith('//'):
            #end of term
            add_object(current)
            current = defaultdict(list)
            count += 1
            if count%50000 == 0:
                #break                   # test 50,000 records
                print "*",
                if count%1000000 == 0:
                    print (" count: "+str(count)),
                    print ("  time: "+str(time.time()-start))
            priorLine = ""
            continue 
            
        if len(line) < 5:
            continue        #ignore blank lines
            
        key = line[:2]
        val = line[5:]

        if key == "ID":
            values = val.split(' ')
            val = values[0]
        elif key == 'AC':
            values = val.split(';')
#            print values
            for ac in values:
                if len(ac) > 0:
                    current[key].append(ac.strip())
            key = ''
        elif key == 'GN':
            if val.endswith(';'):
                if len(priorLine) > 0:
                    val = priorLine + ' ' + val
                priorLine = ''
                values = val.split(';')
                for value in values:
                    if value.startswith('Name='):
                        val1 = value[5:]   # skip over 'Name='
                        vals = val1.split(' ')
                        current[key].append(vals[0])
                    if value.startswith('ORFNames='):
                        val1 = value[9:]   # skip over 'ORFNames='
                        vals2 = val1.split(',')
                        for val2 in vals2:
                            vals3 = val2.strip().split(' ')
                            current[key+'ORF'].append(vals3[0])
                    if value.startswith('Synonyms='):
                        val1 = value[9:]   # skip over 'Synonyms='
                        vals2 = val1.split(',')
                        for val2 in vals2:
                            vals3 = val2.strip().split(' ')
                            current[key+'Syn'].append(vals3[0])
                    if value.startswith('OrderedLocusNames='):
                        val1 = value[18:]   # skip over 'OrderedLocusNames='
                        vals2 = val1.split(',')
                        for val2 in vals2:
                            vals3 = val2.split(' ')
                            current[key+'OLN'].append(vals3[0])
                key =  ''
            else:
                if len(priorLine) > 0:
                    priorLine += ' ' + val
                else:
                    priorLine = val
                key =  ''
        elif key == 'DE':
            values = val.split('=')
            if len(values) > 1:  # note, there are DE's with "Flags:" that will fall through
                if values[0] == 'RecName: Full':
                    val = values[1]
                    key = 'DERF'
                elif values[0] == '         Short':
                    val = values[1]
                    key = 'DERS'
                elif values[0] == 'AltName: Full':
                    val = values[1]
                    key = 'DEAF'
                elif values[0] == 'AltName: Short': # didn't see an example of this. Might not be correct form.
                    val = values[1]
                    key = 'DEAS'
                if val.endswith(';'):
                    val = val[:-1]
            else:
                key =  ''
        elif key == 'OX':
            values = val.split('=')
            if len(values) > 1:
                if values[0] == 'NCBI_TaxID':
                    val = values[1]
                    key = 'OXID'
                    if val.endswith(';'):
                        val = val[:-1]
                else:
                    key = ''
        elif key == 'DR':
            values = val.split(';')
            if len(values) > 1:
                if (values[0] == 'GeneID' or values[0] == 'IntAct' or values[0] == 'KEGG' 
                                or values[0] == 'STRING' or values[0] == 'UCSC'):
                    key = key+values[0]
                    val = values[1]
                elif values[0] == 'EMBL':
                    key = key+values[0]
                    if len(values) > 2:
                        for v in values[1:]:
                            if v.strip() != "-" and v.strip() !='Genomic_RNA.':
                                current[key+'ProtSeqID'].append(v.strip()) # protein sequence id
                                val = v
                elif values[0] == 'Ensembl':
                    key = key+values[0]
                    if len(values) > 2:
                        current[key+'ProteinID'].append(values[2].strip()) # protein sequence id
                    if len(values) > 3:
                        current[key+'GeneID'].append(values[3].strip()) # gene id
                    if len(values) > 4:
                        molecule = values[3].strip()
                        if molecule.endswith(']'):
                            molecule = molecule[:-1]
                        if molecule.startswith('['):
                            molecule = molecule[1:]
                        current[key+'MolID'].append(molecule) # molecule
                    val = values[1]
                elif values[0] == 'Reactome':
                    key = key+values[0]
                    if len(values) > 2:
                        current[key+'PN'].append(values[2].strip()) # pathway name
                    val = values[1]
                elif values[0] == 'RefSeq':
                    key = key+values[0]
                    if len(values) > 2:
                        current[key+'NSID'].append(values[2].strip()) # nucleotide sequence id
                    val = values[1]
                else:
                    key = ''
        else:
            key = ''
        if key != '':
            current[key].append(val.strip().replace(',', '').replace('"', ''))

if current:
    add_object(current)
    count += 1

#    # close communication with the PostgreSQL database server
#    cur.close()
#    # commit the changes
#    conn.commit()
#except (Exception, psycopg2.DatabaseError) as error:
#    print(error)
#finally:
#    if conn is not None:
#        conn.close()
#
print (" count: "+str(count)),
print ("  time: "+str(time.time()-start))
allNamesFile.close()                                      
