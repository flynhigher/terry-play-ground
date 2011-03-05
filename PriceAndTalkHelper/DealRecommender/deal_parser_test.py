import unittest
import os
import sys
from deal_parser import DealParser

class DealParserTest(unittest.TestCase):
	def setUp(self):
		pathname = os.path.dirname(sys.argv[1])        
		self.test = DealParser(os.path.abspath(pathname))
		self.test_text = [
			 ('Samsung LUXIA 40" 120Hz 1080p Widescreen LED LCD HDTV for $1,100 + free shipping', 'samsung,luxia,40,120hz,1080p,widescreen,led,lcd,hdtv', '$1,100', 1100)
			,('Samsung UN40B6000 40" Class LED High Definition TV - 1080p, 1920x1080, 3000000:1 Dynamic, 4ms, 120Hz, 4x HDMI  for $1099.99', 'samsung,un40b6000,40,class,led,high,definition,tv,1080p,1920x1080,3000000,1,dynamic,4ms,120hz,4x,hdmi', '$1099.99', 1100)
			,('*Free Blu-ray Player, ends 1/30* SAMSUNG 52" 16:9 6ms 1080p LCD HDTV w/ TOC Design - Reg. $1799.99, Now $1199 Shipped w/ Free Blu-Ray Player!', 'blu-ray,blu,ray,bluray,player,ends,1,30,samsung,52,16,9,6ms,1080p,lcd,hdtv,toc,design,reg.', '$1199', 1199)
			,('DIY desktop from newegg (i5-750,HD 5850 CFX) - $1231.69 After Rebates Shipped', 'diy,desktop,newegg,i5-750,i5,750,i5750,hd,5850,cfx', '$1231.69', 1231.69)
			,('HP TouchSmart 600xt, Intel(R) Core(TM) 2 Duo processor T6600 [2.2GHz], 23" diagonal hi-def widescreen, 4GB RAM, 640GB, Slot-load SuperMulti DVD burner, 1GB NVIDIA GeForce GT230M, and game console connections, 6-in-1 memory card reader, 802.11 b/g/N, Bluetooth, Integrated high-performance 2.0 speakers, Windows 7 Home Premium, HP wireless keyboard and HP wireless optical mouse   for $1299.99', 'hp,touchsmart,600xt,intel,r,core,tm,2,duo,processor,t6600,2.2ghz,23,diagonal,hi-def,hi,def,hidef,widescreen,4gb,ram,640gb,slot-load,slot,load,slotload,supermulti,dvd,burner,1gb,nvidia,geforce,gt230m,game,console,connections,6-in-1,6,in,1,6in1,memory,card,reader,802.11,b,g,n,bluetooth,integrated,high-performance,high,performance,highperformance,2.0,speakers,windows,7,home,premium,wireless,keyboard,optical,mouse', '$1299.99', 1300)
			,('Wine & Dine On Valentine''s Day - Get $25.00 Restaurant Gift Certificates For Only $2.00!', 'wine,dine,valentine''s,get,restaurant,gift,certificates', '$2.00',2)
#			,('', '', '', )
#			,('', '', '', )
#			,('', '', '', )
#			,('', '', '', )
										 ]

	def tearDown(self):
		self.test = None
		
	def test_get_price(self):
		for case in self.test_text:
			price = self.test.get_price(case[0])
			self.assertEquals(case[2], price, 'price: ' + case[2] + ' not found in ' + case[0])
	
	def test_extract_keywords(self):
		for case in self.test_text:
			keywords = self.test.extract_keywords(case[0])
			self.assertEquals(case[1], ','.join(keywords), 'keywords: ' + case[2] + ' not found in ' + case[0])
	
	def test_get_adjusted_price(self):
		for case in self.test_text:
			a_price = self.test.get_adjusted_price(case[2])
			self.assertEquals(float(case[3]), a_price, str(float(case[3])) + ' != ' + str(a_price) + ' for ' + case[2])
	
if __name__ == '__main__':
	unittest.main()