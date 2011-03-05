def do_post():
	import sys
	import logging
	import urllib2
	sys.stderr = open("E:\\Project\\KoreanProductOnAmazon\\amazonKorea.log", "w+")
	f = open("E:\\Project\\KoreanProductOnAmazon\\amazonKorea.txt")

	for asin in f:
		asin = asin.replace("\n", "")
		try:
			urllib2.urlopen("http://localhost:8000/product/ptpost/4/" + asin + "/")
			print asin + " done!"
		except Exception, ex:
			logging.exception("Exception: " + asin)
	f.close()
	sys.stderr.close()

if __name__ == "__main__" :
  do_post()