#!/usr/bin/env python
import zipfile
import sys,os,random

from zlib import crc32
from index import Index,FileIndex
from gpx_parse import GpxParser

total_caches = 0

if( len( sys.argv ) >= 2 ):
	gpxindex = Index()
	for file in sys.argv[1:]:
		print "Checking:",file
		z = zipfile.ZipFile(file, "r")

		#Build up a reference-index
		for filename in z.namelist():
			if( filename.startswith("data/") and filename.endswith(".gpx") ):
				p = GpxParser()
				text = z.read(filename)
				file_index = FileIndex()
				file_index.cachelist = p.ParseText(text)
				info = z.getinfo(filename)
				file_index.crc = crc32(text)
				if( file_index.crc < 0 ):
					#crc32, depending on py version will either return
					#signed 32 bit or unsigned 32 bit, so we adjust if needed
					file_index.crc = long(file_index.crc)
					file_index.crc += 2**32

				if( file_index.crc != info.CRC ):
					print "Error:CRC failure in ",filename
					print "\tGPX crc:",str(file_index.crc)
					print "\tZIP crc:",str(info.CRC)
				file_index.name = filename[5:]
				gpxindex.filelist.append( file_index )
			elif( filename.startswith("index/") ):
				pass
			else:
				print "warning:unknown file in archive:",filename

		#parse the built-in index
		indexname = "index/com/garmin/geocaches/v0/index.xml"
		try:
			info = z.getinfo(indexname)
		except KeyError:
			print 'ERROR: Did not find %s in ggz file' % indexname
		else:
			print '%s is %d bytes' % (info.filename, info.file_size)
			#todo, hook index reader in, verify indexes match

else:
	print "Please run:%s [input.ggz..]" % sys.argv[0]

