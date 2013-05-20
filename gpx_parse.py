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
			"gpx/wpt/name":self._handle_name,
			"gpx/wpt/sym":self._handle_sym,

			"gpx/wpt/groundspeak:cache/groundspeak:container":self._handle_gs_container,
			"gpx/wpt/groundspeak:cache/groundspeak:difficulty":self._handle_gs_difficulty,
			"gpx/wpt/groundspeak:cache/groundspeak:name":self._handle_gs_name,
			"gpx/wpt/groundspeak:cache/groundspeak:terrain":self._handle_gs_terrain,
			"gpx/wpt/groundspeak:cache/groundspeak:type":self._handle_type,

			"gpx/wpt/ox:opencaching/ox:ratings/ox:awesomeness":self._handle_ox_awesomeness,
			"gpx/wpt/ox:opencaching/ox:ratings/ox:difficulty":self._handle_ox_difficulty,
			"gpx/wpt/ox:opencaching/ox:ratings/ox:size":self._handle_ox_size,
			"gpx/wpt/ox:opencaching/ox:ratings/ox:terrain":self._handle_ox_terrain,

			"gpx/wpt":self._handle_wpt_close,
			}

		self._open_tag_handlers={
			"gpx/wpt":self._handle_wpt_open,
			}

		self._gs_container_size_map = {
			"micro": 2.0,
			"small": 3.0,
			"regular": 4.0,
			"large": 5.0,
			"other": -1.0,
			"not chosen": -2.0,
			"virtual": 0.0,
			}

	def _handle_sym(self,text,ebi):
		self._gch.found_status = text

	def _handle_ox_awesomeness(self,text,ebi):
		self._gch.awesomeness = float( text )

	def _handle_ox_difficulty(self,text,ebi):
		self._gch.difficulty = float( text )

	def _handle_ox_size(self,text,ebi):
		self._gch.size = float( text )

	def _handle_ox_terrain(self,text,ebi):
		self._gch.terrain = float( text )

	def _handle_gs_difficulty(self,text,ebi):
		self._gch.difficulty = float( text )

	def _handle_gs_terrain(self,text,ebi):
		self._gch.terrain = float( text )

	def _handle_gs_container(self,text,ebi):
		try:
			self._gch.size = self._gs_container_size_map[text.lower()]
		except KeyError:
			print "Warning:Don't know how to handle size of '" + text + "' on cache '" + self._gch.name + "'";
			self._gch.size = -1.0

	def _handle_name(self,text,ebi):
		self._gch.name=text
		self._gch.code=text

	def _handle_gs_name(self,text,ebi):
		self._gch.name=text

	def _handle_type(self,text,ebi):
		self._gch.type=text

	def _handle_wpt_close(self,text,ebi):
		self._gch.file_len = ebi - self._gch.file_pos
		self._gch_list.append( deepcopy( self._gch ) )
		self._gch.__init__()

	def _handle_wpt_open(self,attrs,cbi):
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
		self._textbuffer = ""
		self._parser = expat.ParserCreate()
		self._parser.StartElementHandler = self._start
		self._parser.EndElementHandler = self._end
		self._parser.CharacterDataHandler = self._data
		self._parser.buffer_text = 1
		self._tag_stack = []

	def ParseText(self, blob ):
		"Parse some bytes"
		self._parser.Parse(blob,0)

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

	def ParseFile(self, filename ):
		"Parse a file specified by filename"

		#open + parse + close file
		f = open( filename )
		blob = f.read()
		f.close()
		return self.ParseText( blob )

	def _pushTag(self, tag):
		"Accumulate the tag onto the tag stack, return a string-id representing the tag-stack"
		self._tag_stack.append(tag)
		return '/'.join(self._tag_stack)

	def _popTag(self, tag):
		"Pop the current tag while validating order, return a string-id representing the previous tag-stack"
		tag_key =  '/'.join(self._tag_stack)
		popped = self._tag_stack.pop()
		if( popped != tag ):
			raise Exception("mismatched tag pairs at offset=%i", self._parser.CurrentByteIndex )
		return tag_key

	def _start(self, tag, attrs):
		tag_key = self._pushTag(tag)
		if( tag == "wpt" ):
			self._mode = "wpt"

		self._textbuffer=u""
		if( self._mode == "wpt" ):
			self._gch_parser.start( tag_key, attrs, self._parser.CurrentByteIndex )
		else:
			self._nul_parser.start( tag_key, attrs, self._parser.CurrentByteIndex )

	def _data(self, data):
		self._textbuffer += data

	def _end(self, tag):
		tag_key = self._popTag(tag)		

		#To calculate the end pos, we need the CBI, which points to the start of the tag that caused
		#the current event, and we need to add '</' , the taglen, and '>' to find the end-byte-index
		end_pos = self._parser.CurrentByteIndex + 2 + len( tag ) + 1

		if( self._mode == "wpt" ):
			self._gch_parser.end( tag_key, self._textbuffer, end_pos )
		else:
			self._nul_parser.end( tag_key, self._textbuffer, end_pos )
		
		if( tag == "wpt" or tag == "rte" or tag == "trk" ):
			self._mode = "nul"



