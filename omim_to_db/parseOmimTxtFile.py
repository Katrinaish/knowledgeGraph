"""
parse OMIM File to csv 
source: https://omim.org/static/omim/data/mim2gene.txt

"""


omimFile = open("/mnt/knowledgeGraphData/omim/mim2gene.txt" , "r")
omimFileOut = open("/mnt/knowledgeGraphData/omim/omimParsed.csv", "w")
omimFileOut.write("MIM_number" + "," + "MIM_entry_type" + "," + "Entre_gene_id" + "," + "HGNC_symbol" + "," + "ensembl_gene_id" + "\n")




"""
header of file: 

MIM Number	MIM Entry Type (see FAQ 1.3 at https://omim.org/help/faq)	Entrez Gene ID (NCBI)	Approved Gene Symbol (HGNC)	Ensembl Gene ID (Ensembl)
"""
for f in omimFile.readlines()[6:]:
    MIM_number = ""
    MIM_entry_type = ""
    Entre_gene_id = ""
    HGNC_symbol = ""
    ensembl_gene_id = ""
    fSplit = f.split("\t")
    MIM_number = fSplit[0].strip().replace(",", "")
    MIM_entry_type = fSplit[1].strip().replace(",", "")
    Entre_gene_id = fSplit[2].strip().replace(",", "")
    HGNC_symbol = fSplit[3].strip().replace(",", "") 
    ensembl_gene_id = fSplit[4].strip().replace(",", "")
    omimFileOut.write(MIM_number + "," + MIM_entry_type + "," + Entre_gene_id + "," + HGNC_symbol + "," + ensembl_gene_id + "\n")


    
omimFileOut.close()
omimFile.close()


