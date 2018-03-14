#!/usr/bin/python
import psycopg2
from config import config
import csv

"""
"""
def create_tables():
    """ create tables in the PostgreSQL database"""
    commands = (
        """
        DROP TABLE IF EXISTS ref_proteome_edges;
        """,
        """
        CREATE TABLE ref_proteome_edges (
                name_id INTEGER NOT NULL,
                proteome_id VARCHAR(255) NOT NULL,
                FOREIGN KEY (name_id)
                    REFERENCES names_vertices (name_id)
                    ON UPDATE CASCADE ON DELETE CASCADE
        )
        """)
    sql = """INSERT INTO tax_lineage (name_id,proteome_id)
             VALUES(%s,%s);"""
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
# order of csv file uniprotID,inter1,inter2,id,label,orgDiffer,experiment
        with open('/home/kpe/taxonomyLineage.txt','rb') as csvFile:
            reader = csv.reader(csvFile)
            next(reader)
            priorID = ""
            name_id = -1
            for row in reader:
                orgDiff = row[5]
                if orgDiff != 'TRUE':
                    orgDiff = 'FALSE'
                try:
                    experiments = int(row[6])
                except ValueError:
                    experiments = 0
                if priorID != row[0]:
                    priorID = row[0]
                    cur.execute(query,(priorID,))
                    data = cur.fetchone()
                    if data is not None:
                        name_id = data[0]
                    else:
                        name_id = -1
                if name_id != -1:
                    cur.execute(sql,(name_id,row[1],row[2],row[3],row[4],orgDiff,experiments))
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
