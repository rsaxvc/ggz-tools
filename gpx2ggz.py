#!/usr/bin/env python
import zipfile
import sys,os,random
import time

from index import Index
from gpx_parse import GpxParser
from index_to_xml import index_to_xml
from index_to_csv import index_to_csv

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
        index = Index()
        index.cachelist = p.ParseFile(file)
        print "\tFound %i caches" % ( len(index.cachelist) )
        parse_time = time.time() - parse_time

        print "\tZipping"
        zip_time = time.time()
        z.write(file,"data/" + basefile )
        zip_time = time.time() - zip_time

        print "\tCreating CSV Index"
        index_csv_time = time.time()
        tempname = index_to_csv( index )
        noext, ext = os.path.splitext( basefile )
        z.write( tempname, "index/com/garmin/geocaches/v0/" + noext + ".csv" )
        index_csv_time = time.time() - index_csv_time
        os.system("rm -f %s"%tempname)

        index_xml_time = time.time()
        print "\tCreating XML Index"
        tempname = index_to_xml( index )
        noext, ext = os.path.splitext( basefile )
        z.write( tempname, "index/com/garmin/geocaches/v0/" + noext + ".xml" )
        index_xml_time = time.time() - index_xml_time
        os.system("rm -f %s"%tempname)


        print "Spent %fs parsing XML, %fs zipping, %fs creating CSV index, %fs creating XML index"%(
            parse_time,zip_time,index_csv_time,index_xml_time)

else:
    print "Please run:%s [input.gpx]... output.zip" % sys.argv[0]

