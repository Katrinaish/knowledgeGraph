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
        DROP TABLE IF EXISTS protein_vertices;
        """,
        """
        CREATE TABLE protein_vertices (
            name_id INTEGER NOT NULL,
            accession_id VARCHAR(255) NOT NULL,
            length INTEGER,
            mass INTEGER,
            checksum VARCHAR(255),
            modified VARCHAR(255),
            version INTEGER,
            sequence TEXT, 
            FOREIGN KEY (name_id)
                    REFERENCES names_vertices (name_id)
                    ON UPDATE CASCADE ON DELETE CASCADE
 
        )
        """)
    sql = """INSERT INTO protein_vertices(name_id, accession_id, length, mass,checksum,modified,version,sequence)
             VALUES(%s,%s,%s,%s,%s,%s, %s,%s);"""
    query = """SELECT name_id FROM names_vertices WHERE primary_accessid=%s;"""
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
        with open('/home/kpe/protSeqUpdated2_21.txt','rb') as csvFile:
            reader = csv.reader(csvFile)
            next(reader)
            priorID = ""
            name_id = -1
            for row in reader:
                if priorID != row[0]:
                        priorID = row[0]
                        cur.execute(query,(priorID,))
                        data = cur.fetchone()
                        if data is not None:
                            name_id = data[0]
                        else:
                            name_id = -1
                if name_id != -1:
                    cur.execute(sql,(name_id, row[0], row[1], row[2], row[3], row[4], row[5], row[6]))
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
