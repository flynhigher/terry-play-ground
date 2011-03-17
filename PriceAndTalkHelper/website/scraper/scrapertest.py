import unittest
import scraper
from lxml import html

class MockHtmlDataRetriever(scraper.HtmlDataRetriever):
    def __init__(self, file_name):
        self.file_name = file_name
        
    def getroot(self):
        import os
        path = os.path.join(os.path.dirname(__file__), self.file_name)
        return html.parse(path).getroot()

class MockDataRetrieverCreator(scraper.DataRetrieverCreator):
    def __init__(self, file_name):
        self.file_name = file_name

    def get_html_data_retriever(self, url):
        return MockHtmlDataRetriever(self.file_name)
    
class GetScraperTest(unittest.TestCase):
    def test_get_scraper(self):
        test = scraper.get_scraper('http://www.woot.com')
        self.assertTrue(isinstance(test, scraper.WootScraper))
        test = scraper.get_scraper('http://www.amazon.com/gp/product/B004CJ95JW/')
        self.assertTrue(isinstance(test, scraper.AmazonScraper))
        test = scraper.get_scraper('http://www.buy.com/prod/217185308.html')
        self.assertTrue(isinstance(test, scraper.BuyScraper))
        test = scraper.get_scraper('http://www.newegg.com/Product/Product.aspx?Item=N82E16889102448')
        self.assertTrue(isinstance(test, scraper.NeweggScraper))

class WootScraperTest(unittest.TestCase):
    def test_get_product(self):
        test = scraper.WootScraper(retriever_creator=MockDataRetrieverCreator('woot.htm'))
        p = test.get_product()
        #self.assertEqual(p['site'], 'woot.com')
        self.assertEqual(p['home'], 'http://www.woot.com')
        self.assertEqual(p['name'], 'Sanyo Xacti HD Camcorder & 14MP Camera w/12x Optical Zoom')
        self.assertEqual(p['description'], 'Condition: New Product:   1SanyoVPC-GH214MPHD1080Camcorder/Camera    Color: Black,Silver')
        self.assertEqual(p['price'], '129.99')
        self.assertEqual(p['shipping'], '5')
        self.assertEqual(p['image'], 'http://sale.images.woot.com/Sanyo_Xacti_HD_Camcorder___14MP_Camera_w_12x_Optical_ZoomenkStandard.jpg')

class AmazonScraperTest(unittest.TestCase):
    def test_get_product(self):
        test = scraper.AmazonScraper('http://www.amazon.com/gp/product/B004CJ95JW/',
                                     retriever_creator=MockDataRetrieverCreator('amazon.htm'))
        p = test.get_product()
        #self.assertEqual(p['site'], 'amazon.com')
        self.assertEqual(p['home'], 'http://www.amazon.com')
        self.assertEqual(p['product_id'], 'B004CJ95JW')
        self.assertEqual(p['name'], 'ASUS A52F-XA2 15.6-Inch Laptop (Black)')
        self.assertEqual(p['description'], '')
        self.assertEqual(p['price'], '499.99')
        self.assertEqual(p['shipping'], 'FREE with Super Saver Shipping')
        self.assertEqual(p['image'], 'http://ecx.images-amazon.com/images/I/41iDo0HDhbL._SL500_AA300_.jpg')
        self.assertEqual(p['image2'], '')
        self.assertEqual(p['review'], '4.4')
        self.assertEqual(p['review2'], '10')
#        self.assertEqual(p['manufacturer'], 'Samsung')
#        self.assertEqual(p['part_number'], 'BX2450')
#        self.assertEqual(p['upc'], '729507814018')
#        self.assertEqual(p['sku'], '217185308')
#        self.assertEqual(p['sales_rank'], '231')
#        self.assertEqual(p['category'], 'Monitors')
#        self.assertEqual(p['category_url'], 'http://www.buy.com/SR/SearchResults.aspx?tcid=3494')

class NeweggScraperTest(unittest.TestCase):
    def test_get_product(self):
        test = scraper.NeweggScraper('http://www.newegg.com/Product/Product.aspx?Item=N82E16889102448',
                                     retriever_creator=MockDataRetrieverCreator('newegg1.htm'))
        p = test.get_product()
        #self.assertEqual(p['site'], 'newegg.com')
        self.assertEqual(p['home'], 'http://www.newegg.com')
        self.assertEqual(p['product_id'], 'N82E16889102448')
        self.assertEqual(p['name'], 'Samsung  46"  1080p  120Hz  LCD HDTV LN46C600')
        self.assertEqual(p['description'], '')
#        self.assertEqual(p['price'], '888.99')
#        self.assertEqual(p['shipping'], 'FREE SHIPPING')
        self.assertEqual(p['image'], 'http://images10.newegg.com/ProductImageCompressAll300/89-102-448-04.jpg')
        self.assertEqual(p['review'], '5')
        self.assertEqual(p['review2'], '5')
#        self.assertEqual(p['manufacturer'], 'Samsung')
#        self.assertEqual(p['part_number'], 'BX2450')
#        self.assertEqual(p['upc'], '729507814018')
#        self.assertEqual(p['sku'], '217185308')
#        self.assertEqual(p['sales_rank'], '231')
#        self.assertEqual(p['category'], 'Monitors')
#        self.assertEqual(p['category_url'], 'http://www.buy.com/SR/SearchResults.aspx?tcid=3494')

class BuyScraperTest(unittest.TestCase):
    def test_get_product(self):
        test = scraper.BuyScraper('http://www.buy.com/prod/217185308.html',
                                  retriever_creator=MockDataRetrieverCreator('buy.htm'))
        p = test.get_product()
        #self.assertEqual(p['site'], 'buy.com')
        self.assertEqual(p['home'], 'http://www.buy.com')
        self.assertEqual(p['product_id'], '217185308')
        self.assertEqual(p['name'], 'Samsung BX2450 24" LED-backlit LCD Monitor With HDMI')
        self.assertEqual(p['description'], '')
        self.assertEqual(p['price'], '269.99')
        self.assertEqual(p['shipping'], 'FREE')
        self.assertEqual(p['image'], 'http://ak.buy.com/PI/0/500/217185308.jpg')
        self.assertEqual(p['review'], '5')
        self.assertEqual(p['review2'], '1')
        self.assertEqual(p['manufacturer'], 'Samsung')
        self.assertEqual(p['part_number'], 'BX2450')
        self.assertEqual(p['upc'], '729507814018')
        self.assertEqual(p['sku'], '217185308')
        self.assertEqual(p['sales_rank'], '231')
        self.assertEqual(p['category'], 'Monitors')
        self.assertEqual(p['category_url'], 'http://www.buy.com/SR/SearchResults.aspx?tcid=3494')

class BuyScraperTest(unittest.TestCase):
    def test_get_product(self):
        test = scraper.BuyScraper('http://www.buy.com/prod/viewsonic-viewpad-7-7-3-5g-android-2-2-800x480-multi-touch-tablet/q/loc/101/218018747.html',
                                  retriever_creator=MockDataRetrieverCreator('buy2.htm'))
        p = test.get_product()
        #self.assertEqual(p['site'], 'buy.com')
        self.assertEqual(p['home'], 'http://www.buy.com')
        self.assertEqual(p['product_id'], '218018747')
        #self.assertEqual(p['name'], 'ViewSonic ViewPad 7 -  7\xe2\x80\x9d Android 2.2* Wi-Fi/Bluetooth Tablet')
        self.assertEqual(p['description'], '')
        self.assertEqual(p['price'], '429.00')
        self.assertEqual(p['shipping'], 'FREE')
        self.assertEqual(p['image'], 'http://ak.buy.com/PI/0/500/218018747.jpg')
        self.assertEqual(p['review'], '')
        self.assertEqual(p['review2'], 'Write a Review')
        self.assertEqual(p['manufacturer'], 'Viewsonic')
        self.assertEqual(p['part_number'], 'VPAD7')
        self.assertEqual(p['upc'], '766907515817')
        self.assertEqual(p['sku'], '218018747')
        self.assertEqual(p['sales_rank'], '11596')
        self.assertEqual(p['category'], 'Tablet PCs')
        self.assertEqual(p['category_url'], 'http://www.buy.com/SR/SearchResults.aspx?cid=40683')

class RealWorldTest(unittest.TestCase):
    def testWootScraper(self):
        woot = scraper.get_scraper('http://www.woot.com')
        p = woot.get_product()
        self.assertEqual(p["shipping"], '5')