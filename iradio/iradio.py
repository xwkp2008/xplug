#!/usr/bin/env python  
#coding:utf-8  
import urllib2
import sys,os 
from sgmllib import SGMLParser
from lxml import etree as ET
import getopt;  
  
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
def usage():  
    print("Usage: [-v|-o] [--help|--output] args....");
ver="1.8"
configFile="~/.local/share/rhythmbox/rhythmdb.xml"
test=False
if "__main__" == __name__:  
    try:  
	opts,args = getopt.getopt(sys.argv[1:], "hv:o:t")  
        for opt,arg in opts:
            if opt in ("-h", "--help"):  
                usage();  
                sys.exit(1);  
            elif opt in ("-v", "--version"):  
                ver=arg 
            elif opt in ("-o", "--output"):  
		configFile=arg
            elif opt in ("-t", "--test"):  
		test=True
	    else:
		usage()
		sys.exit(1)
    except getopt.GetoptError:  
        print("getopt error!");  
        usage();  
        sys.exit(1);
class ListName(SGMLParser):
	def __init__(self):
		SGMLParser.__init__(self)
		self.is_asx = ""
		self.is_radio = ""
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
content = urllib2.urlopen('http://www.hi-fm.com/').read()
listname = ListName()
listname.feed(content)
home=os.path.expanduser('~')
configFile=configFile.replace("~",home)
print configFile
users = ET.Element('rhythmdb')  
users.attrib['version'] = ver 
if os.path.exists(configFile):
	print os.path.getsize(configFile)
	tree=ET.parse(configFile)
	users=tree.xpath('//rhythmdb')[0]
	print users 
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
		rUrl=item2.replace("../","")
		asx = urllib2.urlopen('http://www.hi-fm.com/'+rUrl).read()
		radio = ListParam()
		radio.feed(asx)
		asxUrl=radio.asx;
		print asxUrl+enc(radioName)
		findDup=tree.xpath('//rhythmdb/entry/location[text()="'+asxUrl+'"]')
		if asxUrl!="" and findDup==[]:
			entry = ET.SubElement(users, 'entry')
			entry.attrib['type'] = 'iradio' 
			title = ET.SubElement(entry, 'title')  
			title.text = enc(radioName)
			genre = ET.SubElement(entry, 'genre')  
			genre.text = enc(posName)
			location = ET.SubElement(entry, 'location')  
			location.text = asxUrl

			media_type = ET.SubElement(entry, 'media-type')  
			media_type.text = "application/octet-stream"
			artist = ET.SubElement(entry, 'artist')  
			artist.text = ""
			album = ET.SubElement(entry, 'album')  
			date = ET.SubElement(entry, 'date') 
		if test:
			break 
	if test:
		break
content=ET.tostring(users, pretty_print=True, xml_declaration=True, encoding='utf-8')
content=content.replace("&amp;#","&#")
f = open(configFile, "w") 
f.write(content)  
f.close()

