# This module writes triples to an nt file via a tmp file. It applies QC test to triples following guidelines found : TODO
import sys
import gzip
import re
import codecs
import os
import tempfile
from subprocess import check_call

from .util import validateUri

miriamPattern = re.compile(r"http://identifiers.org/")

class NtWriter:

	def __enter__ (self):
		return self
	
	def __exit__ (self, exType, exVal, traceback):
		self.f.close()
		self.f = None
		if exType is None:
			print ("Renaming to: " + self.fname) 
			os.rename(self.tmpname, self.fname)
		else:
			print ("Deleting temp file")
			os.unlink (self.tmpname)


	def __init__ (self, fname = None, shapes = None, validate=True, escapeUnicode=True):
		r"""
		fname:
			if no filename is passed, the triples are written to standard output.
			if the passed filename ends with .gz, it is automatically compressed.
		
		escapeUnicode:
			Unicode characters in literals may be either escaped with a prefix (\u....) or written as UTF-8. Set to escaping by default.
		"""
		
		self.validate = validate
		self.escapeUnicode = escapeUnicode
		self.fname = fname
		self.shapes = shapes

		if not os.path.exists(shapes):
			raise Exception ("There was no shapes file for this dataset found in the RDF directory, please copy that shapes.ttl file there before runnning.")

		parentdir = os.path.split (os.path.abspath(fname))[0]

		if fname is None:
			fh = sys.stdout;
		else:			
			if fname.endswith (".gz"):
				# can't open temp file to gzip, see http://www.enricozini.org/2011/cazzeggio/python-gzip/
				self.tmpname = tempfile.mktemp(prefix = "ntwriter-", suffix = ".tmp", dir = parentdir)
				fh = gzip.open (self.tmpname, "w")
			else:
				# this is the proper, race-less way to atomically create and open a temporary file
				# Unfortunately it only works for non-gz files
				(handle, self.tmpname) = tempfile.mkstemp(dir = parentdir)
				fh = os.fdopen(handle, "w")
				#fh = open (fname, "w")
			
		print ("Using temp file: " + self.tmpname)

		if self.escapeUnicode: writer = codecs.getwriter("ascii")
		else: writer = codecs.getwriter("utf-8")
		
		self.f = writer(fh)

	def printStatement(self, sns, sid, pns, pid, ons, oid):
		suri = sns+sid
		puri = pns+pid
		ouri = ons+oid
		if self.validate:
			"""Foreach URI in the triple, check that it is not longer than max length, and doesn't match invalid URI pattern."""
			validateUri(suri)
			validateUri(puri)
			validateUri(ouri)

        # Make sure the predicates are all defined in the shapes.ttl
		validateShapes(puri, "predicate", shapes)
		if puri == "a" or puri == "http://www.w3.org/1999/02/22-rdf-syntax-ns#type" or puri == "rdf.type":
            # Make sure the classes are all defined in the shapes.ttl
			validateShapes(ouri, "class",  shapes)
        # end if

        # Do subject and object ids with miriam namespace match the Miriam regex for the id?
        # Plus any stronger regex we give it to aid data integration
		if re.search(miriamPattern, sns):
			validateMiriamId(sns, sid)
        # end if
		if re.search(miriamPattern, ons):
			validateMiriamId(ons, oid)
        # end if

        # Are there any namespace delimiters in the ID?
		if re.search(r"\/|\#", oid):
			oid_regex = re.search(r"(\/|\#)", oid).group(1)
			raise Exception (f"This Object ID contained the illegal character {oid_regex}. Please find alternatives to '#' or '/' within identifiers.")
		if re.search(r"\/|\#", sid):
			sid_regex = re.search(r"(\/|\#)", sid).group(1)
			raise Exception (f"This Subject ID contained the illegal character {sid_regex}. Please find alternatives to '#' or '/' within identifiers.")
        # end if

        # TODO create a ns summariser here

		self.f.write ("<%s> <%s> <%s> . \n" % (suri, puri, ouri))

	def printLiteral(self, sns, sid, pns, pid, o, otype):
		"""Here we require that the literal must have a type. This can be one of the following:
              - string
              - integer
              - decimal
              - double
              - boolean
              - date (Dates (yyyy-mm-dd) with or without timezone)
           For other possible types, look here: https://www.w3.org/TR/rdf11-concepts/#xsd-datatypes"""

		if otype not in ('string', 'integer', 'decimal', 'double', 'boolean', 'date'):
			raise Exception("The Object type must be one of: 'string', 'integer', 'decimal', 'double', 'boolean', 'date'.")

		xsd = "http://www.w3.org/2001/XMLSchema#"

		suri = sns+sid
		puri = pns+pid

		if self.validate:
			validateUri(suri)
			validateUri(puri)

		if puri == "a" or puri == "http://www.w3.org/1999/02/22-rdf-syntax-ns#type" or puri == "rdf:type":
			raise Exception("An object following the predicate 'type' should always be a URI, not a literal. Please convert "+o+" to a URI and use printStatement\n")
        # end if

		if re.search(miriamPattern, sns):
			validateMiriamId(sns, sid)
        # end if

		validateShapes(puri, "predicate", shapes)

		if o == "" or o == "null" or o == "NULL" or o == "Null":
			raise Exception("This literal object was an empty or 'null' string\n")

		if re.search(r"\/|\#", sid):
			sid_regex = re.search(r"(\/|\#)", sid).group(1)
			raise Exception (f"This Subject ID contained the illegal character {sid_regex}. Please find alternatives to '#' or '/' within identifiers.")
		# end if

		osafe = ""
		for i in o:
			if i == '\\':
				osafe += '\\\\'
			elif i == '"':
				osafe += '\\"'
			elif i == '\n':
				osafe += '\\n'
			elif i == '\r':
				osafe += '\\r'
			elif self.escapeUnicode and ord(i) > 127:
				osafe += "\\u%04X" % ord(i)
			else:
				osafe += i

		oFull = osafe+f"^^<{xsd+otype}>"
		self.f.write ("""<%s> <%s> "%s" . \n""" % (suri, puri, oFull))
	
	"""
	Close filehandle and move temp file to final filename
	"""
	def close(self):
		self.f.close ()
		self.f = None
		print ("Renaming to: " + self.fname)
		os.rename(self.tmpname, self.fname)
