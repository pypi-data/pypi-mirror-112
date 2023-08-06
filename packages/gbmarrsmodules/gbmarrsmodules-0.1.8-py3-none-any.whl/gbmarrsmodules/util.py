import re;
import os;

import jprops;
import rdflib;

from .miriamRegex import *;

# Match empty string, unprintable characters, space, and '>'
_invalidUri = re.compile (r'(^$|[\x00-\x20>])')

"""
Check if an URI is safe.
Raise an exception if it contains invalid chars or is otherwise unsafe
"""
def validateUri(uri):
	if _invalidUri.match(uri):
		raise Exception("Invalid URI: <" + uri + ">")
	if len(uri) > 1900:
		raise Exception("URI is too long: <" + uri + ">")

"""
Make a uri safe.
Simply checks for illegal characters and raise an exception if found.
"""
def safeUri(unsfUri):
	mo = re.search("([^\x20-\x7f]|>)", unsfUri)
	if mo:
		raise Exception("Input param contains unsafe characters: " + mo.group(0))
	return unsfUri # now safe.

"""
Make a Literal safe by addition of necessary escape characters.
"""
def safeLiteral(unsfLiteral):
	mo = unsfLiteral;
	mo = mo.replace('\\', '\\\\')
	mo = mo.replace('"', '\\"')
	mo = mo.replace('\n', '\\n')
	mo = mo.replace('\r', '\\r')
	return mo # now safe.

"""
Replace the prefix of a URI.
"""
def swapNsPrefix(uri):
	result = uri
	for k, v in _prefixmap.items():
		if uri.startswith(v):
			result = k + ':' + uri[len(v):]
			break
	return result

def localPart(value):
	"""
	return the local part of a uri, i.e. the part after the last '/', '#' or ':'
	"""

	pos = max (value.rfind('/'), value.rfind('#'), value.rfind(':'))
	if (pos >= 0): return value[pos+1:]
	else: return value

def getDataRoot(source, dataBuild):
    #base = os.environ['HOME']
    base = "/var/lib/gb/marrs/"
    if (dataBuild and (dataBuild.lower() == "next")):
        prop = "next"

    elif (dataBuild and (dataBuild.lower() == "current")):
        prop = "current"

    else:
        prop = dataBuild

    return os.path.join (base, prop, source)

def validateShapes(uri, uriType, shapes):
    """This function will compare the proposed predicate to the list defined in the shapes.ttl file and will return an error if it is not defined. """

    if uriType not in ("predicate", "class"):
        raise Exception ("The type provided is not in the allowed list, please choose from 'predicate' and 'class'.")

    uriUri = rdflib.namespace.Namespace("http://generalbioinformatics.com/ontologies/provenance/")
    g = rdflib.Graph()
    g.parse(shapes, format="ttl")

    myUri = rdflib.URIRef(uri)
    propDef = rdflib.URIRef("http://generalbioinformatics.com/ontologies/provenance/propDef")
    if not (None, None, myUri) in g:
        raise Exception ("This "+uriType+" URI was not defined in the shapes.ttl file: "+uri)
    for s, p, o in g.triples(( None, propDef, myUri)):
        if uriType == "predicate":
            if not (s, rdflib.namespace.RDF.type, uriUri.Property) in g:
                raise Exception ("This Predicate is not defined as a Predicate/Property in the shapes.ttl file: "+uri)
        if uriType == "class":
            if not (s, rdflib.namespace.RDF.type, uriUri.Class) in g:
                raise Exception ("This Class is not defined as a Class in the shapes.ttl file: "+uri)

def validateMiriamId(ns, id):
    """This will check an identifiers.org ID against the registers regex pattern and return an error if the regex fails, or the regex pattern is not yet defined. """

    pattern = re.compile(r"http:\/\/identifiers.org\/(.*?)\/$")
    if re.match(pattern, ns):
        idType = re.match(pattern,ns).group(1)
    else:
        raise Exception ("This namespace did not match the expected Identifiers.org structure: "+ns)

    if not idType in miriamRegex.miriamPattern.keys():
        raise Exception ("The id type '"+idType+"' has not been defined in the miriamRegex module yet.")

    if not re.match(r""+miriamRegex.miriamPattern[idType]+"", id):
        raise Exception (id+" didn't match the Miriam pattern of "+miriamRegex.miriamPattern[idType]) 
