#!/usr/bin/python
from geocache import *
from xml.parsers import expat
from copy import deepcopy

class GchParser:
	"Parses wpt/cache structures"
	def __init__(self):
		self._gch_list=[]
		self._gch=Geocache()
		self._close_tag_handlers={
			"name":self.handle_name,
			"code":self.handle_code,
			"wpt":self.handle_wpt_close,
			"wpt":self.handle_wpt_close,
			}

		self._open_tag_handlers={
			"wpt":self.handle_wpt_open,
			}

	def handle_awesomeness(self,text,ebi):
		self._gch.awesomeness = float( text )

	def handle_difficulty(self,text,ebi):
		self._gch.difficulty = float( text )

	def handle_size(self,text,ebi):
		self._gch.size = float( text )

	def handle_terrain(self,text,ebi):
		self._gch.terrain = float( text )

	def handle_name(self,text,ebi):
		self._gch.name=text

	def handle_code(self,text,ebi):
		self._gch.code=code

	def handle_wpt_close(self,text,ebi):
		self._gch.file_len = ebi - self._gch.file_pos
		self._gch_list.append( deepcopy( self._gch ) )
		self._gch.__init__()

	def handle_wpt_open(self,attrs,cbi):
		self._gch.lat = float(attrs["lat"])
		self._gch.lon = float(attrs["lon"])
		self._gch.file_pos = cbi

	def start(self, tag, attrs, cbi):
		try:
			self._open_tag_handlers[tag]( attrs, cbi )
		except KeyError:
			pass

	def end(self, tag, textbuffer, ebi):
		try:
			self._close_tag_handlers[tag]( textbuffer, ebi )
		except KeyError:
			pass

	def close(self):
		self._gch_list=[]
		self._gch.__init__()

class NulParser:
	"Parses unused structures"
	def start(self, tag, attrs, cbi ):
		pass

	def end(self, tag, textbuffer, ebi):
		pass

	def close(self):
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
		self._parser.buffer_text = 1

	def ParseFile(self, filename ):
		"Parse a file specified by filename"

		#open + parse + close file
		f = open( filename )
		self._parser.Parse(f.read(),0)
		f.close()

		#close down parser
		self._parser.Parse("", 1) # end of data

		#save results
		list = self._gch_parser._gch_list

		#reset child parsers
		del self._parser # get rid of circular references
		self._nul_parser.close()
		self._gch_parser.close()

		#return result set
		return list

	def start(self, tag, attrs):
		if( tag == "wpt" ):
			self._mode = "wpt"

		self._textbuffer=""
		self._depth = self._depth + 1
		if( self._mode == "wpt" ):
			self._gch_parser.start( tag, attrs, self._parser.CurrentByteIndex )
		else:
			self._nul_parser.start( tag, attrs, self._parser.CurrentByteIndex )

	def data(self, data):
		self._textbuffer += data

	def end(self, tag):
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




