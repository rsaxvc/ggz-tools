#!/usr/bin/python
import sqlite3,sys,os,random
import xml.dom.minidom

id = 0

if( len( sys.argv ) >= 3 ):
    os.system("rm -f %s"%sys.argv[-1])
    conn = sqlite3.connect(sys.argv[-1])
    c = conn.cursor()

    # Create tables
    c.execute('''CREATE TABLE geocaches( id, gc_code VARCHAR(10), name TEXT, short_desc TEXT, long_desc TEXT, awesomeness REAL, difficulty REAL, size REAL, terrain REAL)''')
    c.execute('''CREATE VIRTUAL TABLE geocaches_r USING rtree(id,minLat,maxLat,minLon,maxLon)''')

    for  file in sys.argv[ 1:-1]:
        print "Parsing:",file
        dom = xml.dom.minidom.parse(file)

        def getText(nodelist):
            rc = []
            for node in nodelist:
                if node.nodeType == node.TEXT_NODE:
                    rc.append(node.data)
            return ''.join(rc)

        def handleGeocache( geocache, id ):
            lat = geocache.getAttribute("lat")
            lon = geocache.getAttribute("lon")
    
            gccode_tag = geocache.getElementsByTagName("name");
            if( len( gccode_tag ) == 1 ):
                gccode = getText( gccode_tag[0].childNodes )
            else:
                gccode = ""

            short_desc_tag = geocache.getElementsByTagName("desc");
            if( len( gccode_tag ) == 1 ):
                short_desc = getText( short_desc_tag[0].childNodes )
            else:
                short_desc = ""

            gs_tag = geocache.getElementsByTagName("groundspeak:cache")
            if( len( gs_tag ) == 1 ):
                name_tag = gs_tag[0].getElementsByTagName("groundspeak:name")
                if( len( name_tag ) == 1 ):
                    name = getText( name_tag[0].childNodes )
                else:
                    name = ""

                long_desc_tag = gs_tag[0].getElementsByTagName("groundspeak:long_description")
                if( len( long_desc_tag ) == 1 ):
                    long_desc = getText( long_desc_tag[0].childNodes )
                else:
                    long_desc = ""
            else:
                name = ""
                long_desc = ""

            awesomeness = random.uniform(0,5)
            difficulty  = random.uniform(0,5)
            size        = random.uniform(0,5)
            terrain     = random.uniform(0,5)

            ## Insert a row of data
            c.execute("""INSERT INTO geocaches   VALUES ( ?,?,?,?,?,?,?,?,? )""", (id, gccode, name,short_desc,long_desc,awesomeness,difficulty,size,terrain) )
            c.execute("""INSERT INTO geocaches_r VALUES ( ?,?,?,?,? )""", (id,lat,lat,lon,lon) )

        

        def handleGPX(gpx):
            global id
            geocaches = gpx.getElementsByTagName("wpt")
            for geocache in geocaches:
                handleGeocache( geocache, id )
                id = id + 1
        print "Packing:",file
        handleGPX(dom)

    c.execute("VACUUM;")
    # Save (commit) the changes
    conn.commit()

    # We can also close the cursor if we are done with it
    c.close()
else:
    print "Please run:%s [input.gpx]... output.db" % sys.argv[0]
