#!/usr/bin/python
from index import *
import os
import tempfile


def open( fd, tag ):
    os.write( fd, "<%s>"%tag )

def close( fd, tag ):
    os.write( fd, "</%s>"%tag )

def openCloseTag( fd, tag, text ):
	open( fd, tag )
	os.write( fd, text )
	close( fd, tag )

def entry( fd, geocache ):
	open( fd, "geocache" )
	openCloseTag( fd, "name",        "%s"%geocache.name )
	openCloseTag( fd, "code",        "%s"%geocache.code )
	openCloseTag( fd, "awesomeness", "%f"%geocache.awesomeness )
	openCloseTag( fd, "difficulty",  "%f"%geocache.difficulty )
	openCloseTag( fd, "size",        "%f"%geocache.size )
	openCloseTag( fd, "terrain",     "%f"%geocache.terrain )
	openCloseTag( fd, "file_pos",    "%d"%geocache.file_pos )
	openCloseTag( fd, "file_len",    "%d"%geocache.file_len )
	openCloseTag( fd, "lat",         "%f"%geocache.lat )
	openCloseTag( fd, "lon",         "%f"%geocache.lon )
	openCloseTag( fd, "type",        "%s"%geocache.type )
	close( fd, "geocache" )

def footer( fd ):
    os.write( fd, "</geocache_index>" )

def index_to_xml( index ):
	( temphndl, tempname ) = tempfile.mkstemp(".csv")
	open( temphndl, "geocache_index" )
	for g in index.cachelist:
		entry( temphndl, g )
	close( temphndl, "geocache_index" )
	os.close( temphndl )
	return tempname
