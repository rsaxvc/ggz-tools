#!/usr/bin/python
from index import *
from xml.sax.saxutils import escape
import codecs
import os
import tempfile


class XmlWriter:
	"Simple XML serializer"
	def __init__( self, fs ):
		self._indent = 0
		self._fs = fs

	def indent(self):
		for x in range(self._indent):
			self._fs.write( " " )

	def OpenTag( self, tag ):
		self.indent()
		self._indent = self._indent + 1
		self._fs.write( "<%s>\n"%tag )

	def CloseTag( self, tag ):
		self._indent = self._indent - 1
		self.indent()
		self._fs.write( "</%s>\n"%tag )

	def OpenTagCloseTag( self, tag, text ):
		self.indent()
		self._fs.write( "<%s>"%tag )
		self._fs.write( text )
		self._fs.write( "</%s>\n"%tag )

	def entry( self, geocache ):
		self.OpenTag( "geocache" )
		self.OpenTagCloseTag( "name",        "%s"%geocache.name )
		self.OpenTagCloseTag( "code",        "%s"%geocache.code )
		self.OpenTagCloseTag( "awesomeness", "%f"%geocache.awesomeness )
		self.OpenTagCloseTag( "difficulty",  "%f"%geocache.difficulty )
		self.OpenTagCloseTag( "size",        "%f"%geocache.size )
		self.OpenTagCloseTag( "terrain",     "%f"%geocache.terrain )
		self.OpenTagCloseTag( "file_pos",    "%d"%geocache.file_pos )
		self.OpenTagCloseTag( "file_len",    "%d"%geocache.file_len )
		self.OpenTagCloseTag( "lat",         "%f"%geocache.lat )
		self.OpenTagCloseTag( "lon",         "%f"%geocache.lon )
		self.OpenTagCloseTag( "type",        "%s"%geocache.type )
		self.CloseTag( "geocache" )

def index_to_xml( index ):
	( temphndl, tempname ) = tempfile.mkstemp(".csv")
	os.close( temphndl )
	fs = codecs.open( tempname, "w", "utf-8" )
	x = XmlWriter(fs)
	x.OpenTag( "geocache_index" )
	for g in index.cachelist:
		x.entry( g )
	x.CloseTag( "geocache_index" )
	fs.close()
	return tempname
