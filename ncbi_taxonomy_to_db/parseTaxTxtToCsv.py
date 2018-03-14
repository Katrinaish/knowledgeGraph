from collections import defaultdict
import sys

'''
from Larry Roberts:
pase dmp file to csv
2   |   prokaryotes |   prokaryotes <Bacteria>  |   in-part |
'''

dmpFile = open(sys.argv[1])
#dmpName = 'C:\\Users\\xli\\Documents\\chongle\\tax\\names.dmp'
#dmpFile = open(dmpName)

taxNamesDmpOut = open('taxNamesDmp_2_25.csv' , 'w')
taxNamesDmpOut.write(
typeNames = []
typeNames.append('acronym')
typeNames.append('anamorph')
typeNames.append('authority')
typeNames.append('blast name')
typeNames.append('common name')
typeNames.append('equivalent name')
typeNames.append('genbank acronym')
typeNames.append('genbank anamorph')
typeNames.append('genbank common name')
typeNames.append('genbank synonym')
typeNames.append('includes')
typeNames.append('in-part')
typeNames.append('scientific name')
typeNames.append('synonym')
typeNames.append('teleomorph')

taxNamesDmpOut.write('name')
for type in typeNames:
    taxNamesDmpOut.write(','+type)
taxNamesDmpOut.write('\n')

typeArray = []
for type in typeNames:
    typeArray.append([])

priorName = "1"

count = 0
for f in dmpFile.readlines():
    splitLine = f.split("|")
    name = splitLine[0].strip()
    name1 = splitLine[1].strip()
    name2 = splitLine[2].strip()
    type = splitLine[3].strip()
    if priorName != name:
        taxNamesDmpOut.write('"'+priorName)
        index = 0
        for typeName in typeNames:
            taxNamesDmpOut.write('","'+str(typeArray[index]))
            index += 1
        taxNamesDmpOut.write('"\n')
        typeArray = []
        for type in typeNames:
            typeArray.append([])
        count += 1
        priorName = name
        
    found = False
    index = 0
    for typeName in typeNames:
        if typeName == type:
            found = True
            typeArray[index].append(name1)
            if name1 != name2:
                typeArray[index].append(name2)
        index += 1
    if not found:
        print "type not found: "+type
        
taxNamesDmpOut.write('"'+priorName)
index = 0
for typeName in typeNames:
    taxNamesDmpOut.write('","'+str(typeArray[index]))
    index += 1
taxNamesDmpOut.write('"\n')
count += 1

print count

taxNamesDmpOut.close()
dmpFile.close()

