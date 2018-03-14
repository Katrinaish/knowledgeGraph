#!/usr/bin/python
import sys
sys.path.insert(0, "/home/kpe/scripts/db_setup")
import psycopg2
from config import config
import csv

"""
tax_id,parent_tax_id,rank,embl_code,division_id,inherited_div_flag,genetic_code_id,inherited_GC_flag,mitochondrial_genetic_code_id,inherited_MGC_flag,,hidden_subtree_root_flag,comments,plastid_genetic_code_id,inherited_PGC_flag,specified_species,hydrogenosome_genetic_code_id,inherited_HGC_flag
"""
def create_tables():
    """ create tables in the PostgreSQL database"""
    commands = (
        """
        DROP TABLE IF EXISTS uniprot_tax_edges;
        """,
        """
        CREATE TABLE uniprot_tax_edges (
            tax_edges_id SERIAL PRIMARY KEY,
            tax_id INTEGER NOT NULL,
            parent_tax_id INTEGER NOT NULL,
            rank VARCHAR(255),
            embl_code VARCHAR(255),
            division_id VARCHAR(255),
            inherited_div_flag BYTEA,
            genetic_code_id VARCHAR(255),
            inherited_GC_flag BYTEA,
            mitochondrial_genetic_code_id VARCHAR(255),
            inherited_MGC_flag BYTEA,
            hidden_subtree_root_flag BYTEA,
            comments TEXT,
            plastid_genetic_code_id VARCHAR(255),
            inherited_PGC_flag BYTEA,
            specified_species TEXT,
            hydrogenosome_genetic_code_id VARCHAR(255),
            inherited_HGC_flag BYTEA
 
        )
        """)
    sql = """INSERT INTO uniprot_tax_edges(tax_id, parent_tax_id,rank,embl_code,division_id,inherited_div_flag,genetic_code_id,inherited_GC_flag,mitochondrial_genetic_code_id,inherited_MGC_flag,hidden_subtree_root_flag,comments,plastid_genetic_code_id,inherited_PGC_flag,specified_species,hydrogenosome_genetic_code_id,inherited_HGC_flag)
             VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
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
        with open('/home/kpe/data/taxonomy/taxNodesDmp.csv','rb') as csvFile:
            reader = csv.reader(csvFile)
            next(reader)
            for row in reader:
                cur.execute(sql,(row[0].strip(), row[1].strip(),str(row[2]).strip(),row[3].strip(),row[4].strip(),row[5].strip(),row[6].strip(), row[7].strip(),row[8].strip(),row[9].strip(),row[10].strip(),row[11].strip(),row[12].strip(),row[13].strip(),row[14].strip(),row[15].strip(), row[16].strip()))
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
