#!/usr/bin/python
import sys
sys.path.insert(0, "/home/kpe/scripts/db_setup")
import psycopg2
from config import config
import csv


"""
Proteome ID Organism    Organism ID Protein count

"""
def create_tables():
    """ create tables in the PostgreSQL database"""
    commands = (
        """
        DROP TABLE IF EXISTS ref_proteome_vertices;
        """,
        """
        CREATE TABLE ref_proteome_vertices (
            ref_id SERIAL PRIMARY KEY,
            proteome_ID VARCHAR(255) NOT NULL,
            organism_name TEXT,
            organism_id INTEGER,
            protein_count INTEGER
        )
        """)
    sql = """INSERT INTO ref_proteome_vertices(proteome_ID, organism_name, organism_id, protein_count)
             VALUES(%s,%s,%s,%s);"""
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
        with open('/home/kpe/data/uniProtReference/proteomeIds_to_organismID/proteomes-all.tab','rb') as tabFile:
            tabFile.next()
            for tabLine in tabFile:
                row = tabLine.split("\t")
                cur.execute(sql,(row[0].strip() ,row[1].strip(), row[2].strip(), row[3].strip())) 
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
