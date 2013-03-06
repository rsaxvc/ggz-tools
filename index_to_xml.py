#!/usr/bin/python
from index import *
from xml.sax.saxutils import escape
import codecs
import os
import tempfile

def crc32_to_hex( crc ):
	ulong = long()
	if( crc < 0 ):
		ulong = crc+2**31
	else:
		ulong = crc
	return hex(ulong)[2:].upper()


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
		self._fs.write( escape( text ) )
		self._fs.write( "</%s>\n"%tag )

	def entry( self, geocache ):
		self.OpenTag( "gch" )
		self.OpenTagCloseTag( "code",        "%s"%geocache.code )
		self.OpenTagCloseTag( "name",        "%s"%geocache.name )
		self.OpenTagCloseTag( "type",        "%s"%geocache.type )
		self.OpenTagCloseTag( "lat",         "%f"%geocache.lat )
		self.OpenTagCloseTag( "lon",         "%f"%geocache.lon )
		self.OpenTagCloseTag( "file_pos",    "%d"%geocache.file_pos )
		self.OpenTagCloseTag( "file_len",    "%d"%geocache.file_len )
		self.OpenTag( "ratings" )
		self.OpenTagCloseTag( "awesomeness", "%f"%geocache.awesomeness )
		self.OpenTagCloseTag( "difficulty",  "%f"%geocache.difficulty )
		self.OpenTagCloseTag( "size",        "%f"%geocache.size )
		self.OpenTagCloseTag( "terrain",     "%f"%geocache.terrain )
		self.CloseTag( "ratings" )
		self.CloseTag( "gch" )

def index_to_xml( index ):
	( temphndl, tempname ) = tempfile.mkstemp(".xml")
	os.close( temphndl )
	fs = codecs.open( tempname, "w", "utf-8" )
	x = XmlWriter(fs)
	x.OpenTag( "ggz" )
	for f in index.filelist:
		x.OpenTag( "file" )
		x.OpenTagCloseTag( "name", f.name )
		x.OpenTagCloseTag( "crc", crc32_to_hex( f.crc ) )
		for g in f.cachelist:
			x.entry( g )
		x.CloseTag( "file" )
	x.CloseTag( "ggz" )
	fs.close()
	return tempname
