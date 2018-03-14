#!/usr/bin/python
import sys
sys.path.insert(0, "/home/kpe/scripts/db_setup")
import psycopg2
from config import config
import os
import gzip
from os import walk
from os.path import splitext
from os.path import join

def create_tables():
#    """ create tables in the PostgreSQL database"""
#    commands = (
#        """
#        """)
    sql = """INSERT INTO ref_proteome_edges(proteomes,gene) VALUES(%s,%s);"""
    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table
#        for command in commands:
#            cur.execute(command)
            
        # insert records
        dir = '/mnt/knowledgeGraphData/uniprotRefProteome/Viruses'
        fileList = list()
        for root, dirs, files in walk(dir):
            for f in files:
#                print f
#                print splitext(f)[0].lower()
#                print len(splitext(f))
#                need to get it to split so only have extension, right now getting everything in file name
#                print str(splitext(f)[0].lower()).split("_")[2]
#                print splitext(f)[0].lower()
#                print str(splitext(f)[1].lower()).split(".")[0]
#                if str(splitext(f)[1].lower()).split(".")[1] == "fasta":
                fileList.append(f)
#                print len(fileList)
#                print fileList
    
        for file in fileList:
#            print file
            fileName = file.split('_')
            up = fileName[0]
#            print up
            with gzip.open(dir+'/'+file) as f:
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


