#!/usr/bin/python
import psycopg2
from config import config
import os
from os import walk
from os.path import splitext
from os.path import join

def create_tables():
    """ create tables in the PostgreSQL database"""
    commands = (
        """
        DROP TABLE IF EXISTS fasta;
        """,
        """
        CREATE TABLE fasta (
            proteomes VARCHAR(255),
            gene VARCHAR(255)
        )
        """)
    sql = """INSERT INTO fasta(proteomes,gene) VALUES(%s,%s);"""
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
        dir = os.path.expanduser('~')+'/uniprot'
        fileList = list()
        for root, dirs, files in walk(dir):
            for f in files:
                if splitext(f)[1].lower() == ".fasta":
                    fileList.append(f)

        for file in fileList:
            fileName = file.split('.')
            up = fileName[0]
            print up
            with open(dir+'/'+file) as f:
                lines = f.readlines()
                for line in lines:
                    if line.startswith('>tr'):
                        fields = line.split('|')
                        gene = fields[0]
                        cur.execute(sql,(up,fields[1]))

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

