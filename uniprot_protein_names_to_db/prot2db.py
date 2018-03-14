#!/usr/bin/python
import sys
sys.path.insert(0, "/home/kpe/scripts/db_setup")
import psycopg2
from config import config
import csv

def create_tables():
    """ create tables in the PostgreSQL database"""
    commands = (
        """
        DROP TABLE IF EXISTS names;
        """,
        """
        CREATE TABLE names (
            prot_id SERIAL PRIMARY KEY,
            uniprot_id VARCHAR(255) NOT NULL,
            gene_name VARCHAR(255)
        )
        """)
    sql = """INSERT INTO names(uniprot_id, gene_name)
             VALUES(%s,%s);"""
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
        #uniprotID,fullName,ShortName
        with open('/home/kpe/geneNames.txt','rb') as csvFile:
            reader = csv.reader(csvFile)
            for row in reader:
                cur.execute(sql,(row[0],row[1]))
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
