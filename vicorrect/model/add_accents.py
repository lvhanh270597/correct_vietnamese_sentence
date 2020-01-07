import pickle
from vicorrect.machine_learning.hmm import HiddenMarkovModel

class CorrectVietnameseSentence():
	def __init__(self, listNgrams=[2, 3, 4], eta=0.000001, verbose=True):
		self.__listNgrams = listNgrams
		self.__eta = eta
		self.__loaded = False
		self.__verbose = verbose

	def load(self, filePath):
		try:
			self.__model = pickle.load(open(filePath, 'rb'))
			self.__loaded = True
			print("OK!")
		except Exception as E:
			print("Error: %s" % E)
			return None
	
	def __initModel(self):
		self.__model = HiddenMarkovModel(self.__listNgrams, self.__eta, self.__verbose)

	def fit(self, data):
		if self.__loaded: 
			print("Done!")
			return 
		self.__initModel()
		self.__model.setData(data)
		self.__model.fit()
	
	def predict(self, testcase, lim_per_index=[5], output_size=1):
		return self.__model.fastPredict(testcase, lim_per_index, output_size)
	
	def score(self, inp_list, label_list, list_of_indices=[5]):
		return self.__model.score(inp_list, label_list, list_of_indices)