#!/usr/bin/python
import sqlite3,sys,os,random
import xml.dom.minidom
import zlib

id = 0

if( len( sys.argv ) >= 3 ):
    os.system("rm -f %s"%sys.argv[-1])
    conn = sqlite3.connect(sys.argv[-1])
    c = conn.cursor()

    # Create tables
    c.execute("CREATE TABLE geocaches                      ( id INTEGER PRIMARY KEY, gc_code VARCHAR(10), short_desc TEXT, long_desc BLOB, awesomeness REAL, difficulty REAL, size REAL, terrain REAL)")
    c.execute("CREATE VIRTUAL TABLE geocaches_r USING rtree( id INTEGER PRIMARY KEY, minLat REAL,maxLat REAL, minLon REAL, maxLon REAL)")
    c.execute("CREATE VIRTUAL TABLE geocache_t  USING fts4 ( id INTEGER PRIMARY KEY, name TEXT)")
    c.execute("CREATE TABLE geocache_logs                 ( id INTEGER PRIMARY KEY, gc_id INT, type TEXT, finder TEXT, text BLOB)")

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
            long_desc.encode("utf-8")
            zlib.compress( long_desc.encode("utf-8") )
            sqlite3.Binary( zlib.compress( long_desc.encode("utf-8") ) )
            c.execute("""INSERT INTO geocaches   VALUES ( ?,?,?,?,?,?,?,? )""", (id, gccode, short_desc, sqlite3.Binary( zlib.compress( long_desc.encode("utf-8" ) ) ),awesomeness,difficulty,size,terrain) )
            c.execute("""INSERT INTO geocaches_r VALUES ( ?,?,?,?,? )""", (id,lat,lat,lon,lon) )
            c.execute("""INSERT INTO geocache_t  VALUES ( ?,?)""",(id,name) )

            for log_sets in geocache.getElementsByTagName("groundspeak:logs"):
                for log in log_sets.getElementsByTagName("groundspeak:log"):
                    log_id = log.getAttribute("id")

                    log_type_tag = log.getElementsByTagName("groundspeak:type")
                    if len( log_type_tag ) == 1:
                        log_type = getText( log_type_tag[0].childNodes )
                    else:
                        log_type = ""

                    log_finder_tag = log.getElementsByTagName("groundspeak:finder")
                    if len( log_finder_tag ) == 1:
                        log_finder = getText( log_finder_tag[0].childNodes )
                    else:
                        log_finder = ""

                    log_text_tag = log.getElementsByTagName("groundspeak:text")
                    if len( log_text_tag ) == 1:
                        log_text = getText( log_text_tag[0].childNodes )
                    else:
                        log_text = ""
                    print log_id
                    c.execute("INSERT INTO geocache_logs VALUES(?,?,?,?,?)", ( log_id, id, log_type, log_finder, sqlite3.Binary( zlib.compress( log_text.encode("utf-8") ) ) ) )

        def handleGPX(gpx):
            global id
            geocaches = gpx.getElementsByTagName("wpt")
            for geocache in geocaches:
                handleGeocache( geocache, id )
                id = id + 1
        print "Packing:",file
        handleGPX(dom)

    # Save (commit) the changes
    conn.commit()
    c.execute("VACUUM;")
    c.close()
else:
    print "Please run:%s [input.gpx]... output.db" % sys.argv[0]
