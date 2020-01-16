from vicorrect.datastructures.sentence import Sentence
from vicorrect.datastructures.phanso import PhanSo
from nltk.tokenize import word_tokenize, sent_tokenize
import time, re

class HiddenMarkovModel():
	def __init__(self,  listNgrams=[2, 3, 4], eta=0.000001, verbose=True):
		self.__listNgrams = set(listNgrams)
		self.__listNgrams.add(1)
		self.__maxTime = 0
		self.__eta = eta
		self.__verbose = verbose
		if self.__verbose:
			print('Created Hidden Markov Model with ngram =', listNgrams)
	def setData(self, listParagraphs):
		if self.__verbose:
			print('Separating sentence...')
		self.__listSentences = []
		for paragraph in listParagraphs:
			listOfSentences = sent_tokenize(paragraph)
			for sentence in listOfSentences:
				sentence = Sentence(sentence).remove_continue()
				self.__listSentences.append(sentence)
		if self.__verbose:
			print(self.__listSentences[:10])
		if self.__verbose:
			print('Done!')
	def __getListSim(self, word):
		if word not in self.__simwords:
			word = Sentence(word).remove_continue()	
		if word not in self.__simwords:
			word = re.sub(r'(\d+)|([wjfz]+)', '', word)
			word = re.sub(r'([a-z])(r|s|x)', r'\1', word)
		if word not in self.__simwords:
			return {self.__index[Sentence().R_S]}
		return self.__simwords[word]
	def __maxPropIndices(self, indices):
		sum_prop, prop = PhanSo(0, 1), PhanSo(0, 1)
		for i in self.__listNgrams - {1}:
			if i > len(indices): break
			for tp in [tuple(indices[j : j + i]) for j in range(len(indices) - i + 1)]:
				count = 0 if tp not in self.__prop[i] else self.__prop[i][tp]
				prop.add(PhanSo(count, self.__cnt[i]))
			prop.multiple(PhanSo(i, 1))
			sum_prop.add(prop)
			prop = PhanSo(0, 1)
		return sum_prop.convert_to_float()
	def __getResultContinue(self, old_words, words, lim_per_index=[5], output_size=1):				
		lim_per_index += [lim_per_index[-1]] *  (len(words) - len(lim_per_index))
		lim_per_index_prev = [lim_per_index[0]] *  (len(words) - len(lim_per_index)) + lim_per_index
		list_of_sentence_prev = self.__getWordsContinuePrev(words, lim_per_index_prev)
		list_of_sentences = self.__getWordsContinueNext(words, lim_per_index)
		res = {}
		for indices in list_of_sentences + list_of_sentence_prev:
			cur = []
			for index in range(len(words)):
				cur_word = self.__word[indices[index]]
				if cur_word.startswith('__') and cur_word.endswith('__'):
					cur_word = old_words[index]
				cur.append(cur_word)			
			res[' '.join(cur)] = self.__maxPropIndices(indices)
		res = [k for k in sorted(res, key=res.get, reverse=True)]
		if len(res) == 0: res = [' '.join(old_words)]
		return res
	def __getWordsContinueNext(self, words, lim_per_index):		
		if len(words) == 0: return tuple()
		if len(words) == 1:			
			return tuple([tuple([w]) for w in self.__getListSim(words[-1])])
		cur_word = words[-1]
		# if has accent then not neccessary to guess
		if cur_word != Sentence(cur_word).remove_accents():
			if cur_word in self.__index:
				cur_simwords = {self.__index[cur_word]}
			else:
				cur_simwords = {self.__index[Sentence().R_S]}
		else:
			cur_simwords = self.__getListSim(cur_word)
		list_bef_words = self.__getWordsContinueNext(words[:-1], lim_per_index[:-1])
		list_choices = {}
		for bef_words in list_bef_words:			
			size_bef = len(bef_words)
			prop_next = {}
			for n in self.__listNgrams:				
				if n - 1 > size_bef: continue			
				check_words = bef_words[-n + 1:]
				for word in cur_simwords:
					tp = check_words + tuple([word])
					prop = 0 if tp not in self.__prop[n] else self.__prop[n][tp] / self.__cnt[n]
					if word not in prop_next:
						prop_next[word] = prop
					else:
						prop_next[word] += prop
			cur_choices = [(k, prop_next[k]) for k in sorted(prop_next, key=prop_next.get, reverse=True)]			
			for choice in cur_choices[:lim_per_index[-1]]:
				if choice[1] < self.__eta : break
				next_sentence = tuple(bef_words) + choice[:1]			
				list_choices[next_sentence] = self.__maxPropIndices(next_sentence)
		res = tuple([k for k in sorted(list_choices, key=list_choices.get, reverse=True)])
		return res[:lim_per_index[-1]]
	def __getWordsContinuePrev(self, words, lim_per_index):
		if len(words) == 0: return tuple()
		if len(words) == 1:	
			return tuple([tuple([w]) for w in self.__getListSim(words[0])])
		cur_word = words[0]
		# if has accent then not neccessary to guess
		if cur_word != Sentence(cur_word).remove_accents():
			if cur_word in self.index:
				cur_simwords = {self.__index[cur_word]}
			else:
				cur_simwords = {self.index[Sentence().R_S]}
		else:
			cur_simwords = self.__getListSim(cur_word)
		list_next_words = self.__getWordsContinuePrev(words[1:], lim_per_index[1:])		
		list_choices = {}
		for next_words in list_next_words:			
			size_next = len(next_words)
			prop_prev = {}
			for n in self.__listNgrams:			
				if n - 1 > size_next: continue			
				check_words = next_words[: n - 1]
				for word in cur_simwords:
					tp = tuple([word]) + check_words
					prop = 0 if tp not in self.__prop[n] else self.__prop[n][tp] / self.__cnt[n]
					if word not in prop_prev:
						prop_prev[word] = prop
					else:
						prop_prev[word] += prop
			cur_choices = [(k, prop_prev[k]) for k in sorted(prop_prev, key=prop_prev.get, reverse=True)]			
			for choice in cur_choices[:lim_per_index[0]]:
				if choice[1] < self.__eta : break
				prev_sentence = choice[:1] + tuple(next_words)				
				prop = self.__maxPropIndices(prev_sentence)				
				list_choices[prev_sentence] = prop
		res = tuple([k for k in sorted(list_choices, key=list_choices.get, reverse=True)])
		return res[:lim_per_index[0]]	
	def fastPredict(self, testdata, list_of_indices=[10], output_size=5):
		if self.__verbose:
			print('Predicting...')
		y = []
		for sentence in testdata:			
			start = time.time()
			sentence = ' '.join(word_tokenize(sentence))			
			old_words = sentence.split()
			sentence = Sentence(sentence).remove_continue()
			new_words = sentence.split()
			res = self.__getResultContinue(old_words, new_words, list_of_indices, output_size)
			end = time.time()
			if self.__verbose:
				print('Done %f (ms)' % ((end-start) * 1000))
			self.__maxTime = max(self.__maxTime, end - start)
			y.append(res)
		if self.__verbose:
			print('Done!')
		return y
	def score(self, inp_list, label_list, list_of_indices):
		y_pred = self.fastPredict(inp_list)
		acc = 0
		for i in range(len(label_list)):
			acc += (label_list[i] in y_pred[i])
		return (acc / len(label_list)) * 100
	def fit(self):
		if self.__verbose:
			print('Fitting model...')
		start_time = time.time()
		self.__prop, self.__cnt, self.__index = {}, {}, {}
		self.__simwords, self.__word = {}, {}
		for i in self.__listNgrams:
			self.__prop[i] = {}
			self.__cnt[i] = 0
		if self.__verbose:
			print('Extract n-gram ', self.__listNgrams)
		cnt, full_size = 1, len(self.__listSentences)
		for sentence in self.__listSentences:
			if self.__verbose:
				print('Processing at %d/%d (%.2f%%)' %(cnt, full_size, (cnt / full_size) * 100))
			listIndices = []
			words = word_tokenize(sentence)
			for word in words:
				if word not in self.__index:
					self.__index[word] = len(self.__word) + 1
				index = self.__index[word]
				self.__word[index] = word
				# build prop
				listIndices.append(index)
				for ngram in self.__listNgrams:
					if ngram > len(listIndices): continue
					word_encodes = tuple(listIndices[-ngram:])					
					if word_encodes not in self.__prop[ngram]:
						self.__prop[ngram][word_encodes] = 1
					else:
						self.__prop[ngram][word_encodes] += 1
				# inscrease cnt 
			for ngram in self.__listNgrams:
				self.__cnt[ngram] += max(0, len(words) - ngram + 1)
			cnt += 1
		################# add __object__ #####################
		R_S = Sentence().R_S
		if R_S not in self.__index:
			index = len(self.__index) + 1
			self.__index[R_S] = index
			self.__word[index] = R_S
			self.__prop[1][index] = 0			
		######################################################		
		if self.__verbose:
			print('Done!')	
		if self.__verbose:
			print('Extract similar non-accent words')		
		cnt, full_size = 1, len(self.__index)
		# build sim words
		for word in self.__index:
			if self.__verbose:
				print('Processing at %d/%d (%.2f)' %(cnt, full_size, (cnt / full_size) * 100))
			index = self.__index[word]
			non_accent = Sentence(word).remove_accents()
			if non_accent not in self.__simwords:
				self.__simwords[non_accent] = {index}
			else:
				self.__simwords[non_accent].add(index)
			cnt += 1
		if self.__verbose:
			print('Done!')
		end_time = time.time()
		if self.__verbose:
			print('Finished! Ellapse time: %f (ms)' %((end_time - start_time) * 1000))