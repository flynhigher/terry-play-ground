import os
import re
from lxml import html, etree

from logger import *

def get_scraper(url):
    if url:
        if url.find('amazon.com') >= 0:
            return AmazonScraper(url)
        elif url.find('newegg.com') >= 0:
            return NeweggScraper(url)
        elif url.find('buy.com') >= 0:
            return BuyScraper(url)
        elif url.find('woot.com') >= 0:
            return WootScraper()
        else:
            return None
    else:
        raise InvalidArgumentScraperError()

class InvalidArgumentScraperError(Exception):
    pass

class ProductAttribute():
    def __init__(self, split):
        if not split:
            raise InvalidArgumentScraperError()
        self.key = split[0]
        self.path = split[1]
        self.regex = None
        if len(split) >= 3 and split[2]:
            self.regex = split[2]
        self.value = None
        if len(split) >= 4 and split[3]:
            self.value = split[3]

class DataRetriever(object):
    def process(self, attributes):
        pass

class ObjectDataRetriever(DataRetriever):
    def __init__(self, sender):
        self.scraper = sender

    def process(self, attributes):
        for item in attributes:
            if item.path\
                and item.path.startswith('scraper'):
                attr_name = item.path.split('.')[1]
                v = getattr(self.scraper, attr_name)
                if v:
                    item.value = v
        return attributes

class RegexDataRetriever(DataRetriever):
    def process(self, attributes):
        import re
        for item in attributes:
            if item.regex:
                m = re.search(item.regex, item.value)
                if m:
                    if len(m.groups()) > 0:
                        item.value = m.group(1)
                    elif m.group():
                        item.value = m.group()
        return attributes

class HtmlDataRetriever(DataRetriever):
    def __init__(self, url):
        self.url = url

    def process(self, attributes):
        return self.__parse_product_attributes(attributes)

    def getroot(self):
        return html.parse(self.url).getroot()

    def __parse_product_attributes(self, attributes):
        root = self.getroot()
        for item in attributes:
            if item.path \
                and not item.path.startswith('scraper'):
                value = self.__get_xpath_value(root, item.path)
                if not isinstance(value, str):
                    if isinstance(value, etree._ElementUnicodeResult):
                        #cannot serializable - don't know why getting below error
                        #Type 'lxml.etree._ElementUnicodeResult' cannot be serialized.
                        pass
                    else:
                        value = html.tostring(value, method='text', encoding='UTF-8').replace(' ', '').replace('\n', '').replace('\r', ' ')
                #value = re.sub('', '', value)
                item.value = value.strip()
        return attributes

    def __get_xpath_value(self, root, xpath):
        result = root.xpath(xpath)
        value = ''
        if result:
            value = result[0]
        return value

class DataRetrieverCreator(object):
    def get_html_data_retriever(self, url):
        return HtmlDataRetriever(url);
    def get_object_data_retriever(self, scraper):
        return ObjectDataRetriever(scraper);
    def get_regex_data_retriever(self):
        return RegexDataRetriever();
    def get_retrievers(self, scraper):
        return [self.get_html_data_retriever(scraper.url),
            self.get_object_data_retriever(scraper),
            self.get_regex_data_retriever()]

class Scraper(object):
    def __init__(self, site_name, url, retriever_creator=DataRetrieverCreator(), config_file='scraper.cfg'):
        self.url = url
        self.retrievers = retriever_creator.get_retrievers(self)
        self.product_attributes = []
        path = os.path.join(os.path.dirname(__file__), config_file)
        write_trace('site_name:' + site_name)
        write_trace('url:' + url)
        write_trace('scraper path:' + path)
        f = open(path)
        config_found = False
        for line in f.readlines():
            line = line.rstrip('\r\n')
            if config_found and not line:
                break
            if not line:
                continue
            split = line.split('|')
            if split \
                and split[0] == 'site' \
                and split[3].lower() == site_name.lower():
                config_found = True
                self.product_attributes.append(ProductAttribute(split))
                continue
            if config_found:
                self.product_attributes.append(ProductAttribute(split))

    def get_product(self):
        for retriever in self.retrievers:
            self.product_attributes = retriever.process(self.product_attributes)
        key_value = {}
        for attr in self.product_attributes:
            key_value[attr.key] = attr.value
        
        return key_value

    def get_full_url (self):
        return self.url

class ProductUrlScraper(Scraper):
    def __init__(self, site_name, product_url='', product_url_format=''):
        super(ProductUrlScraper, self).__init__(site_name)
        self.product_url = product_url
        self.product_id = product_id
        self.product_url_format = product_url_format

    def get_full_url(self):
        if self.product_id:
            if not self.product_url_format:
                raise InvalidArgumentScraperError()
            return self.product_url_format % self.product_id
        else:
            return self.product_url

class WootScraper(Scraper):
    def __init__(self, retriever_creator=None):
        if retriever_creator:
            super(WootScraper, self).__init__(
                    site_name='woot.com',
                    url='http://www.woot.com', 
                    retriever_creator=retriever_creator)
        else:
            super(WootScraper, self).__init__(
                    site_name='woot.com',
                    url='http://www.woot.com')

class NeweggScraper(Scraper):
    def __init__(self, product_url, retriever_creator=None):
        if retriever_creator:
            super(NeweggScraper, self).__init__(
                site_name='newegg.com',
                url=product_url,
                retriever_creator=retriever_creator)
        else:
            super(NeweggScraper, self).__init__(
                site_name='newegg.com',
                url=product_url)

class AmazonScraper(Scraper):
    def __init__(self, product_url, retriever_creator=None):
        if retriever_creator:
            super(AmazonScraper, self).__init__(
                site_name='amazon.com',
                url=product_url,
                retriever_creator=retriever_creator)
        else:
            super(AmazonScraper, self).__init__(
                site_name='amazon.com',
                url=product_url)

class BuyScraper(Scraper):
    def __init__(self, product_url, retriever_creator=None):
        if retriever_creator:
            super(BuyScraper, self).__init__(
                site_name='buy.com',
                url=product_url,
                retriever_creator=retriever_creator)
        else:
            super(BuyScraper, self).__init__(
                site_name='buy.com',
                url=product_url)
