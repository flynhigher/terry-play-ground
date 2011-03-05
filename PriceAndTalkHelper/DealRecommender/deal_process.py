import re
import os
import sys
import sha
from pt_poster import Article, Article_Poster
from deal_parser import DealParser
from deal_recommend_engine import Engine

def regex_test(path):
	decoded_path = os.path.join(path, 'decoded1000')
	db_hash = {}
	parser = DealParser(path)
	engine = Engine(parser.get_adjusted_price)
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
		engine.insert_article_db(a)
	print "now printing"
	engine.print_db()
