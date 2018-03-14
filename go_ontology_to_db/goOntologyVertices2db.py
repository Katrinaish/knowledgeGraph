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
        DROP TABLE IF EXISTS go_vertices;
        """,
        """
        CREATE TABLE go_vertices (
            go_vertices_id SERIAL PRIMARY KEY,
            go_id VARCHAR(255) NOT NULL,
            go_alter_id TEXT,
            definition TEXT, 
            comment TEXT,
            subset TEXT,
            synonyms TEXT,
            xref TEXT,
            relationships TEXT,
            intersections TEXT,
            disJoint_from TEXT,
            replaced_by TEXT,
            consider TEXT,      
            created_by TEXT,
            creationDate TEXT
        )
        """)

    sql = """INSERT INTO go_vertices(go_id,go_alter_id,definition,comment,subset,synonyms,xref,relationships,intersections,disJoint_from,replaced_by,consider,created_by,creationDate)
             VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s,%s,%s,%s);"""
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
        with open('/home/kpe/gitLabClones/knowledgeGraph/GoOntology to sql/goVertices.csv','rb') as csvFile:
            reader = csv.reader(csvFile)
            next(reader)
            for row in reader:
                cur.execute(sql,(row[0],row[1],row[2],row[3], row[4], row[5],row[6],row[7], row[8],row[9],row[10],row[11], row[12], row[13]))
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
