#!/usr/bin/python
import zipfile
import sys,os,random
import time
import tempfile

from gpx_parse import *

def writeXmlIndexHeader( fd ):
	os.write( fd, "<xml>" )

def writeXmlIndexEntry( fd, geocache ):
	os.write( fd, "" );

def writeXmlIndexFooter( fd ):
	os.write( fd, "</xml>" )

def writeCsvIndexEntry( fd, geocache ):
	os.write( fd, "" );

if( len( sys.argv ) >= 3 ):
    os.system("rm -f %s"%sys.argv[-1])
    z = zipfile.ZipFile( sys.argv[-1], "w", zipfile.ZIP_DEFLATED )

    # Create tables
    for  file in sys.argv[ 1:-1]:
        basefile = os.path.basename(file)
        print "Processing %s"%(basefile)

        parse_time = time.time()
        print "\tParsing XML into cachelist"
        p = GpxParser()
        cachebuffer = p.ParseFile(file)
        print "\tFound %i caches" % ( len(cachebuffer) )
        parse_time = time.time() - parse_time

        print "\tZipping"
        zip_time = time.time()
        z.write(file,"data/" + basefile )
        zip_time = time.time() - zip_time

        print "\tCreating CSV Index"
        index_csv_time = time.time()
        ( temphndl, tempname ) = tempfile.mkstemp(".csv")
        os.write( temphndl, ("Hello") )
        os.close( temphndl )
        noext, ext = os.path.splitext( basefile )
        z.write( tempname, "index/com/garmin/geocaches/v0/" + noext + ".csv" )
        for g in cachebuffer:
            #yield (g['lat'],g['lat'],g['lon'],g['lon'] )
            pass
        index_csv_time = time.time() - index_csv_time

        index_zip_time = time.time()
        print "\tCreating XML Index"
        index_zip_time = index_zip_time - time.time()


        print "Spent %fs parsing XML, %fs zipping, %fs creating XML index, %fs creating CSV index"%(
            parse_time,zip_time,index_csv_time,index_zip_time)

else:
    print "Please run:%s [input.gpx]... output.zip" % sys.argv[0]
