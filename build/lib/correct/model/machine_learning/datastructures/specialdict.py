class SpecialDict():
	def __init__(self):
		self.d = dict()
	def add(self, key, value=1):
		if key not in self.d:			
			self.d[key] = value
			return True
		else:
			self.d[key] += value
		return False	
	def set(self, key, value=0):
		self.d[key] = value
	def len(self):
		return len(self.d)
	def get(self, key):
		if key not in self.d:
			return PhanSo(0, 1)
		return self.d[key]
	def keys(self):
		return self.d.keys()
