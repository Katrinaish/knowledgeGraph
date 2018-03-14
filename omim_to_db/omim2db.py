#!/usr/bin/python
import sys
sys.path.insert(0, "/home/kpe/scripts/db_setup")
import psycopg2
from config import config
import csv

"""
"MIM_number" + "," + "MIM_entry_type" + "," + "Entre_gene_id" + "," + "HGNC_symbol" + "," + "ensembl_gene_id"
"""
def create_tables():
    """ create tables in the PostgreSQL database"""
    commands = (
        """
        DROP TABLE IF EXISTS omim_edges;
        """,
        """
        CREATE TABLE omim_edges (
            omim_id SERIAL PRIMARY KEY,
            mim_number INTEGER,
            mim_entry_type VARCHAR(255),
            ncbi_gene_id VARCHAR(255),
            hgnc_symbol VARCHAR(255),
            ensembl_gene_id VARCHAR(255)
        )
        """)
    sql = """INSERT INTO omim_edges(mim_number, mim_entry_type, ncbi_gene_id, hgnc_symbol, ensembl_gene_id)
             VALUES(%s,%s, %s, %s, %s);"""
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
        with open('/mnt/knowledgeGraphData/omim/omimParsed.csv','rb') as csvFile:
            reader = csv.reader(csvFile)
            next(reader)
            for row in reader:
                cur.execute(sql,(row[0].strip(), row[1].strip(), row[2].strip(), row[3].strip(), row[4].strip()))
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
