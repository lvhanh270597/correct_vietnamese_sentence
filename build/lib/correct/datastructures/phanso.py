import math
class PhanSo():
	def __init__(self, a, b):
		self.a = a // math.gcd(a, b)
		self.b = b // math.gcd(a, b)
	def add(self, x):
		ta = self.a * x.b + self.b * x.a
		tb = self.b * x.b
		gcd = math.gcd(ta, tb)
		self.a = ta // gcd
		self.b = tb // gcd
	def multiple(self, x):
		ta = self.a * x.a
		tb = self.b * x.b
		gcd = math.gcd(ta, tb)
		self.a = ta // gcd
		self.b = tb // gcd
	def instance(self):
		return PhanSo(self.a, self.b)
	def compare(self, x):
		c = self.a * x.b - x.a * self.b
		if c > 0: c = 1
		if c < 0: c = -1
		return c
	def convert_to_float(self):
		return self.a / self.b

