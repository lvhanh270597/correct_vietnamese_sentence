import pickle
from correct.machine_learning.hmm import HiddenMakovModel

class CorrectVietnameseSentence():
	def __init__(self, default=True, list_ngrams=[2, 3, 4], eta=0.000001):
		self.default = default
		self.list_ngrams = list_ngrams
		self.eta = eta
		self.init_model()		
	def init_model(self):
		if self.default == True:
			self.model = pickle.load(open(self.DEFAULT_MODEL_PATH, 'rb'))
		else:
			self.model = HiddenMakovModel(self.list_ngrams, self.eta)
	def fit(self, data):
		if self.default: return
		self.model.set_data(data)
		self.model.fit()
	def predict(self, testcase, lim_per_index=[5], output_size=1):
		return self.model.fast_predict(testcase, lim_per_index, output_size)
	def score(self, inp_list, label_list, list_of_indices=[5]):
		return self.model.score(inp_list, label_list, list_of_indices)