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
        DROP TABLE IF EXISTS malacards_vertices;
        """,
        """
        CREATE TABLE malacards_vertices (
        malacard_id SERIAL PRIMARY KEY,
        disease_name integer,
        disease_slug TEXT,
        displayed_gene_name VARCHAR(255),
        gene_symbol VARCHAR(255),
        is_elite BYTEA,
        is_cancer_census BYTEA,
        gene_disorder_score FLOAT8,
        score_implication TEXT,
        pubmed_ids TEXT
        )
        """)
    sql = """INSERT INTO malacards_vertices(disease_name, disease_slug, displayed_gene_name, gene_symbol, is_elite, is_cancer_census, gene_disorder_score, score_implication, pubmed_ids)
             VALUES(%s,%s, %s, %s, %s, %s,%s, %s);"""
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
        with open('/mnt/knowledgeGraphData/malaCards/MalaCards_genes_implication_v460.txt','rb') as csvFile:
            reader = csv.reader(csvFile)
            next(reader)
            for row in reader:
                cur.execute(sql,(row[0].strip(), row[1].strip(), row[2].strip(), row[3].strip(), row[4].strip(), row[5].strip(), row[6].strip(), row[7].strip(), row[8].strip(),))
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
