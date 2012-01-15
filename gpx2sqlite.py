#!/usr/bin/python
import sqlite3
import sys,os,random
import xml.dom.minidom
import zlib
import time

id = 0
multiplier = 1 #Multiply every insert by this
filenum = 0

if( len( sys.argv ) >= 3 ):
    os.system("rm -f %s"%sys.argv[-1])
    conn = sqlite3.connect(sys.argv[-1])
    conn.isolation_level="EXCLUSIVE"
    c = conn.cursor()

    # Create tables
    c.execute("CREATE TABLE geocaches                                ( id INTEGER PRIMARY KEY, gc_code VARCHAR(10), short_desc TEXT, long_desc BLOB, awesomeness REAL, difficulty REAL, size REAL, terrain REAL)")
    c.execute("CREATE VIRTUAL TABLE geocaches_attributes  USING rtree( id INTEGER PRIMARY KEY, awesomeness REAL, awesomeness2 REAL, difficulty REAL, difficulty2 REAL, size REAL, size2 REAL, terrain REAL, terrain2 REAL)")
    c.execute("CREATE VIRTUAL TABLE geocaches_awesomeness USING rtree( id INTEGER PRIMARY KEY, awesomeness REAL, awesomeness2 REAL)")
    c.execute("CREATE VIRTUAL TABLE geocaches_difficulty  USING rtree( id INTEGER PRIMARY KEY, difficulty  REAL, difficulty2  REAL)")
    c.execute("CREATE VIRTUAL TABLE geocaches_size        USING rtree( id INTEGER PRIMARY KEY, size        REAL, size2        REAL)")
    c.execute("CREATE VIRTUAL TABLE geocaches_terrain     USING rtree( id INTEGER PRIMARY KEY, terrain     REAL, terrain2     REAL)")
    c.execute("CREATE VIRTUAL TABLE geocaches_location    USING rtree( id INTEGER PRIMARY KEY, lat REAL, lat2 REAL, lon REAL, lon2 REAL)")
    c.execute("CREATE VIRTUAL TABLE geocaches_name        USING fts4 ( id INTEGER PRIMARY KEY, name TEXT)")
    c.execute("CREATE TABLE geocache_logs                            ( id INTEGER PRIMARY KEY, gc_id INT, type TEXT, finder TEXT, text BLOB)")

    for  file in sys.argv[ 1:-1]:
        time0 = time.time()
        print "Parsing file%i : %s"%(filenum,file)
        dom = xml.dom.minidom.parse(file)
        time1 = time.time()

        def getText(nodelist):
            rc = []
            for node in nodelist:
                if node.nodeType == node.TEXT_NODE:
                    rc.append(node.data)
            return ''.join(rc)

        def insertGeocache(id,gccode,name,short_desc,long_desc,awesomeness,difficulty,size,terrain,lat,lon):
            for localid in range(id * multiplier, ( id + 1 ) * multiplier):
                if( multiplier != 1 ):
                    gccode = "OX%06d"%localid
                c.execute("""REPLACE INTO geocaches             VALUES (?,?,?,?,?,?,?,?)""", (localid, gccode, short_desc, sqlite3.Binary( zlib.compress( long_desc.encode("utf-8" ) ) ),awesomeness,difficulty,size,terrain) )
                c.execute("""REPLACE INTO geocaches_attributes  VALUES (?,?,?,?,?,?,?,?,?)""",(localid,awesomeness,awesomeness,difficulty,difficulty,size,size,terrain,terrain) )
                c.execute("""REPLACE INTO geocaches_awesomeness VALUES (?,?,?)""",(localid,awesomeness,awesomeness) )
                c.execute("""REPLACE INTO geocaches_difficulty  VALUES (?,?,?)""",(localid,difficulty, difficulty) )
                c.execute("""REPLACE INTO geocaches_size        VALUES (?,?,?)""",(localid,size,       size) )
                c.execute("""REPLACE INTO geocaches_terrain     VALUES (?,?,?)""",(localid,terrain,    terrain) )
                c.execute("""REPLACE INTO geocaches_location    VALUES (?,?,?,?,?)""", (localid,str(lat),str(lat),str(lon),str(lon) ) )
                c.execute("""REPLACE INTO geocaches_name        VALUES (?,?)""",(localid,name) )
                if( multiplier != 1 ):
                    lat += random.gauss(0,.00075)
                    lon += random.gauss(0,.00075)

        def insertLog( log_id, id, log_type, log_finder, log_text ):
            for localid in range(id * multiplier, ( id + 1 ) * multiplier):
                c.execute("REPLACE INTO geocache_logs VALUES(?,?,?,?,?)", ( log_id, localid, log_type, log_finder, sqlite3.Binary( zlib.compress( log_text.encode("utf-8") ) ) ) )

        def handleLog( log ):
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
            insertLog( log_id, id, log_type, log_finder, log_text )

        def handleGeocache( geocache ):
            global id
            lat = float(geocache.getAttribute("lat"))
            lon = float(geocache.getAttribute("lon"))
    
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
            insertGeocache(id,gccode,name,short_desc,long_desc,awesomeness,difficulty,size,terrain,lat,lon)

            for log_sets in geocache.getElementsByTagName("groundspeak:logs"):
                for log in log_sets.getElementsByTagName("groundspeak:log"):
                    handleLog( log )

        def handleGPX(gpx):
            global id
            geocaches = gpx.getElementsByTagName("wpt")
            for geocache in geocaches:
                handleGeocache( geocache )
                id = id + 1
        print "Packing %i : %s"%(filenum,file)
        handleGPX(dom)
        time2 = time.time()
        print "Spent %f seconds parsing, %f seconds packing"%((time1-time0),(time2-time1))

    # Save (commit) the changes
    c.execute("VACUUM;")
    c.close()
else:
    print "Please run:%s [input.gpx]... output.db" % sys.argv[0]
