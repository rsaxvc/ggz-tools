#!/usr/bin/python
from index import *

import os
import tempfile

def index_to_csv( index ):
	( temphndl, tempname ) = tempfile.mkstemp(".csv")
	os.write( temphndl, ("Hello - this indexer is unimplemented") )
	for g in index.cachelist:
		#yield (g['lat'],g['lat'],g['lon'],g['lon'] )
		pass
	os.close( temphndl )
	return tempname
