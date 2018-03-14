#!/usr/bin/python
import psycopg2
from config import config
import csv

def create_tables():
    """ create tables in the PostgreSQL database"""
    commands = (
        """
        DROP TABLE IF EXISTS tax_lineage;
        """,
        """
        CREATE TABLE tax_lineage (
                name_id INTEGER,
                taxon VARCHAR(255) NOT NULL,
                FOREIGN KEY (name_id)
                    REFERENCES names (name_id)
                    ON UPDATE CASCADE ON DELETE CASCADE
        )
        """)
    sql = """INSERT INTO tax_lineage (name_id,taxon)
             VALUES((SELECT name_id FROM names WHERE uniprot_id=%s),%s);"""
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
        count = 0
        with open('/home/kpe/taxonomyLineage.txt','rb') as csvFile:
            reader = csv.reader(csvFile)
            next(reader)
            for row in reader:
                count +=1
                if count %100000 == 0:
                    print "at 100000"
                if row[0] is not None and row[1] is not None:
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
