import os, time, cgi, sys
from datetime import datetime, timedelta, tzinfo
import rawdoglib.plugins, rawdoglib.rawdog
import libxml2
import httplib2
import base64
import re
import ftplib
import mimetypes
#import rawdoglib.hashlib
import sha
import MySQLdb
from rawdoglib.pt_poster import Article, Article_Poster
from rawdoglib.deal_parser import DealParser
from rawdoglib.deal_recommend_engine import Engine

class NullOut:
	def write(self, s):
		pass
	
	def close(self):
		pass

class XML_Archiver:
	def __init__(self, rawdog, config):
		self.pt_poster = Article_Poster(config=config)
		pathname = os.path.dirname(sys.argv[0])				
		path = os.path.abspath(pathname)
		self.parser = DealParser(path)
		self.recommend_engine = Engine(path, self.parser.get_adjusted_price)
		self.trace = NullOut()#sys.stdout #file('testPython.txt','w')
		self.trace.write(path + '\n')

	def articles_add(self, rawdog, config, articles, article_dates):
		reImg = re.compile('<img src="http://feeds2\.feedburner\.com.*?>')
		reAmazon = re.compile('&tag=.*?["> \Z]')

		DB = 'pricentalk2'
		HOST = 'localhost'#'pricentalk2.db.4240609.hostedresource.com'
		DB_USER = 'pricentalk2'
		DB_PASSWORD = 'Paramus8'
		conn = MySQLdb.Connection(db=DB, host=HOST, user=DB_USER, passwd=DB_PASSWORD)
		cursor = conn.cursor()

		articleCount = 0
			
		for article in articles:
			entry_info = article.entry_info

			#check if title hashkey is exist
			hashKey = ''
				
			try:
				#hashKey = hashlib.sha1(entry_info['title_raw']).hexdigest()
				hashKey = sha.new(entry_info['title_raw']).hexdigest()
			except:
				continue
				#hashKey = entry_info['title_raw']

			sql = """select count(*) from tbl_article
			where article_hashkey = '%s';
			"""
			cursor.execute(sql % hashKey)
				
			result = cursor.fetchone()[0]
			if int(result) > 0:
				continue
				
			a = Article()
			a.title = entry_info['title_raw']
			a.category = rawdog.feeds[article.feed].args['category']
			a.source = rawdog.feeds[article.feed].args['name']
			a.user_id = 'priceandtalk'
			a.nickname = 'PriceAndTalk'
			a.price = self.parser.get_price(a.title)
			a.date = datetime.utcnow()
			a.keywords = self.parser.extract_keywords(a.title)
				
			if entry_info.has_key('content'):
				for content in entry_info['content']:
					a.content = content['value']
			elif entry_info.has_key('summary_detail'):
				a.content = entry_info['summary_detail']['value']
			else:
				a.content = ''
				
			content = a.content
			if rawdog.feeds[article.feed].args['category'] == 'Amazon':
				content = re.sub(reAmazon, '&tag=pric048-20', content)
				entry_info['link'] = re.sub(reAmazon, '&tag=pric048-20', entry_info['link'])
			if entry_info.has_key('link'):
				content += '<p>Source: <a href="' + entry_info['link'] + '">' + entry_info['link'] + '</a></p>'
				sys.stderr.write(entry_info['link'] + '\n')	
			a.content = re.sub(reImg, '', content)
				
			self.pt_poster.add_article(a)

			try:
					
				sql = """
				INSERT INTO tbl_article(title, category, article_content, article_hashkey, keywords, date_added)
				SELECT '%s','%s','%s','%s', '%s', now();
				"""
				#FROM DUAL
				#WHERE (SELECT COUNT(*) FROM tbl_article WHERE article_hashkey = '%s')=0;
				#"""
				cursor.execute (sql % (a.title.replace("'", "''"), a.category.replace("'", "''"), a.content.replace("'", "''"), hashKey, ','.join(a.keywords).replace("'", "''")))
				articleCount = articleCount + 1
				#trace.write(sql %(a.content, hashKey, hashKey))
			except:
				pass
				self.trace.write('Exception: %s. \n' % sys.exc_info()[0])
				self.trace.write('Exception-Value: %s. \n' % sys.exc_info()[1])
				self.trace.write('Exception-Stack: %s. \n' % sys.exc_info()[1])
			if not a.price:
				continue
			self.recommend_engine.insert_article_db(a)
			#trace.write('Key: %s: Content:%s' %(hashKey, a.content))	
			#trace.write(a.content)
			#trace.wrtie()

		cursor.close()
		conn.commit()
		conn.close()
		self.trace.write('Total article: %d \n' % articleCount )
		self.trace.write('--End of File--\n')
		#TODO:Process engine

	def write(self, rawdog, config):
		self.pt_poster.write()
		self.post_recommendation(config)
		self.recommend_engine.serialize()
		self.trace.close()
		
	def backwards(self, rawdog, config, articles):
		articles.sort()
		articles.reverse()
		return False

	def post_recommendation(self, config):
		self.pt_poster = Article_Poster(board_id=2, config=config)
		for a in self.recommend_engine.get_not_posted_deals_w_children():
			a.posted = True
			c = self.recommend_engine.get_copy(a)
			c.content += '<hr><p>Similar ones:</p>'
			for child in a.children:
				c.content += '<hr><p>' + child.title + '<br />' + child.content + '</p>' 
			self.pt_poster.add_article(c)
		self.pt_poster.write()

xml_archiver = {}
def startup(rawdog, config):
		xml_archiver = XML_Archiver(rawdog, config)
#		rawdoglib.plugins.attach_hook("feed_fetched", xml_archiver.feed_sync)
#		rawdoglib.plugins.attach_hook("article_added", xml_archiver.article_add)
		rawdoglib.plugins.attach_hook("output_write_files", xml_archiver.articles_add)
#		rawdoglib.plugins.attach_hook("article_updated", xml_archiver.article_sync)
		rawdoglib.plugins.attach_hook("shutdown", xml_archiver.write)
#		rawdoglib.plugins.attach_hook("output_sort_articles", xml_archiver.backwards)
		return True
rawdoglib.plugins.attach_hook("startup", startup)
