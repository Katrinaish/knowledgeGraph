#!/usr/bin/python
import sys
sys.path.insert(0, "/home/kpe/scripts/db_setup")
import psycopg2
from config import config
import csv

#name,acronym,anamorph,authority,blast name,common name,equivalent name,genbank acronym,genbank anamorph,genbank common name,genbank synonym,includes,in-part,scientific name,synonym,teleomorph
def create_tables():
    """ create tables in the PostgreSQL database"""
    commands = (
        """
        DROP TABLE IF EXISTS tax_vertices;
        """,
        """
        CREATE TABLE tax_vertices (
            tax_vertices_id SERIAL PRIMARY KEY,
            tax_id INTEGER NOT NULL,    
            scientificName TEXT,
            synonym TEXT,
            acronym TEXT,
            anamorph TEXT,
            authority TEXT,
            blastName TEXT,
            commonName TEXT,
            equivalentName TEXT,
            genbankAcronym TEXT,
            genbankAnamorph TEXT,
            genbankCommonName TEXT,
            genbankSynonym TEXT,
            includes TEXT,
            inPart TEXT,
            teleomorph TEXT
            
 
        )
        """)

    sql = """INSERT INTO tax_vertices(tax_id, scientificName, synonym, acronym,anamorph,authority,blastName,commonName,equivalentName,genbankAcronym,genbankAnamorph,genbankCommonName,genbankSynonym,includes,inPart,teleomorph)
             VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
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
        with open('/home/kpe/data/taxonomy/taxNamesDmp_2_25.csv','rb') as csvFile:
            reader = csv.reader(csvFile)
            next(reader)
#            priorID = ""
#            name_id = -1
            for row in reader:
                cur.execute(sql,(row[0].strip(), row[13].strip().replace("'",""), row[14].strip().replace("'",""), row[1].strip().replace("'",""), row[2].strip().replace("'",""), row[3].strip().replace("'",""), row[4].strip().replace("'",""),row[5].strip().replace("'",""),row[6].strip().replace("'",""),row[7].strip().replace("'",""),row[8].strip().replace("'",""),row[9].strip().replace("'",""),row[10].strip().replace("'",""),row[11].strip().replace("'",""),row[12].strip().replace("'",""), row[15].strip().replace("'","")))

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
