#!/usr/bin/env python
import zipfile
import sys,os,random
import time

from zlib import crc32
from index import Index,FileIndex
from gpx_parse import GpxParser
from index_to_xml import index_to_xml

total_caches = 0

if( len( sys.argv ) >= 3 ):
	os.system("rm -f %s"%sys.argv[-1])
	z = zipfile.ZipFile( sys.argv[-1], "w", zipfile.ZIP_DEFLATED )

	# Create tables
	index = Index()
	for  file in sys.argv[ 1:-1]:
		file_index = FileIndex()
		zip_time = 0

		basefile = os.path.basename(file)
		print "Processing %s"%(basefile)

		parse_time = time.time()
		print "\tParsing XML into cachelist"
		p = GpxParser()
		f = open( file )
		text = f.read()
		f.close()
		file_index.cachelist = p.ParseText(text)
		file_index.crc = crc32(text)
		file_index.name = os.path.basename(file)
		print "\tFound %i caches" % ( len(file_index.cachelist) )
		total_caches = total_caches + len(file_index.cachelist)
		parse_time = time.time() - parse_time

		print "\tZipping"
		zip_time = zip_time - time.time()
		z.write(file,"data/" + basefile )
		zip_time = zip_time + time.time()

		index.filelist.append( file_index )

	print "\tCreating indexes for %i caches" % total_caches

	index_xml_time = time.time()
	print "\tCreating XML Index"
	tempname = index_to_xml( index )
	zip_time = zip_time - time.time()
	z.write( tempname, "index/com/garmin/geocaches/v0/index.xml" )
	zip_time = zip_time + time.time()
	index_xml_time = time.time() - index_xml_time
	os.system("rm -f %s"%tempname)


	print "Spent %fs parsing XML, %fs zipping, %fs creating XML index"%(
		parse_time,zip_time,index_xml_time)

else:
	print "Please run:%s [input.gpx]... output.zip" % sys.argv[0]

