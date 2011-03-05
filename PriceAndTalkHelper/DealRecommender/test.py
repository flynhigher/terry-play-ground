from lxml import etree
import nltk
import ie_process
import deal_process

def ie_preprocess(doc):
	sents = nltk.sent_tokenize(doc)
	sents = [nltk.word_tokenize(sent) for sent in sents]
	return [nltk.pos_tag(sent) for sent in sents]

def main2(path):
	x = etree.parse('dealnews-processed.xml')
	f = open('pos_tag.txt','w')
	for d in x.xpath('//description'):
		for s in ie_preprocess(nltk.clean_html(d.text)):
			f.write(str(s))
			f.write('\n')
		f.write('===============\n')	

def main3(path):
	ie_process.decode(path)
			
def main(path):
	deal_process.regex_test(path)
	
import sys
import os
if __name__ == '__main__':
	pathname = os.path.dirname(sys.argv[0])        
	os.path.abspath(pathname)
	main(os.path.abspath(pathname))