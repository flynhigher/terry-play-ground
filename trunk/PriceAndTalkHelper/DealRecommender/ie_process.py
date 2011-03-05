import nltk
from lxml import etree
import re
import os
import sys
from pt_poster import Article, Article_Poster
from deal_parser import DealParser

sample_path = None
rss_path = None
decoded_path = None
parser = None
db_hash = {}
db_price = {}

def init_path(work_path):
	global sample_path, rss_path, decoded_path
	sample_path = work_path + '\\sample_data'
	rss_path = work_path + '\\rss_data'
	decoded_path = work_path + '\\decoded1000'

def regex_test(path):
	global parser
	parser = DealParser(path)
	import sha
	for filename in os.listdir(decoded_path):
		doc = open(decoded_path + '\\' + filename, 'r')
		doc = doc.read().split('||')
		a = Article()
		try:
			a.filename = filename
			a.category = doc[0]
			a.title = doc[1]
			a.date = doc[2]
		except:
			sys.stdout.write('content error: ' + filename + '\n')
			continue
		try:
			a.hashKey = sha.new(a.title).hexdigest()
		except:
			pass
		if a.hashKey in db_hash:
			continue
		else:
			db_hash[a.hashKey] = a

		a.price = parser.get_price(a.title)
		if not a.price:
			#sys.stdout.write("can't find price: " + filename + ', title: ' + a.title + '\n')
			continue
		a.keywords = parser.extract_keywords(a.title)
		insert_article_db(a)
	print "now printing"
	print_db()

def insert_article_db(a):	
	a_price = parser.get_adjusted_price(a.price)
	if a_price in db_price:
		insert_article(db_price[a_price], a)
	else:
		db_price[a_price] = [a]

def insert_article(a_list, a):
	parent = find_similar(a_list, a)
	if parent:
		if not parent.children:
			parent.children = []
		parent.children.append(a)
#		print 'found similar: ' + parent.title + '::' + a.title
	else:
		a_list.append(a)
#		print 'no similar: ' + a.title + '::' + a.price
#		for aa in a_list:
#			print ' - ' + aa.title

def find_similar(list, a):
	for item in list:
		if item.category == a.category:
			continue
		if is_similar(item, a):
#			print "== " + item.title + " || " + a.title 
			return item
#	print "!= " + item.title + " || " + a.title 
	return None
	
def is_similar(a1, a2):
	wordset1 = set(a1.keywords)
	wordset2 = set(a2.keywords)
	intersection = wordset1 & wordset2
	x = len(intersection)
	c = min(len(wordset1), len(wordset2))
	return True if c and x/float(c) > 0.5 else False
	
def print_db():
	matches = []
	fw = open('price.txt', 'w+')
#	fw = sys.stdout
	for p in sorted(db_price.keys()):
		fw.write('*** $' + str(p) + ':\n')
		for i, a in enumerate(db_price[p]):
			print_match(fw, str(i), a.category, a.filename, a.title, a.price, a.keywords)
			if a.children and len(a.children) > 0:
				matches.append(a)
				for child in a.children:
					print_match(fw, ' - ', child.category, child.filename, child.title, child.price, child.keywords)
	fw.write('**************************')
	for i, a in enumerate(matches):
		print_match(fw, str(i), a.category, a.filename, a.title, a.price, a.keywords)
		for child in a.children:
			print_match(fw, ' - ', child.category, child.filename, child.title, child.price, child.keywords)
	fw.close()
	
def decode(path):
	init_path(path)
	for filename in os.listdir(rss_path):
		doc = None
		try:
			doc = etree.parse(rss_path + '\\' + filename)
		except:
			sys.stderr.write('etree parsing error: ' + filename)
			continue
		for index, post in enumerate(doc.xpath('//post')):
			regdate = user_id = nick_name = content = title = category = None
			fw = open(decoded_path + '\\decoded_' + filename + str(index), 'w+')
			for i, e in enumerate(post):
				if e.tag == 'title' or e.tag == 'content' or e.tag == 'category' or e.tag == 'nick_name' or e.tag == 'user_id' or e.tag == 'regdate':
					if i > 0:
						fw.write('||')
					fw.write (nltk.clean_html(re.sub('<br\s*?/?>|</?p\s*?/?>', '. ', e.text.decode('base64') if e.text else '')))
#					t = nltk.clean_html(re.sub('<br\s*?/?>|</?p\s*?/?>', '. ', e.text.decode('base64') if e.text else ''))
#					try:
#						e.text = t.encode('utf-8')
#					except:
#						print 'Encoding error: ' + t
			#sys.stdout.write(str(dir(doc)))
			#fw.write(doc)
			#doc.write(fw)
			fw.close()

def print_match(fw, index, category, filename, title, price, keywords):
#	fw.write(index + '|' + filename + '|' + category + '|' + title + '|' + price + '\n')
	fw.write(index + '|' + category + '|' + title + '|' + price + '|' + ','.join(keywords) + '\n')
	
def pos_tag():
	for filename in os.listdir(path):
		doc = etree.parse(path + '\\' + filename)
		for post in doc.xpath('//post'):
			content = title = None
			for e in post:
				cleaned = nltk.clean_html(re.sub('<br\s*?/?>|</?p\s*?/?>', '. ', e.text.decode('base64')))
				if e.tag == 'content':
					content = cleaned
				if e.tag == 'title':
					title = cleaned
				#fw.write(e.tag + ':' + cleaned + '\n')
			#fw.write('title-ie:' + '\n')
			fw.write(str(ie_preprocess(title)))
			fw.write('\n')
			#fw.write('content-ie:' + '\n')
			fw.write(str(ie_preprocess(content)))
			fw.write('\n')


class IndexedText():
	def __init__(self, doc, stemmer=None):
		self._doc = doc
		self._stemmer = stemmer
		self._index = nltk.Index((self.stem(word), i) for (i, word) in enumerate(doc))
		
	def concordance(self, word, width=40):
		key = self.stem(word)
		wc = width
		for i in self._index[key]:
			lcontext = ''.join(self._doc[i-wc:i])
			rcontext = ''.join(self._doc[i:i+wc])
			ldisplay = '%*s' % (width, lcontext[-width:])
			rdisplay = '%-*s' % (width, rcontext[:width])
			print ldisplay, rdisplay
			
	def stem(self, word):
		return self._stemmer.stem(word).lower() if self._stemmer else word