import sys
import gzip

""""
unzipping mass files from:
https://www.peterbe.com/plog/fastest-way-to-unzip-a-zip-file-in-python
"""




def unzip_member_f3(zip_filepath, filename, dest):
    with open(zip_filepath, 'rb') as f:
        zf = gzip.GzipFile(f)
        zf.open(filename, dest)
    fn = os.path.join(dest, filename)
    return _count_file(fn)



def f3(fn, dest):
    with open(fn, 'rb') as f:
        zf = gzip.GzipFile(f)
        futures = []
        with concurrent.futures.ProcessPoolExecutor() as executor:
            for member in zf.infolist():
                futures.append(
                    executor.submit(
                        unzip_member_f3,
                        fn,
                        member.filename,
                        dest,
                    )
                )
            total = 0
            for future in concurrent.futures.as_completed(futures):
                total += future.result()
    return total


fileList = open("/mnt/knowledgeGraphData/uniprotRefProteome/Eukaryota/listOfFastagz.txt", "r")

for f in fileList.readlines():
    f3(f.strip(), "/mnt/knowledgeGraphData/uniprotRefProteome/Eukaryota/unzippedFasta")


fileList.close()
