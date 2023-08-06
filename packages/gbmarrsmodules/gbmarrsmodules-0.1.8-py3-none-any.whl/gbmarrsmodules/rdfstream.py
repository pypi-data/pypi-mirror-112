import sys
import gzip
import re
import codecs
import os
import tempfile
from subprocess import check_call
import locale

from .util import validateUri

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


	def __init__ (self, fname = None, validate=True, escapeUnicode=True):
		r"""
		fname:
			if no filename is passed, the triples are written to standard output.
			if the passed filename ends with .gz, it is automatically compressed.
		
		validate: 
			Option to disable validation for extra speed, enabled by default

		escapeUnicode:
			Unicode characters in literals may be either escaped with a prefix (\u....) or written as UTF-8. Set to escaping by default.
		"""
		
		self.validate = validate
		self.escapeUnicode = escapeUnicode
		self.fname = fname

		parentdir = os.path.split (os.path.abspath(fname))[0]

		if fname is None:
			fh = sys.stdout;
		else:			
			if fname.endswith (".gz"):
				# can't open temp file to gzip, see http://www.enricozini.org/2011/cazzeggio/python-gzip/
				self.tmpname = tempfile.mktemp(prefix = "ntwriter-", suffix = ".tmp", dir = parentdir)
				fh = gzip.open (self.tmpname, "wb")
			else:
				# this is the proper, race-less way to atomically create and open a temporary file
				# Unfortunately it only works for non-gz files
				(handle, self.tmpname) = tempfile.mkstemp(dir = parentdir)
				fh = os.fdopen(handle, "wb")
				#fh = open (fname, "w")
			
		print ("Using temp file: " + self.tmpname)

		if self.escapeUnicode: writer = codecs.getwriter("ascii")
		else: writer = codecs.getwriter("utf-8")
		self.f = writer(fh)

	def printStatement(self, s, p, o):
		if self.validate:
			validateUri(s)
			validateUri(p)
			validateUri(o)

		self.f.write ("<%s> <%s> <%s> . \n" % (s, p, o))

	def printLiteral(self, s, p, o):
		if self.validate:
			validateUri(s)
			validateUri(p)

		osafe = ""
		for i in o:
			if i == '\\':
				osafe += '\\'
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
				osaf = osafe
		self.f.write ("""<%s> <%s> "%s" . \n""" % (s, p, osaf))
	
	"""
	Close filehandle and move temp file to final filename
	"""
	def close(self):
		self.f.close ()
		self.f = None
		print ("Renaming to: " + self.fname)
		os.rename(self.tmpname, self.fname)
