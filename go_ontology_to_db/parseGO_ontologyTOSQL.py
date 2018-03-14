"""
From http://stackoverflow.com/q/32989776/4014959
"""
import sys
#sys.path.insert(0, "/home/kpe/data/goTerms/obo")
from collections import defaultdict

fname = sys.argv[1]

goVertices = open("goVertices.csv", "w")
goEdges = open("goEdges.csv" , "w")
goVertices.write("id" + "," + "alterID" + "," + "def" + "," + "coment" + "," + "subset" + "," + "synonyms" + "," + "xref" + "," + "relationships" + "," + "intersections" + ", " + "disJoint_from" + "," + "replaced_by" + "," + "consider" + "," + "created_by" + "," + "creationDate" + "\n")

goEdges.write("id" + "," + "goPartner" + "," + "relationship_type" + "," + "relationshipText" + "\n")
#first create  vertex table of all attributes of the go ID
#then create edges table of all the relationships of goID and the subsequenet gene_ids in relationshp




term_head = "[Term]"
goID = ""
goAlterID = ""
isA = ""
name = ""
goDef = ""
goComment = ""
goSubset = ""
goRelationships = ""
goIntersection_of = ""
goDisJointFrom = ""
goReplacedBy =""
goConsider = ""
goCreatedby = ""
goCreationDate ="" 
goSynonyms = ""
goXrefs = ""
def add_object(d):
    if "is_obsolete" in d:
        return

    global goID
    global goAlterID
    global isA
    global name
    global goDef
    global goComment
    global goSubset
    global goRelationships
    global goIntersection_of
    global goDisJointFrom
    global goReplacedBy
    global goConsider
    global goCreatedby
    global goCreationDate 
    global goSynonyms
    global goXrefs

    #Gather desired data into a single list,
    # and store it in the main all_objects dict
    goID = str(d["id"][0]).strip()
    #    print goID
    isA = d["is_a"]
    goAlterID = d["alt_id"]
    name = d["name"]
    goDef = d["definiton"]
    goSubset = d["subset"]
    goComment = d["comment"]
    goSubset = d["subset"]
    goRelationships = d["relationship"]
    goIntersection_of = d["intersection_of"]
    goDisJointFrom = d["disjoint_from"]
    goReplacedBy = d["replaced_by"]
    goConsider = d["consider"]
    goCreatedby = d["created_by"]
    goCreationDate = d["creation_date"]
    goSynonyms = d["synonym"]
    goXrefs = d["xref"]

current = defaultdict(list)
with open(fname) as f:
    #Skip header data
    for line in f:
        if line.rstrip() == term_head:
            break

    for line in f:
        goID = ""
        goAlterID = ""
        isA = ""
        name = ""
        goDef = ""
        goComment = ""
        goSubset = ""
        goRelationships = ""
        goIntersection_of = ""
        goDisJointFrom = ""
        goReplacedBy =""
        goConsider = ""
        goCreatedby = ""
        goCreationDate ="" 
        goSynonyms = ""
        goXrefs = ""
        line = line.rstrip()
        if not line:
            #ignore blank lines
            continue
        if line == term_head:
            #end of term
            add_object(current)
#            print "first"
#            print goID
            current = defaultdict(list)

            goVertices.write(goID.replace(",", "") + "," + "|".join(goAlterID) + "," + "|".join(goDef) + "," + "|".join(goComment) + "," +  "|".join(goSubset) + "," + "|".join(goSynonyms) + "," + "|".join(goXrefs) + "," + "|".join(goRelationships) + "," + "|".join(goIntersection_of) +"," + "|".join(goDisJointFrom) + "," + "|".join(goReplacedBy) + "," + "|".join(goConsider) + "," + "|".join(goCreatedby) + "," + "|".join(goCreationDate) +  "\n") 
            for aLen in range(0, len(isA)):
                isASplit = isA[aLen].split("!")
                goEdges.write(goID.replace("," , "") + "," + isASplit[0].strip().replace(",", "") + "," + "subset" + "," + isASplit[1].replace(",", "")+  "\n")

            for relLen in range(0, len(goRelationships)):
                relSplit = goRelationships[relLen].split(" ")
                goEdges.write(goID.replace("," , "") + "," + relSplit[1].strip().replace(",", "") + "," + relSplit[0].replace(",", "") + "," + relSplit[3].replace(",", "") + "\n")
        else:
            #accumulate object data into current
            key, _, val = line.partition(": ")
            current[key].append(val.strip().replace(",", ""))
#            print key, val

if current:
    add_object(current)    

goVertices.write(goID.replace(",", "") + "," + "|".join(goAlterID) + "," + "|".join(goDef) + "," + "|".join(goComment) + "," +  "|".join(goSubset) + "," + "|".join(goSynonyms) + "," + "|".join(goXrefs) + "," + "|".join(goRelationships) + "," + "|".join(goIntersection_of) +"," + "|".join(goDisJointFrom) + "," + "|".join(goReplacedBy) + "," + "|".join(goConsider) + "," + "|".join(goCreatedby) + "," + "|".join(goCreationDate) +  "\n") 
for aLen in range(0, len(isA)):
    isASplit = isA[aLen].split("!")
    goEdges.write(goID.replace("," , "") + "," + isASplit[0].strip().replace(",", "") + "," + "subset" + "," + isASplit[1].replace(",", "")+  "\n")

for relLen in range(0, len(goRelationships)):
    relSplit = goRelationships[relLen].split(" ")
    goEdges.write(goID.replace("," , "") + "," + relSplit[1].strip().replace(",", "") + "," + relSplit[0].replace(",", "") + "," + relSplit[3].replace(",", "") + "\n")


goVertices.close()
goEdges.close()

