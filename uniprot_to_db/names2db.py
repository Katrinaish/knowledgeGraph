#!/usr/bin/python
import psycopg2
from config import config
import csv

"""
uniprotID,primaryAccessID,alterAccessIDList,geneName,protFullName,protShortName,protFullAltNameList,protShortAltNameList,ncbiTAXID,ensemblIDs,ensemblMolID,ensemblGeneIDs,ensemblProteinIDs,ncbiGeneID,intActID,KEGGIds,reactIDs,reactPathwayValues,refSeqIDs,refSeqNucs,stringID,ucscID,emblID,emblProtSeqID
"""
def create_tables():
    """ create tables in the PostgreSQL database"""
    commands = (
        """
        DROP TABLE IF EXISTS names_vertices;
        """,
        """
        CREATE TABLE names_vertices (
            name_id SERIAL PRIMARY KEY,
            primary_accessID VARCHAR(255) NOT NULL,
            uniprot_ID VARCHAR(255) NOT NULL,
            gene_name TEXT NOT NULL,
            protFullName TEXT,
            protShortName VARCHAR(255),
            ncbiTAXID VARCHAR(255),
            ncbiGeneID VARCHAR(255),
            intActID VARCHAR(255),
            stringID VARCHAR(255), 
            ucscID VARCHAR(255), 
            emblID TEXT, 
            emblProtSeqID TEXT,
            protFullAltNameList TEXT,
            protShortAltNameList TEXT,
            alterAccessIDList TEXT,
            ensemblMolID TEXT,
            ensemblIDs TEXT,
            ensemblGeneIDs TEXT,
            ensemblProteinIDs TEXT,
            KEGGIds TEXT,
            reactIDs TEXT,
            reactPathwayValues TEXT, 
            refSeqIDs TEXT, 
            refSeqNucs TEXT 
        )
        """)
    sql = """INSERT INTO names_vertices(primary_accessID, uniprot_ID, gene_name, protFullName, protShortName, ncbiTAXID, ncbiGeneID, intActID, stringID, ucscID, emblID, emblProtSeqID, protFullAltNameList, protShortAltNameList, alterAccessIDList, ensemblMolID, ensemblIDs, ensemblGeneIDs, ensemblProteinIDs, KEGGIds, reactIDs, reactPathwayValues, refSeqIDs, refSeqNucs)
             VALUES(%s,%s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s,%s, %s, %s, %s, %s, %s);"""
    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table
        for command in commands:
            cur.execute(command)
        # insert records
        with open('/home/kpe/allNamesUpdated.csv','rb') as csvFile:
            reader = csv.reader(csvFile)
            next(reader)
            for row in reader:
                cur.execute(sql,(row[1].strip() ,row[0].strip(), row[3].strip(), row[4].strip(), row[5].strip(), row[8].strip(), row[13].strip(), row[14].strip(), row[20].strip(), row[21].strip(),  row[22].strip(), row[23].strip(), row[6].strip(), row[7].strip(), row[2].strip(), row[10].strip(), row[9].strip(), row[11].strip(), row[12].strip(), row[15].strip(), row[16].strip(), row[17].strip(), row[18].strip(), row[19].strip()))
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
 
 
if __name__ == '__main__':
    create_tables()
