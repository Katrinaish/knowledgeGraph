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
        DROP TABLE IF EXISTS go_edges;
        """,
        """
        CREATE TABLE go_edges (
            go_edge_id SERIAL PRIMARY KEY,
            go_id VARCHAR(255) NOT NULL,
            go_partner VARCHAR(255) NOT NULL,
            relationship_type VARCHAR(255) NOT NULL,
            relationship_text TEXT
        )
        """)

    sql = """INSERT INTO go_edges(go_id,go_partner, relationship_type, relationship_text)
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
        with open('/home/kpe/gitLabClones/knowledgeGraph/GoOntology to sql/goEdges.csv','rb') as csvFile:
            reader = csv.reader(csvFile)
            next(reader)
            for row in reader:
                cur.execute(sql,(row[0],row[1],row[2],row[3]))
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
