# import public modules
import os

def defineCsiDirectories(dirType, version):
    """This function will return the directory path to the required directory and create it if it does not already exist.
       Requires one of the following as dirType: "download", "rdf", "sql", "work", "production-tags". 
       Also requires the cpsd version""" 

    if not dirType in ["cpsd", "downloads", "rdf", "sql", "work", "production-tags"]:
        raise Exception("The directory type "+str(dirType)+" is not one of the required options: \"downloads\", \"rdf\", \"sql\", \"work\",  \"production-tags\"")
    if dirType == "production-tags":
        directoryPath = "/var/lib/gb/marrs/asynchronous-updates/production-tags/rdf/"
    elif dirType == "cpsd":
        directoryPath = "/var/lib/gb/cpsd/"+version+"/"
    else:
        directoryPath = "/var/lib/gb/marrs/asynchronous-updates/CPSD-"+version+"/"+dirType+"/"

    if not os.path.exists(directoryPath):
        os.makedirs(directoryPath)

    return directoryPath
# end def


def defineOrthologDirectories(dirType, version):
    """This function will return the directory path to the required directory and create it if it does not already exist.
       Requires one of the following as dirType: "download", "rdf", "sql", "work". 
       Also requires the cpsd version""" 

    if not dirType in ["downloads", "rdf", "sql", "work"]:
        raise Exception("The directory type "+str(dirType)+" is not one of the required options: \"downloads\", \"rdf\", \"sql\", \"work\"")
    directoryPath = "/var/lib/gb/marrs/asynchronous-updates/CPSD-"+version+"/orthologs/"+dirType+"/"

    if not os.path.exists(directoryPath):
        os.makedirs(directoryPath)

    return directoryPath
# end def

def prepCpsdIdForUri(fastaHeaderId):
    """This function will take the long fasta header identifier and standardise it ready for use in a URI that can be recognised across graphs.
       After its return, use in combination with the appropriate cpsd identifier namespace."""
    compiledPattern = re.compile(r"[^a-zA-Z0-9]")
    uriName = re.sub(compiledPattern, "-", fastaHeaderId)
    return uriName
# end def

