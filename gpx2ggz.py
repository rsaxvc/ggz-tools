#!/usr/bin/python
import zipfile
import sys,os,random
import xml.dom.minidom
import zlib
import time
import tempfile

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
        cachebuffer = []

        time0 = time.time()
        print "\tParsing XML"
        dom = xml.dom.minidom.parse(file)
        time1 = time.time()

        def getText(nodelist):
            rc = []
            for node in nodelist:
                if node.nodeType == node.TEXT_NODE:
                    rc.append(node.data)
            return ''.join(rc)

        def handleGeocache( geocache ):
            retn={}
            retn['lat']=float(geocache.getAttribute("lat"))
            retn['lon']=float(geocache.getAttribute("lon"))

            name_tag = geocache.getElementsByTagName("groundspeak:name")
            if len( name_tag ) == 1:
                retn['name'] = getText( name_tag[0].childNodes )
            else:
                retn['name'] = ""

            code_tag = geocache.getElementsByTagName("name")
            if len( code_tag ) == 1:
                retn['code'] = getText( code_tag[0].childNodes )
            else:
                retn['code'] = ""

            retn['type']=random.randint(0, 9)
            return retn
#            return (lat,lon,gccode,name,short_desc,long_desc,awesomeness,difficulty,size,terrain,log_list)

        geocaches = dom.getElementsByTagName("wpt")
        def handleGPX(gpx):
            geocaches = gpx.getElementsByTagName("wpt")
            for geocache in geocaches:
                cachebuffer.append( handleGeocache( geocache ) )

        print "\tParsing DOM"

        handleGPX(dom)

        print "\tZipping"
        z.write(file,"data/" + basefile )
        time2 = time.time()

        print "\tCreating CSV Index"
        time3 = time.time()
        ( temphndl, tempname ) = tempfile.mkstemp(".csv")
        os.write( temphndl, ("Hello") )
        os.close( temphndl )
        noext, ext = os.path.splitext( basefile )
        z.write( tempname, "index/com/garmin/geocaches/v0/" + noext + ".csv" )
        for g in cachebuffer:
            #yield (g['lat'],g['lat'],g['lon'],g['lon'] )
			print ""

        print "\tCreating XML Index"


        print "Spent %f seconds parsing XML, %f seconds zipping, %f seconds indexing"%((time1-time0),(time2-time1),(time3-time2))

else:
    print "Please run:%s [input.gpx]... output.zip" % sys.argv[0]
