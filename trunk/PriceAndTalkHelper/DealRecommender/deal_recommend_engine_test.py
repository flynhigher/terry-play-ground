import unittest
import os
import sys
from datetime import datetime, timedelta
from deal_parser import DealParser
from deal_recommend_engine import Engine
from pt_poster import Article

class DealParserTest(unittest.TestCase):
	def setUp(self):
		self.output = ''
		pathname = os.path.dirname(sys.argv[1])        
		orig_work_path = os.path.abspath(pathname)
		self.parser = DealParser(orig_work_path)
		self.test_work_path = os.path.join(orig_work_path, 'test')
		self.test = Engine(self.test_work_path, self.parser.get_adjusted_price)
		for i in range(1,21):
			u = datetime.utcnow()
			d = u if i <= 10 else u-timedelta(days=4)
			a = Article()
			a.title = 'test title ' + str(i)
			a.date = d
			a.price = '$' + str(i)
			a.keywords = ['test','keywords' + str(i)]
			a.source = 'test category ' + str(i)
			self.test.insert_article_db(a)
#		self.test_text = [
#			 ('Samsung LUXIA 40" 120Hz 1080p Widescreen LED LCD HDTV for $1,100 + free shipping', 'samsung,luxia,40,120hz,1080p,widescreen,led,lcd,hdtv', '$1,100', 1100)
#			,('Samsung UN40B6000 40" Class LED High Definition TV - 1080p, 1920x1080, 3000000:1 Dynamic, 4ms, 120Hz, 4x HDMI  for $1099.99', 'samsung,un40b6000,40,class,led,high,definition,tv,1080p,1920x1080,3000000,1,dynamic,4ms,120hz,4x,hdmi', '$1099.99', 1100)
#			,('*Free Blu-ray Player, ends 1/30* SAMSUNG 52" 16:9 6ms 1080p LCD HDTV w/ TOC Design - Reg. $1799.99, Now $1199 Shipped w/ Free Blu-Ray Player!', 'blu-ray,blu,ray,bluray,player,ends,1,30,samsung,52,16,9,6ms,1080p,lcd,hdtv,toc,design,reg.', '$1199', 1199)
#			,('DIY desktop from newegg (i5-750,HD 5850 CFX) - $1231.69 After Rebates Shipped', 'diy,desktop,newegg,i5-750,i5,750,i5750,hd,5850,cfx', '$1231.69', 1231.69)
#			,('HP TouchSmart 600xt, Intel(R) Core(TM) 2 Duo processor T6600 [2.2GHz], 23" diagonal hi-def widescreen, 4GB RAM, 640GB, Slot-load SuperMulti DVD burner, 1GB NVIDIA GeForce GT230M, and game console connections, 6-in-1 memory card reader, 802.11 b/g/N, Bluetooth, Integrated high-performance 2.0 speakers, Windows 7 Home Premium, HP wireless keyboard and HP wireless optical mouse   for $1299.99', 'hp,touchsmart,600xt,intel,r,core,tm,2,duo,processor,t6600,2.2ghz,23,diagonal,hi-def,hi,def,hidef,widescreen,4gb,ram,640gb,slot-load,slot,load,slotload,supermulti,dvd,burner,1gb,nvidia,geforce,gt230m,game,console,connections,6-in-1,6,in,1,6in1,memory,card,reader,802.11,b,g,n,bluetooth,integrated,high-performance,high,performance,highperformance,2.0,speakers,windows,7,home,premium,wireless,keyboard,optical,mouse', '$1299.99', 1300)
#			,('Wine & Dine On Valentine''s Day - Get $25.00 Restaurant Gift Certificates For Only $2.00!', 'wine,dine,valentine''s,get,restaurant,gift,certificates', '$2.00',2)
#			,('', '', '', )
#			,('', '', '', )
#			,('', '', '', )
#			,('', '', '', )
#										 ]

	def tearDown(self):
		if os.path.isfile(self.test.outfile_path):
			os.remove(self.test.outfile_path)
		if os.path.isfile(self.test.dbfile_path):
			os.remove(self.test.dbfile_path)
		self.test = None
		self.parser = None

	def write(self, content):
		self.output += content
		
	def close(self):
		pass
	
	def test_remove_old_article_from_db(self):
		self.test.remove_old_article_from_db()
		self.test.print_db(self)
		expected = '*** $1.0: 0|test category 1|test title 1|$1|test,keywords1 *** $2.0: 0|test category 2|test title 2|$2|test,keywords2 *** $3.0: 0|test category 3|test title 3|$3|test,keywords3 *** $4.0: 0|test category 4|test title 4|$4|test,keywords4 *** $5.0: 0|test category 5|test title 5|$5|test,keywords5 *** $6.0: 0|test category 6|test title 6|$6|test,keywords6 *** $7.0: 0|test category 7|test title 7|$7|test,keywords7 *** $8.0: 0|test category 8|test title 8|$8|test,keywords8 *** $9.0: 0|test category 9|test title 9|$9|test,keywords9 *** $10.0: 0|test category 10|test title 10|$10|test,keywords10 **************************'
		self.assertEquals(expected, self.output.replace('\n', ' ').replace('\r', ''), '')#'price: ' + case[2] + ' not found in ' + case[0])
		
	def test_serialize(self):
		self.assertEquals(20, len(self.test.db_price))
		self.test.serialize()
		new_test = Engine(self.test_work_path, self.parser.get_adjusted_price)
		new_test.print_db(self)
		expected = '*** $1.0: 0|test category 1|test title 1|$1|test,keywords1 *** $2.0: 0|test category 2|test title 2|$2|test,keywords2 *** $3.0: 0|test category 3|test title 3|$3|test,keywords3 *** $4.0: 0|test category 4|test title 4|$4|test,keywords4 *** $5.0: 0|test category 5|test title 5|$5|test,keywords5 *** $6.0: 0|test category 6|test title 6|$6|test,keywords6 *** $7.0: 0|test category 7|test title 7|$7|test,keywords7 *** $8.0: 0|test category 8|test title 8|$8|test,keywords8 *** $9.0: 0|test category 9|test title 9|$9|test,keywords9 *** $10.0: 0|test category 10|test title 10|$10|test,keywords10 **************************'
		self.assertEquals(expected, self.output.replace('\n', ' ').replace('\r', ''), '')#'price: ' + case[2] + ' not found in ' + case[0])
		
	def test_insert_article_db(self):
		self.assertEquals(20, len(self.test.db_price))
		a = Article()
		a.title = 'test title'
		a.date = datetime.utcnow()
		a.price = '$1'
		a.keywords = ['test', 'title']
		a.source = 'test category 1'
		self.test.insert_article_db(a)
		self.test.print_db(self)
		expected = '*** $1.0: 0|test category 1|test title 1|$1|test,keywords1 1|test category 1|test title|$1|test,title *** $2.0: 0|test category 2|test title 2|$2|test,keywords2 *** $3.0: 0|test category 3|test title 3|$3|test,keywords3 *** $4.0: 0|test category 4|test title 4|$4|test,keywords4 *** $5.0: 0|test category 5|test title 5|$5|test,keywords5 *** $6.0: 0|test category 6|test title 6|$6|test,keywords6 *** $7.0: 0|test category 7|test title 7|$7|test,keywords7 *** $8.0: 0|test category 8|test title 8|$8|test,keywords8 *** $9.0: 0|test category 9|test title 9|$9|test,keywords9 *** $10.0: 0|test category 10|test title 10|$10|test,keywords10 *** $11.0: 0|test category 11|test title 11|$11|test,keywords11 *** $12.0: 0|test category 12|test title 12|$12|test,keywords12 *** $13.0: 0|test category 13|test title 13|$13|test,keywords13 *** $14.0: 0|test category 14|test title 14|$14|test,keywords14 *** $15.0: 0|test category 15|test title 15|$15|test,keywords15 *** $16.0: 0|test category 16|test title 16|$16|test,keywords16 *** $17.0: 0|test category 17|test title 17|$17|test,keywords17 *** $18.0: 0|test category 18|test title 18|$18|test,keywords18 *** $19.0: 0|test category 19|test title 19|$19|test,keywords19 *** $20.0: 0|test category 20|test title 20|$20|test,keywords20 **************************'
		self.assertEquals(expected, self.output.replace('\n', ' ').replace('\r', ''), '')#'price: ' + case[2] + ' not found in ' + case[0])
	
	def test_get_not_posted_deals_w_children(self):
		self.assertEquals(20, len(self.test.db_price))
		a = Article()
		a.title = 'test title'
		a.date = datetime.utcnow()
		a.price = '$1'
		a.keywords = ['test', 'keywords1']
		a.source = 'test category 2'
		inserted = self.test.insert_article_db(a)
		self.assertFalse(inserted.posted)
		list = self.test.get_not_posted_deals_w_children()
		self.assertEquals(1, len(list))
		for deal in list:
			deal.posted = True
		list = self.test.get_not_posted_deals_w_children()
		self.assertEquals(0, len(list))
		
		
if __name__ == '__main__':
	unittest.main()