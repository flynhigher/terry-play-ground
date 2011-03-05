import re, os
#import sys

class DealParser:
	def __init__(self, work_path):
		self.__init_price_patterns(os.path.join(work_path, 'regexpattern.txt'))
		self.__init_noword_patterns(os.path.join(work_path, 'nowordpattern.txt'))
		self.round_threshhold = 0.3
		
	def get_price(self, text):
		match = self.__get_price_match(text)
		price = '$0'
		if match:
			try:
				price = match.groups(0)[0]
			except:
				pass
#				sys.stdout.write('price error: ' + text + ', ' +  match.group() + '\n')
		return price
	
	def extract_keywords(self, text):
		for p, r in zip(self.replace_patterns, self.replace_with):
			text = p.sub(r, text)
		words = text.lower().split(' ')
		words = [self.__process_word(w) for w in words if w]
		words = [w for w in words if w]
		keywords = []
		for w in words:
			if w not in keywords:
				keywords.append(w)
				after_words = self.__process_word_after(w)
				keywords = keywords + [w for w in after_words if w and w not in keywords]
						
		return keywords
	
	def get_adjusted_price(self, price):
		p = price[1:].replace(',', '')
		f = float(p)
		r = round(f)
		if abs(r - f) < self.round_threshhold:
			return r
		else:
			return f
	
	def __get_price_match(self, text):
		for p in self.price_patterns:
			m = p.search(text)
	#		sys.stdout.write(p.pattern + ' : ' + text + ' -> ' + (m.group() if m else 'not match') + '\n')
			if m:
				return m
		return None
				
	def __process_word(self, w):
		w = w.strip()
		if not w:
			return None
		for p in self.delete_patterns:
			if p.search(w):
				return None
		if w in self.delete_words:
			return None
		return w
	
	def __process_word_after(self, w):
		words = []
		split = None
		if len(self.split_patterns) > 0:
			split = self.split_patterns[0].split(w)
		if split and len(split) > 0:
			words = split
		for p, r in zip(self.replace_after_patterns, self.replace_after_with):
			w = p.sub(r, w)
		words = words + w.split(' ')
		return [w for w in words if w]
	
	def __init_noword_patterns(self, filepath):
		pfile = open(filepath)
		self.replace_patterns = []
		self.replace_with = []
		self.delete_words = []
		self.delete_patterns = []
		self.split_patterns = []
		self.replace_after_patterns = []
		self.replace_after_with = []
		for line in pfile:
			split = line.replace('\r','').replace('\n','').split(':::')
			p = re.compile(split[1], re.IGNORECASE)
			if split[0] == 'delete':
				self.delete_words.append(split[1])
			elif split[0] == 'deleter':
				self.delete_patterns.append(p)
			elif split[0] == 'split':
				self.split_patterns.append(p)
			elif split[0] == 'replace_after':
				self.replace_after_patterns.append(p)
				rr = ''
				if len(split) > 2:
					rr = split[2]
				self.replace_after_with.append(rr)
			else:
				self.replace_patterns.append(p)
				rr = ''
				if len(split) > 2:
					rr = split[2]
				self.replace_with.append(rr)
		pfile.close()
	
	def __init_price_patterns(self, filepath):
		patternfile = open(filepath)
		self.price_patterns = [re.compile(pattern.replace('\r', '').replace('\n', ''), re.IGNORECASE) for pattern in patternfile.readlines()]
		patternfile.close()
