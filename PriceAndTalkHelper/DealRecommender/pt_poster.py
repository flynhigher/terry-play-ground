import os, time, cgi, sys
from datetime import datetime, timedelta, tzinfo
import libxml2
import httplib2
import base64
import re
import ftplib
import mimetypes

# A complete implementation of current DST rules for major US time zones.
ZERO = timedelta(0)
HOUR = timedelta(hours=1)

def first_sunday_on_or_after(dt):
    days_to_go = 6 - dt.weekday()
    if days_to_go:
        dt += timedelta(days_to_go)
    return dt
# US DST Rules
#
# This is a simplified (i.e., wrong for a few cases) set of rules for US
# DST start and end times. For a complete and up-to-date set of DST rules
# and timezone definitions, visit the Olson Database (or try pytz):
# http://www.twinsun.com/tz/tz-link.htm
# http://sourceforge.net/projects/pytz/ (might not be up-to-date)
#
# In the US, since 2007, DST starts at 2am (standard time) on the second
# Sunday in March, which is the first Sunday on or after Mar 8.
DSTSTART_2007 = datetime(1, 3, 8, 2)
# and ends at 2am (DST time; 1am standard time) on the first Sunday of Nov.
DSTEND_2007 = datetime(1, 11, 1, 1)
# From 1987 to 2006, DST used to start at 2am (standard time) on the first
# Sunday in April and to end at 2am (DST time; 1am standard time) on the last
# Sunday of October, which is the first Sunday on or after Oct 25.
DSTSTART_1987_2006 = datetime(1, 4, 1, 2)
DSTEND_1987_2006 = datetime(1, 10, 25, 1)
# From 1967 to 1986, DST used to start at 2am (standard time) on the last
# Sunday in April (the one on or after April 24) and to end at 2am (DST time;
# 1am standard time) on the last Sunday of October, which is the first Sunday
# on or after Oct 25.
DSTSTART_1967_1986 = datetime(1, 4, 24, 2)
DSTEND_1967_1986 = DSTEND_1987_2006

class USTimeZone(tzinfo):

    def __init__(self, hours, reprname, stdname, dstname):
        self.stdoffset = timedelta(hours=hours)
        self.reprname = reprname
        self.stdname = stdname
        self.dstname = dstname

    def __repr__(self):
        return self.reprname

    def tzname(self, dt):
        if self.dst(dt):
            return self.dstname
        else:
            return self.stdname

    def utcoffset(self, dt):
        return self.stdoffset + self.dst(dt)

    def dst(self, dt):
        if dt is None or dt.tzinfo is None:
            # An exception may be sensible here, in one or both cases.
            # It depends on how you want to treat them.  The default
            # fromutc() implementation (called by the default astimezone()
            # implementation) passes a datetime with dt.tzinfo is self.
            return ZERO
        assert dt.tzinfo is self

        # Find start and end times for US DST. For years before 1967, return
        # ZERO for no DST.
        if 2006 < dt.year:
            dststart, dstend = DSTSTART_2007, DSTEND_2007
        elif 1986 < dt.year < 2007:
            dststart, dstend = DSTSTART_1987_2006, DSTEND_1987_2006
        elif 1966 < dt.year < 1987:
            dststart, dstend = DSTSTART_1967_1986, DSTEND_1967_1986
        else:
            return ZERO

        start = first_sunday_on_or_after(dststart.replace(year=dt.year))
        end = first_sunday_on_or_after(dstend.replace(year=dt.year))

        # Can't compare naive to aware objects, so strip the timezone from
        # dt first.
        if start <= dt.replace(tzinfo=None) < end:
            return HOUR
        else:
            return ZERO

Eastern  = USTimeZone(-5, "Eastern",  "EST", "EDT")
Mountain = USTimeZone(-7, "Maountain",  "MST", "MDT")
UTC = USTimeZone(0, "UTC",  "UTC", "UTC")

def encode_multipart_formdata(fields=None, files=None):
  """
  fields is a sequence of (name, value) elements for regular form fields.
  files is a sequence of (name, filename, value) elements for data to be uploaded as files
  Return (content_type, body) ready for httplib.HTTP instance
  """
  BOUNDARY = '----------ThIs_Is_tHe_bouNdaRY_$'
  CRLF = '\r\n'
  L = []
  if fields is not None:
    for (key, value) in fields:
      L.append('--' + BOUNDARY)
      L.append('Content-Disposition: form-data; name="%s"' % key)
      L.append('')
      L.append(value)
  if files is not None:
    for (key, filename, value) in files:
      L.append('--' + BOUNDARY)
      L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, filename))
      L.append('Content-Type: %s' % get_content_type(filename))
      L.append('')
      L.append(value)
  L.append('--' + BOUNDARY + '--')
  L.append('')
  body = CRLF.join(L)
  content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
  return content_type, body

def get_content_type(filename):
    return mimetypes.guess_type(filename)[0] or 'application/octet-stream'

schema_xml = """
<grammar xmlns="http://relaxng.org/ns/structure/1.0">
  <start>
    <element name="posts">
      <attribute name="count" />
			<attribute name="id" />
			<attribute name="pubDate" />
      <zeroOrMore>
        <ref name="post" />
      </zeroOrMore>
    </element>
  </start>
  <define name="post">
    <element name="post">
			<interleave>
	    	<element name="title">
					<text />
	    	</element>
				<optional>
					<element name="content">
						<optional>
							<text />
						</optional>
					</element>
				</optional>
				<optional>
					<element name="readed_count">
						<optional>
							<text />
						</optional>
					</element>
				</optional>
				<element name="user_id">
					<text />
				</element>
				<optional>
					<element name="nick_name">
						<optional>
							<text />
						</optional>
					</element>
				</optional>
				<optional>
					<element name="email">
						<optional>
							<text />
						</optional>
					</element>
				</optional>
				<optional>
					<element name="ipaddress">
						<optional>
							<text />
						</optional>
					</element>
				</optional>
				<optional>
					<element name="allow_comment">
						<optional>
							<text />
						</optional>
					</element>
				</optional>
				<optional>
					<element name="lock_comment">
						<optional>
							<text />
						</optional>
					</element>
				</optional>
				<optional>
					<element name="allow_trackback">
						<optional>
							<text />
						</optional>
					</element>
				</optional>
				<optional>
					<element name="is_notice">
						<optional>
							<text />
						</optional>
					</element>
				</optional>
				<optional>
					<element name="is_secret">
						<optional>
							<text />
						</optional>
					</element>
				</optional>
				<optional>
					<element name="regdate">
						<optional>
							<text />
						</optional>
					</element>
				</optional>
      </interleave>
    </element>
  </define>
</grammar>
"""


class Article:
	def __init__(self):
		self.title = ""
		self.category = ''
		self.source = ''
		self.user_id = ''
		self.nickname = ''
		self.content = ''
		self.date = None
		self.retailer = None
		self.link = None
		self.feed_url = None
		self.price = None
#		self.filename = None
		self.children = None
		self.keywords = None

class Article_Poster_Exception(Exception): pass

class Article_Poster:
    __tformat = '%Y%m%d%H%M%S'
    def __init__(self, board_id=3, working_folder=None, config=None):
			self.server_url = 'http://www.ucprice.com'
			self.board_id = board_id
			self.server_out_filepath = 'rss_feed/'
			import os.path
			now = datetime.now(Mountain)
			self.out_filename = 'output' + now.strftime(self.__tformat) + '.xml'
			if config and config['defines'].has_key('outputpath'):
				self.out_file = os.path.join(config['defines']['outputpath'], self.out_filename)
			else:
				if not working_folder:
					working_folder = ""
				self.out_file = os.path.join(working_folder, self.out_filename)
			self.doc = libxml2.newDoc("1.0")
			self.xml = self.doc.newChild(None, 'posts', None)
			self.xml_articles = self.xml.xpathEval('/posts')[0]
			self.xml.setProp('pubDate', now.strftime(self.__tformat))

    def __get_module_id(self):
			module_id = {
#ucprice.com
						1: ('100', 'Shopping List'),
						2: ('84', 'Hot Deal'),
						3: ('106', 'RSS'),
#priceandtalk.com
#						1: ('109', 'Shopping List'),
#						2: ('93', 'Hot Deal'),
#						3: ('128', 'RSS'),
#						4: ('132', 'Project'),
						}
			return module_id[self.board_id][0]
			
    def writeElement(self, parent, name, content):
        xml_d = parent.xpathEval(name)
        #try:
        content = content.encode('utf-8')
        content = content.encode('base64')
        #except:
        #  print 'Base64 encoding error'
        #  print content
        if len(xml_d) is 0:
          xml_d = parent.newChild(None, name, content)
        else:
          xml_d[0].setContent(content)
        
    def add_article(self, article):
			xml_article = self.xml_articles.newChild(None, 'post', None)
			self.writeElement(xml_article, 'category', article.category);
			self.writeElement(xml_article, 'title', article.title)
			
			modified = None
			if article.date is not None:
			    #modified = datetime.fromtimestamp(article.date, Mountain)
			    modified = article.date.replace(tzinfo=Mountain)
			if modified is None:
			    modified = datetime.now(Mountain)
			#        sys.stderr.write( 'modified time: ' + modified.strftime(self.__tformat) + '\n')
			
			self.writeElement(xml_article, 'regdate', modified.strftime(self.__tformat));
			self.writeElement(xml_article, 'user_id', article.user_id);
			self.writeElement(xml_article, 'nick_name', article.nickname);
			self.writeElement(xml_article, 'content', article.content)
			self.writeElement(xml_article, 'tags', ','.join(article.keywords))
			
			return True

    def __write(self):
        self.doc.setDocCompressMode(0)
        self.doc.saveFormatFile(self.out_file, 1)
        self.doc.freeDoc()
#    def __ftp(self):
#        FTP_HOST = 'ucprice.com'
#        FTP_USER = 'flynhigh'
#        FTP_PASS = 'xxxx'
#        
#        f=None
#        while not f:
#          try:
#            f=ftplib.FTP(FTP_HOST,FTP_USER,FTP_PASS)
#          except ftplib.error_perm:
#            f=None
#            
#        f.storlines('STOR ' + self.server_out_filepath + self.out_filename, open(self.out_file,'r'))
    def __upload(self):
			http = httplib2.Http()
			
			url = self.server_url + '/etc/upload.php'
			f=open(self.out_file, 'r')
			body = f.read()
			content_type, body = encode_multipart_formdata(files=[('attachment', self.out_filename, body)])
			headersxml = {'Content-type': content_type, 'Content-Length': str(len(body))}
			response, content = http.request(url, 'POST', headers=headersxml, body=body)
			if(content.find('success') < 0):
			  sys.stderr.write( 'headers:\n')
			  for key in headersxml.keys():
			    sys.stderr.write( '   ' + key + ':' + headersxml[key] + '\n')
			  raise Exception('File upload error, response content: ' + content)
    def __post(self):
        http = httplib2.Http()

        url = self.server_url + '/index.php'
        login = """<?xml version="1.0" encoding="utf-8"?>
        <methodCall>
        <params>
        <user_id>
        <![CDATA[admin]]>
        </user_id>
        <password>
        <![CDATA[Paramus8]]>
        </password>
        <keep_signed>
        <![CDATA[]]>
        </keep_signed>
        <module>
        <![CDATA[member]]>
        </module>
        <act>
        <![CDATA[procMemberLogin]]>
        </act>
        </params>
        </methodCall>"""

        file = """<?xml version="1.0" encoding="utf-8"?>
        <methodCall>
        <params>
        <xml_file>
        <![CDATA[?file?]]>
        </xml_file>
        <type>
        <![CDATA[module]]>
        </type>
        <module>
        <![CDATA[importer]]>
        </module>
        <act>
        <![CDATA[procImporterAdminPreProcessing]]>
        </act>
        </params>
        </methodCall>"""

        target = """<?xml version="1.0" encoding="utf-8"?>
        <methodCall>
        <params>
        <type>
        <![CDATA[module]]>
        </type>
        <total>
        <![CDATA[?total?]]>
        </total>
        <cur>
        <![CDATA[0]]>
        </cur>
        <key>
        <![CDATA[?key?]]>
        </key>
        <target_module>
        <![CDATA[?module_id?]]>
        </target_module>
        <guestbook_target_module>
        <![CDATA[]]>
        </guestbook_target_module>
        <unit_count>
        <![CDATA[1000]]>
        </unit_count>
        <user_id>
        <![CDATA[]]>
        </user_id>
        <module>
        <![CDATA[importer]]>
        </module>
        <act>
        <![CDATA[procImporterAdminImport]]>
        </act>
        </params>
        </methodCall>"""
        
        headersxml = {'Content-type': 'application/xml'}
        headersxml['Content-Length'] = str(len(login))
        response, content = http.request(url, 'POST', headers=headersxml, body=login)
        if(content.find('success') < 0):
          sys.stderr.write( 'headers:\n')
          for key in headersxml.keys():
            sys.stderr.write( '   ' + key + ':' + headersxml[key] + '\n')
          sys.stderr.write( 'login xml:\n' + login + '\n')
          sys.stderr.write( 'size: ' + str(len(login)) + '\n')
          raise Exception('Login post error, response content: ' + content)
        headersxml['Cookie'] = 'editor_mode=html; ' + response['set-cookie']
        file = file.replace('?file?', self.server_out_filepath + self.out_filename)
        headersxml['Content-Length'] = str(len(file))
        response, content = http.request(url, 'POST', headers=headersxml, body=file)
        if(content.find('success') < 0):
          raise Exception('File post error, response content: ' + content)
        resXml = libxml2.parseMemory(content, len(content))
        total = resXml.xpathEval('//total')
        total = map ( libxml2.xmlNode.getContent, total)[0]
        key = resXml.xpathEval('//key')
        key = map ( libxml2.xmlNode.getContent, key)[0]
        target = target.replace('?total?', total)
        target = target.replace('?key?', key)
        target = target.replace('?module_id?', self.__get_module_id())
        headersxml['Content-Length'] = str(len(target))
        response, content = http.request(url, 'POST', headers=headersxml, body=target)
        if(content.find('key') < 0):
          raise Exception('Target post error, response content: ' + content)

    def __delete(self):
        os.remove(self.out_file)
					   
    def write(self):
        self.__write()
#        self.__ftp()
        self.__upload()
        self.__post()
#        self.__delete()
        return True
