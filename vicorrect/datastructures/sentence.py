import re
from dateutil.parser import parse

class Sentence():
	s1 = u'ÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚÝàáâãèéêìíòóôõùúýĂăĐđĨĩŨũƠơƯưẠạẢảẤấẦầẨẩẪẫẬậẮắẰằẲẳẴẵẶặẸẹẺẻẼẽẾếỀềỂểỄễỆệỈỉỊịỌọỎỏỐốỒồỔổỖỗỘộỚớỜờỞởỠỡỢợỤụỦủỨứỪừỬửỮữỰựỲỳỴỵỶỷỸỹ'
	s0 = u'AAAAEEEIIOOOOUUYaaaaeeeiioooouuyAaDdIiUuOoUuAaAaAaAaAaAaAaAaAaAaAaAaEeEeEeEeEeEeEeEeIiIiOoOoOoOoOoOoOoOoOoOoOoOoUuUuUuUuUuUuUuYyYyYyYy'
	u = u'ÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚÝĂĐĨŨƠƯẠẢẤẦẨẪẬẮẰẲẴẶẸẺẼẾỀỂỄỆỈỊỌỎỐỒỔỖỘỚỜỞỠỢỤỦỨỪỬỮỰỲỴỶỸ'
	B_C = '^'
	E_C = '$'
	S_C = '\t'
	R_S = '__object__'
	def __init__(self, sentence=''):
		words = sentence.split()
		if len(words) == 0: return 
		self.sentence = ' '.join(words)
		self.replacements = {
			'phone' : {
				'regrex' : [re.compile(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]', re.UNICODE)],
				'replace' : '__phone__'
			},
			'number' : {
				'regrex' : [re.compile(r'[-+]?[.]?[\d]+(?:,\d\d\d)*[\.\,]?\d*(?:[eE][-+]?\d+)?', re.UNICODE)],
				'replace' : '__num__'
			},
			'name' : {
				'regrex' : [re.compile(r'[' + self.u + r'A-Z]+[\w]+,?\s+(?:[' + self.u + r'A-Z][\w]*\s*)*[' + self.u + r'A-Z][\w]+', re.UNICODE),
							re.compile(r'[' + self.u + r'A-Z]{3,5}', re.UNICODE)],
				'replace' : '__name__'
			},
			'measure' : {
				'regrex' : [re.compile(r'[-+]?[.]?[\d]+(?:,\d\d\d)*[\.\,]?\d*(?:[eE][-+]?\d+)?\s?[' + self.s0 + self.s1 + r'a-zA-Z]{2}\s', re.UNICODE),
							re.compile(r'[-+]?[.]?[\d]+(?:,\d\d\d)*[\.\,]?\d*(?:[eE][-+]?\d+)?\s?[' + self.s0 + self.s1 + r'a-zA-Z\%]{1}\s', re.UNICODE)],
				'replace' : '__measure__ '
			},
			'interval' : {
				'regrex' : [re.compile(r'[-+]?[.]?[\d]+(?:,\d\d\d)*[\.\,]?\d*(?:[eE][-+]?\d+)?\s?-[ ]?[-+]?[.]?[\d]+(?:,\d\d\d)*[\.\,]?\d*(?:[eE][-+]?\d+)?', re.UNICODE)],
				'replace' : '__interval__'
			},
			'date'	: {
				'regrex' : [re.compile(r"[\d]{1,2}/[\d]{1,2}(/[\d]{2,4})?", re.UNICODE),
							re.compile(r"[\d]{1,2}-[\d]{1,2}(-[\d]{2,4})?", re.UNICODE)],
				'replace' : '__date__'
			}
		}	
		self.replace_items = ['__phone__', '__num__', '__name__', '__measure__', '__interval__', '__date__']			
	def extract(self, typeName):
		if typeName not in self.replacements: return []
		regrexes = self.replacements[typeName]['regrex']
		lst = []
		s = self.sentence
		for regrex in regrexes:
			lst.extend(re.findall(regrex, s))
			s = re.sub(regrex, '', s)
		return lst
	def extract_continue(self, lst):
		res = []
		s = self.sentence
		for typeName in lst:
			res.extend(self.extract(typeName))
			self.sentence = self.remove(typeName, '')
		self.sentence = s
		return res			
	def extract_n_gram(self, n, sentence, lower=True):
		lst = []
		sentence = sentence.lower()
		words = sentence.split()
		word_size = len(words)
		for i in range(word_size - n + 1):
			lst.append(tuple(words[i : i + n]))
		return lst
	def remove(self, typeName, replace=False):
		if typeName not in self.replacements:
			return self.sentence
		s = self.sentence
		regrexes = self.replacements[typeName]['regrex']
		if replace == False:
			replace = self.replacements[typeName]['replace']
		for regrex in regrexes:
			s = re.sub(regrex, replace, ' ' + s + ' ')
		return s
	def remove_no_replace(self, lst=['phone', 'num', 'measure', 'interval', 'date']):
		for typeName in lst:
			self.sentence = self.remove(typeName)
		return self.sentence
	def remove_continue(self, lst=['phone', 'num', 'measure', 'interval', 'date']):		
		for typeName in lst:
			self.sentence = self.remove(typeName)
		for item in self.replace_items:
			self.sentence = re.sub(r'([^\s]+)('+ item +')([^\s]*)', self.R_S + ' ', self.sentence)
		return self.sentence
	def check_object(self, word):
		return word.startswith('__') and word.endswith('__')
	def remove_no_vietnamese(self, word):
		return re.sub(r'(\d+)|([wjfz]+)', '', word)
	def check_has_accent(self, input_str):
		return (input_str != self.remove_accents(input_str))
	def remove_accents(self):
		input_str = self.sentence
		s = ''
		for c in input_str:
			if c in self.s1:
				s += self.s0[self.s1.index(c)]
			else:
				s += c
		self.sentence = s
		return self.sentence