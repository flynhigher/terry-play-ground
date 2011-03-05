import re
import os
import sys
from pt_poster import Article, Article_Poster
from deal_parser import DealParser
import cPickle
from datetime import datetime, timedelta

class Engine:
	def __init__(self, work_path, get_adjusted_price):
		self.del_count = 10
		self.outfile_path = os.path.join(work_path, 'price.txt')
		self.dbfile_path = os.path.join(work_path, 'price.db')
#		self.tracefile_path = os.path.join(work_path, 'trace.txt')
#		self.trace = open(self.tracefile_path, 'w+')
		f = None
		try:
			f = open(self.dbfile_path, 'rb')
			self.db_price = cPickle.load(f)
			f.close()
		except IOError:
			if f:
				f.close()
			self.db_price = {}
#		self.print_db(None)
		self.remove_old_article_from_db()
		self.get_adjusted_price = get_adjusted_price
		self.similarity_rate = 0.5
	
	def remove_old_article_from_db(self):
		del_list = {}
		u = datetime.utcnow()
		valid_date = u-timedelta(days=3)
#		self.trace.write('delete_date:%s\n' % valid_date)
		for key, list in self.db_price.iteritems():
			for indx, article in enumerate(list):
#				self.trace.write('price:%s,index:%i,title:%s,a_date:%s\n' % (key, indx, article.title, article.date))
				if valid_date > article.date:
					if key in del_list:
						del_list[key].append(indx)
					else:
						del_list[key] = [indx]
		for key, indxlist in del_list.iteritems():
			for indx in reversed(sorted(indxlist)):
				del self.db_price[key][indx]
			if len(self.db_price[key]) == 0:
				del self.db_price[key]
		
	def serialize(self):
		f = None
		try:
			f = open(self.dbfile_path, 'wb')
			cPickle.dump(self.db_price, f, 2)
			f.close()
		except:
			if f:
				f.close()
		
	def insert_article_db(self, a):
		c = self.get_copy(a)
		a_price = self.get_adjusted_price(c.price)
		if a_price in self.db_price:
			self.__insert_article(self.db_price[a_price], c)
		else:
			self.db_price[a_price] = [c]
		return c
	
	def get_not_posted_deals_w_children(self):
		list = []
		for k in self.db_price.keys():
			for a in self.db_price[k]:
#				print 'price: ' + a.price + '| title: ' + a.title + '| keywords: ' + ','.join(a.keywords) + '| children: ' + (str(len(a.children)) if a.children else 'None')
				if not a.posted and a.children and len(a.children) > 0:
					list.append(a)
		return list
			
	def print_db(self, outfile = None):
		matches = []
		if outfile:
			fw = outfile
		else:
			fw = open(self.outfile_path, 'w+')
	#	fw = sys.stdout
		for p in sorted(self.db_price.keys()):
			fw.write('*** $' + str(p) + ':\n')
			for i, a in enumerate(self.db_price[p]):
				self.__print_match(fw, str(i), a.source, a.title, a.price, a.keywords)
				if a.children and len(a.children) > 0:
					matches.append(a)
					for child in a.children:
						self.__print_match(fw, ' - ', child.source, child.title, child.price, child.keywords)
		fw.write('**************************')
		for i, a in enumerate(matches):
			self.__print_match(fw, str(i), a.source, a.title, a.price, a.keywords)
			for child in a.children:
				self.__print_match(fw, ' - ', child.source, child.title, child.price, child.keywords)
		fw.close()

	def get_copy(self, a):
		copy = Article()
		copy.title = a.title
		copy.date = a.date
		copy.price = a.price
		copy.user_id = a.user_id
		copy.nickname = a.nickname
		copy.keywords = a.keywords
		copy.source = a.source
		copy.content = a.content
		copy.posted = False
		return copy
	
	def __insert_article(self, a_list, a):
		parent = self.__find_similar(a_list, a)
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
	
	def __find_similar(self, list, a):
		for item in list:
			if item.source == a.source:
#				print 'same source'
				continue
			if self.__is_similar(item, a):
#				print "== " + item.title + " || " + a.title 
				return item
#		print "!= " + item.title + " || " + a.title 
		return None
		
	def __is_similar(self, a1, a2):
		wordset1 = set(a1.keywords)
		wordset2 = set(a2.keywords)
		intersection = wordset1 & wordset2
		x = len(intersection)
		c = min(len(wordset1), len(wordset2))
#		print 'k_words1: ' + ','.join(wordset1) + '| k_words2: ' + ','.join(wordset2) + '| intersection: ' + ','.join(intersection) + '| min word len: ' + str(c)
		similar = False
		if c and x/float(c) > self.similarity_rate:
			similar = True
		return similar
	
	def __print_match(self, fw, index, source, title, price, keywords):
	#	fw.write(index + '|' + filename + '|' + source + '|' + title + '|' + price + '\n')
		fw.write(index + '|' + source + '|' + title + '|' + price + '|' + ','.join(keywords) + '\n')
