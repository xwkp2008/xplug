#!/usr/bin/env python  
#coding:utf-8  
import urllib2
import sys
from sgmllib import SGMLParser
import xml.dom.minidom as Dom  
import getopt;  
  
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
def usage():  
    print("Usage: [-v|-o] [--help|--output] args....");
ver="1.8"
configFile="~/.local/share/rhythmbox/rhythmdb.xml"
if "__main__" == __name__:  
    #lsArgs = [""];  
      
    try:  
        opts,args = getopt.getopt(sys.argv[1:], "hv:o", ["help","version=" "output="]);  
        for opt,arg in opts:  
            if opt in ("-h", "--help"):  
                usage();  
                sys.exit(1);  
            elif opt in ("-v", "--version"):  
                ver=arg 
            elif opt in ("-o", "--output"):  
		configFile=arg
    except getopt.GetoptError:  
        print("getopt error!");  
        usage();  
        sys.exit(1);
class ListName(SGMLParser):
	def __init__(self):
		SGMLParser.__init__(self)
		self.is_asx = ""
		self.is_radio = ""
		self.asx = ""
		self.urls = {}
		self.flag = ""
	def handle_data(self, text):
		if self.flag!="":
			self.urls[self.flag]=text
	def start_a(self, attrs):                       
        	href = [v for k, v in attrs if k=='href']
        	if href[0].startswith("/") or href[0].startswith("../"):  
            		self.urls[href[0]]=""
			self.flag=href[0]
			self.is_radio = 1
	def end_a(self):                       
		self.flag=""
		self.is_radio = ""
class ListParam(SGMLParser):
	def __init__(self):
		SGMLParser.__init__(self)
		self.asx = ""
	def start_param(self, attrs):
		for k, v in attrs:
			if k=="name" and v=="Filename":
				self.asx = attrs[1][1]
				break
	def end_param(self):                       
		self.asx=""
#html实体编码10进制，兼容16进制
def enc(unicode_data, encoding='ascii'):
	return unicode_data.encode(encoding, 'xmlcharrefreplace')
	#return unicode_data
class XMLGenerator:  
    def __init__(self, xml_name):  
        self.doc = Dom.Document()  
        self.xml_name = xml_name  
          
    def createNode(self, node_name):  
        return self.doc.createElement(node_name)  
      
    def addNode(self, node, prev_node = None):  
        cur_node = node  
        if prev_node is not None:  
            prev_node.appendChild(cur_node)  
        else:  
            self.doc.appendChild(cur_node)  
        return cur_node  
  
    def setNodeAttr(self, node, att_name, value):  
        cur_node = node  
        cur_node.setAttribute(att_name, value)  
  
    def setNodeValue(self, cur_node, value):  
        node_data = self.doc.createTextNode(value)  
        cur_node.appendChild(node_data)  
  
    def genXml(self):  
        f = open(self.xml_name, "w")  
        f.write(self.doc.toprettyxml(indent = "\t", newl = "\n"))  
        f.close()  
content = urllib2.urlopen('http://www.hi-fm.com/').read()
listname = ListName()
listname.feed(content)
doc = Dom.Document()
root_node = doc.createElement("rhythmdb")
root_node.setAttribute("version", ver) 
doc.appendChild(root_node)
dbxml = XMLGenerator("/tmp/rhythmdb.xml")  
#xml root node  
rhythmdb = myXMLGenerator.createNode("rhythmdb")  
myXMLGenerator.setNodeAttr(rhythmdb, "version", ver)  
for item in listname.urls:
	posName=listname.urls[item].decode('gbk').encode('utf8')
	print item+enc(posName)
	muluItem=item.replace("/","")
	content2 = urllib2.urlopen('http://www.hi-fm.com/mulu/'+muluItem+'01.htm').read()
	listname2 = ListName()
	listname2.feed(content2)
	for item2 in listname2.urls:
		radioName=listname2.urls[item2].decode('gbk').encode('utf8')
		radioName="".join(radioName.split())
		radioName=radioName.strip()
		asx = urllib2.urlopen('http://www.hi-fm.com/'+muluItem).read()
		radio = ListParam()
		radio.feed(asx)
		asxUrl=radio.asx;
		print asxUrl+enc(radioName)
		entry_node = doc.createElement("entry")
		entry_title = doc.createElement("title")
		entry_title_value=doc.createTextNode(enc(radioName))
		entry_title.appendChild(entry_title_value)
		entry_genre = doc.createElement("genre")
		entry_genre_value=doc.createTextNode(enc(radioName))
		entry_genre.appendChild(entry_genre_value)
		entry_location = doc.createElement("location")
		entry_location_value=doc.createTextNode(asxUrl)
		entry_location.appendChild(entry_location_value)
		entry_media_type = doc.createElement("media-type")
		entry_media_type_value=doc.createTextNode("application/octet-stream")
		entry_media_type.appendChild(entry_media_type_value)
		
		entry_artist = doc.createElement("artist")
		entry_artist_value=doc.createTextNode("")
		entry_artist.appendChild(entry_artist_value)

		entry_album = doc.createElement("album")
		entry_album_value=doc.createTextNode("")
		entry_album.appendChild(entry_album_value)
		
		entry_date = doc.createElement("date")
		entry_date_value=doc.createTextNode("")
		entry_date.appendChild(entry_date_value)

		entry_node.appendChild(entry_title)
		entry_node.appendChild(entry_genre)
		entry_node.appendChild(entry_location)
		entry_node.appendChild(entry_media_type)
		entry_node.appendChild(entry_artist)
		entry_node.appendChild(entry_album)
		entry_node.appendChild(entry_date)
		entry_node.setAttribute("type","iradio") 
		root_node.appendChild(entry_node)
		break
	break
f = open("", "w") 
f.write(doc.toprettyxml(indent = "\t",newl = "\n"))  
f.close()


