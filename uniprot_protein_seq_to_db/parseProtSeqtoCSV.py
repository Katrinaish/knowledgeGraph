
#
#        """"
#        print protein sequences 
#        """	
#        protSeqs = element.findall(uri + 'sequence')
#        for protSeq in protSeqs:
#            protSeqTxt = ""
#            protSeqL = ""
#            protSeqM = ""
#            protCkSum = ""
#            protMod = ""
#            protVer = ""
#            if 'length' in protSeq.attrib:
#                protSeqL = protSeq.get('length')
#            if 'mass' in protSeq.attrib:
#                protSeqM = protSeq.get('length')
#            if 'checksum' in protSeq.attrib:
#                protCkSum = protSeq.get('checksum')
#            if 'modified' in protSeq.attrib:
#                protMod = protSeq.get('modified')	
#            if 'version' in protSeq.attrib:
#                protVer = protSeq.get('version')
#            protSeqTxt	= protSeq.text
#            if protSeqTxt is not None:
#                if protSeqL is not None:
#                    if protSeqM is not None: 
#                        if protCkSum is not None:
#                            if protMod is not None:
#                                if protVer is not None:
#                                    protSeqFile.write(str(uniprotName).rstrip() + "," + str(protSeqTxt).rstrip().replace(",", "") + "," + str(protSeqL).rstrip().replace(",", "") + "," + str(protSeqM).rstrip().replace(",", "") + "," + protCkSum.rstrip().replace(",", "") + "," + str(protMod).rstrip().replace(",", "") + "," + str(protVer).rstrip().replace(",", "") + "\n")
#                                else:
#                                    protSeqFile.write(str(uniprotName).rstrip() + "," + str(protSeqTxt).rstrip().replace(",", "") + "," + str(protSeqL).rstrip().replace(",", "") + "," + str(protSeqM).rstrip().replace(",", "") + "," + protCkSum.rstrip().replace(",", "") + "," + str(protMod).rstrip().replace(",", "") +  "\n")
#                            else:
#                                protSeqFile.write(str(uniprotName).rstrip() + "," + str(protSeqTxt).rstrip().replace(",", "") + "," + str(protSeqL).rstrip().replace(",", "") + "," + str(protSeqM).rstrip().replace(",", "") + "," + protCkSum.rstrip().replace(",", "") + "\n")
#                        else:
#                            protSeqFile.write(str(uniprotName).rstrip() + "," + str(protSeqTxt).rstrip().replace(",", "") + "," + str(protSeqL).rstrip().replace(",", "") + "," + str(protSeqM).rstrip().replace(",", "") + "\n")
#                    else:
#                        protSeqFile.write(str(uniprotName).rstrip() + "," + str(protSeqTxt).rstrip().replace(",", "") + "," + str(protSeqL).rstrip().replace(",", "")  + "\n")
#                else:
#                    protSeqFile.write(str(uniprotName).rstrip() + "," + str(protSeqTxt).rstrip().replace(",", "") + "\n")
#                
#            print protSeqL, protSeqM, protCkSum, protMod, protVer 
#            print protSeqTxt
