#!/usr/bin/env python
import sys

from subprocess import call
from os import putenv

class LastSavedId():
	def __init__(self, filename):
		self.__filename = filename
		self.last_id = None		
		try:
			f = open(self.__filename)
			self.last_id = f.read()
			f.close()
		except:
			pass

	def save_last_id(self, id):
		self.last_id = None
		f = open(self.__filename, 'w')
		f.write(id)
		f.close()

if __name__ == "__main__" :
	putenv('DJANGO_SETTINGS_MODULE', 'settings')
	counter = 0
	while 1:
		call([sys.argv[1], sys.argv[2]])
		counter += 1
		last_browse_id = LastSavedId('last_browse_id.txt')
		if not last_browse_id.last_id or counter > 10000:
			break

