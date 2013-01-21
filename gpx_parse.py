from xml.parsers import expat
import sys

class Geocache:
	def __init__(self):
		self._name=""
		self._code=""
		self._awesomeness = 3
		self._difficulty  = 3
		self._size        = 3
		self._terrain     = 3
		self._file_pos    = 0
		self._file_len    = 0
		self._lat         = 0.0
		self._lon         = 0.0
		self._type        = ""

class GchParser:
	"Parses wpt/cache structures"
	def __init__(self):
		self._gch_list=[]
		self._gch=Geocache()
		self._close_tag_handlers={
			"name":self.handle_name,
			"code":self.handle_code,
			"wpt":self.handle_wpt
			}

	def handle_name(self,text,ebi):
		self._name=text

	def handle_code(self,text,ebi):
		self._code=code

	def handle_wpt(self,text,ebi):
		self._gch_list.append( self._gch )
		self._gch.__init__()

	def start(self, tag, attrs, cbi):
		print "GCH:Start", repr(tag), attrs, cbi

	def end(self, tag, textbuffer, ebi):
		try:
			self._close_tag_handlers[tag]( textbuffer, ebi )
		except KeyError:
			pass
		print "GCH:End", repr(tag), textbuffer, ebi

class NulParser:
	"Parses unused structures"
	def start(self, tag, attrs, cbi ):
		print "NULL:Start"
		pass

	def end(self, tag, textbuffer, ebi):
		print "NULL:End"
		pass

class GpxParser:
	def __init__(self):
		self._mode = "nul"
		self._nul_parser = NulParser()
		self._gch_parser = GchParser()
		self._depth = 0
		self._textbuffer = ""
		self._parser = expat.ParserCreate()
		self._parser.StartElementHandler = self.start
		self._parser.EndElementHandler = self.end
		self._parser.CharacterDataHandler = self.data

	def feed(self, data ):
		self._parser.Parse(data,0)

	def close(self):
		self._parser.Parse("", 1) # end of data
		del self._parser # get rid of circular references

	def start(self, tag, attrs):
		if( tag == "wpt" ):
			self._mode = "wpt"

		self._textbuffer=""
		self._depth = self._depth + 1
		if( self._mode == "wpt" ):
			self._gch_parser.start( tag, attrs, self._parser.CurrentByteIndex )
		else:
			self._nul_parser.start( tag, attrs, self._parser.CurrentByteIndex )
		print "START", repr(tag), attrs, self._depth, self._parser.CurrentByteIndex

	def data(self, data):
		self._textbuffer += repr(data)

	def end(self, tag):
		print "END", repr(tag), self._textbuffer, self._depth
		#To calculate the end pos, we need the CBI, which points to the start of the tag that caused
		#the current event, and we need to add '</' , the taglen, and '>' to find the end-byte-index
		end_pos = self._parser.CurrentByteIndex + 2 + len( tag ) + 1

		if( self._mode == "wpt" ):
			self._gch_parser.end( tag, self._textbuffer, end_pos )
		else:
			self._nul_parser.end( tag, self._textbuffer, end_pos )
		
		if( tag == "wpt" or tag == "rte" or tag == "trk" ):
			self._mode = "nul"
		self._depth = self._depth - 1


if( len( sys.argv ) == 2 ):
	p=GpxParser()
	f = open( sys.argv[-1] )
	p.feed( f.read() )
	f.close()
	p.close();
else:
    print "Please run:%s [input.gpx]" % sys.argv[0]





