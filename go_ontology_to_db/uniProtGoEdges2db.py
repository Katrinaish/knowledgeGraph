#!/usr/bin/python
import sys
sys.path.insert(0, "/home/kpe/scripts/db_setup")
import psycopg2
from config import config
import csv

"""


"""
def create_tables():
    """ create tables in the PostgreSQL database"""
    commands = (
        """
        DROP TABLE IF EXISTS uniprot_to_GO_edges;
        """,
        """
        CREATE TABLE uniprot_to_GO_edges (
            name_id INTEGER NOT NULL,
            accessionID VARCHAR(255) NOT NULL,
            goID VARCHAR(255) NOT NULL,
            goTerm VARCHAR(255), 
            goEvidence VARCHAR(255),
            goProj VARCHAR(255),
            FOREIGN KEY (name_id)
                    REFERENCES names_vertices (name_id)
                    ON UPDATE CASCADE ON DELETE CASCADE
 
        )
        """)
    sql = """INSERT INTO uniprot_to_GO_edges(name_id, accessionID, goID, goTerm, goEvidence, goProj)
             VALUES(%s,%s,%s,%s,%s,%s);"""
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
        with open('/home/kpe/goAnnotationsUpdated.txt','rb') as csvFile:
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
                    cur.execute(sql,(name_id, row[0], row[1], row[2], row[3]))
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
