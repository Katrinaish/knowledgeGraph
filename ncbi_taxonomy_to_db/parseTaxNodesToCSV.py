
from collections import defaultdict
import sys

'''
from Larry Roberts:
pase dmp file to csv
1	|	1	|	no rank	|		|	8	|	0	|	1	|	0	|	0	|	0	|	0	|	0	|		|		|		|	0	|	0	|	0	|
2	|	131567	|	superkingdom	|		|	0	|	0	|	11	|	0	|	0	|	0	|	0	|	0	|		|		|		|	0	|	0	|	1	|
6	|	335928	|	genus	|		|	0	|	1	|	11	|	1	|	0	|	1	|	0	|	0	|		|		|		|	0	|	0	|	1	|
7	|	6	|	species	|	AC	|	0	|	1	|	11	|	1	|	0	|	1	|	1	|	0	|		|		|		|	1	|	0	|	1	|
9	|	32199	|	species	|	BA	|	0	|	1	|	11	|	1	|	0	|	1	|	1	|	0	|		|		|		|	1	|	0	|	1	|
10	|	1706371	|	genus	|		|	0	|	1	|	11	|	1	|	0	|	1	|	0	|	0	|		|		|		|	0	|	0	|	1	|
11	|	1707	|	species	|	CG	|	0	|	1	|	11	|	1	|	0	|	1	|	1	|	0	|		|		|		|	1	|	0	|	1	|
13	|	203488	|	genus	|		|	0	|	1	|	11	|	1	|	0	|	1	|	0	|	0	|		|		|		|	0	|	0	|	1	|
14	|	13	|	species	|	DT	|	0	|	1	|	11	|	1	|	0	|	1	|	1	|	0	|		|		|		|	1	|	0	|	1	|
16	|	32011	|	genus	|		|	0	|	1	|	11	|	1	|	0	|	1	|	0	|	0	|		|		|		|	0	|	0	|	1	|
17	|	16	|	species	|	MM	|	0	|	1	|	11	|	1	|	0	|	1	|	1	|	0	|		|		|		|	1	|	0	|	1	|
18	|	213421	|	genus	|		|	0	|	1	|	11	|	1	|	0	|	1	|	0	|	0	|		|		|		|	0	|	0	|	1	|
19	|	18	|	species	|	PC	|	0	|	1	|	11	|	1	|	0	|	1	|	1	|	0	|		|		|		|	1	|	0	|	1	|
20	|	76892	|	genus	|		|	0	|	1	|	11	|	1	|	0	|	1	|	0	|	0	|		|		|		|	0	|	0	|	1	|
21	|	20	|	species	|	PI	|	0	|	1	|	11	|	1	|	0	|	1	|	1	|	0	|		|		|		|	1	|	0	|	1	|
22	|	267890	|	genus	|		|	0	|	1	|	11	|	1	|	0	|	1	|	0	|	0	|		|		|		|	0	|	0	|	1	|
'''



dmpFile = open(sys.argv[1])
#dmpName = 'C:\\Users\\xli\\Documents\\chongle\\tax\\names.dmp'
#dmpFile = open(dmpName)

taxNamesDmpOut = open('taxNodesDmp.csv' , 'w')
taxNamesDmpOut.write("tax_id" + "," + "parent_tax_id" + "," + "rank" + "," + "embl_code" + "," + "division_id" + "," + "inherited_div_flag" + "," + "genetic_code_id" + "," + "inherited_GC_flag" + "," + "mitochondrial_genetic_code_id" + "," + "inherited_MGC_flag" + "," + "," + "hidden_subtree_root_flag" + "," + "comments" + "," + "plastid_genetic_code_id" + "," + "inherited_PGC_flag" + "," + "specified_species" + "," + "hydrogenosome_genetic_code_id" + "," + "inherited_HGC_flag" + "\n") 
for f in dmpFile.readlines():
    tax_id = ""                 
    parent_tax_id = ""              
    rank = ""                     
    embl_code= ""                
    division_id = ""           
    inherited_div_flag = ""  
    genetic_code_id= ""              
    inherited_GC_flag= ""  
    mitochondrial_genetic_code_id= ""        
    inherited_MGC_flag = "" 
    GenBank_hidden_flag = "" 
    hidden_subtree_root_flag = "" 
    comments = ""               
    plastid_genetic_code_id = ""                 
    inherited_PGC_flag = "" 
    specified_species = ""          
    hydrogenosome_genetic_code_id = ""            
    inherited_HGC_flag = "" 

    fSplit = f.split("|")
    tax_id = fSplit[0].strip()                 
    parent_tax_id = fSplit[1].strip()
    rank = fSplit[2].strip()                    
    embl_code= fSplit[3].strip()               
    division_id = fSplit[4].strip()           
    inherited_div_flag = fSplit[5].strip() 
    genetic_code_id= fSplit[6].strip()              
    inherited_GC_flag= fSplit[7].strip() 
    mitochondrial_genetic_code_id= fSplit[8].strip()        
    inherited_MGC_flag = fSplit[9].strip() 
    GenBank_hidden_flag = fSplit[10].strip()
    hidden_subtree_root_flag = fSplit[11].strip()
    comments = fSplit[12].strip()               
    plastid_genetic_code_id = fSplit[13].strip()                 
    inherited_PGC_flag = fSplit[14].strip() 
    specified_species = fSplit[15].strip()          
    hydrogenosome_genetic_code_id = fSplit[16].strip()         
    inherited_HGC_flag = fSplit[17].strip()

    taxNamesDmpOut.write(tax_id + "," + parent_tax_id + "," + rank + "," + embl_code + "," + division_id + "," + inherited_div_flag + "," + genetic_code_id + "," + inherited_GC_flag + "," + mitochondrial_genetic_code_id + "," + inherited_MGC_flag + "," + "," + hidden_subtree_root_flag + "," + comments + "," + plastid_genetic_code_id + "," + inherited_PGC_flag + "," + specified_species + "," + hydrogenosome_genetic_code_id + "," + inherited_HGC_flag + "\n") 
taxNamesDmpOut.close()
dmpFile.close()

