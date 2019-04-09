from datastructures.sentence import Sentence
from datastructures.phanso import PhanSo
from nltk.tokenize import word_tokenize, sent_tokenize
import time, re

class HiddenMakovModel():
	def __init__(self,  list_ngrams=[2, 3, 4], eta=0.000001):	
		print('Create Hidden Markov Model with ngram =', list_ngrams)
		self.list_ngrams = set(list_ngrams)
		self.list_ngrams.add(1)
		self.maxtime = 0
		self.eta = eta
	def set_data(self, list_paragraphs):
		self.separate_sentences(list_paragraphs)
	def separate_sentences(self, list_paragraphs):
		print('Separating sentence...')
		self.list_sentences = []
		for paragraph in list_paragraphs:
			list_of_sentences = sent_tokenize(paragraph)
			for sentence in list_of_sentences:
				sentence = Sentence(sentence).remove_continue()
				self.list_sentences.append(sentence)
		print(self.list_sentences[:10])
		print('Done!')
	def get_list_sim(self, word):
		if word not in self.simwords:
			word = Sentence(word).remove_continue()	
		if word not in self.simwords:
			word = re.sub(r'(\d+)|([wjfz]+)', '', word)
			word = re.sub(r'([a-z])(r|s|x)', r'\1', word)
		if word not in self.simwords:
			return {self.index[Sentence().R_S]}
		return self.simwords[word]
	def convert_to_indices(self, words):
		lst = []
		for word in words:
			if type(word) == list:
				word = word[0]
			info = self.trie.searchWord(word)
			if info == False:
				info = self.trie.searchWord(Sentence().R_S)
			lst.append(info[0])
		return tuple(lst)
	def max_prop_words(self, words):		
		indices = self.convert_to_indices(words)
		sum_prop = PhanSo(0, 1)
		prop = PhanSo(0, 1)
		for i in sorted(self.check_list):
			if i > len(indices): break
			for tp in [tuple(indices[j : j + i]) for j in range(len(indices) - i + 1)]:				
				prop.add(self.P[i].get(tp))
			prop.multiple(PhanSo(i, 1))
			sum_prop.add(prop)
			prop = PhanSo(0, 1)
		return sum_prop
	def max_prop_indices(self, indices):
		sum_prop, prop = PhanSo(0, 1), PhanSo(0, 1)
		for i in self.list_ngrams - {1}:
			if i > len(indices): break
			for tp in [tuple(indices[j : j + i]) for j in range(len(indices) - i + 1)]:
				count = 0 if tp not in self.prop[i] else self.prop[i][tp]
				prop.add(PhanSo(count, self.cnt[i]))
			prop.multiple(PhanSo(i, 1))
			sum_prop.add(prop)
			prop = PhanSo(0, 1)
		return sum_prop.convert_to_float()
	def max_prop_words_again(self, words):
		word_size = len(words)
		indices = self.convert_to_indices(words)
		F = []
		for i in range(word_size): F.append(PhanSo(0, 1))
		F[0] = self.P[1].get(indices[:1])
		for i in range(1, word_size):			
			for j in range(i - 1, max(-1, i - self.farthus), -1):
				tp = indices[j : i + 1]
				tmp = F[j].instance()
				tmp.multiple(self.P[i - j + 1].get(tp))
				F[i].add(tmp)
		return F[word_size - 1]
	def get_result_continue(self, old_words, words, lim_per_index=[5], output_size=1):				
		lim_per_index += [lim_per_index[-1]] *  (len(words) - len(lim_per_index))
		lim_per_index_prev = [lim_per_index[0]] *  (len(words) - len(lim_per_index)) + lim_per_index
		list_of_sentence_prev = self.get_words_continue_prev(words, lim_per_index_prev)
		list_of_sentences = self.get_words_continue_next(words, lim_per_index)
		res = {}
		for indices in list_of_sentences + list_of_sentence_prev:
			cur = []
			for index in range(len(words)):
				cur_word = self.word[indices[index]]
				if cur_word.startswith('__') and cur_word.endswith('__'):
					cur_word = old_words[index]
				cur.append(cur_word)			
			res[' '.join(cur)] = self.max_prop_indices(indices)
		res = [k for k in sorted(res, key=res.get, reverse=True)]
		if len(res) == 0: res = [' '.join(old_words)]
		return res
	def get_words_continue_next(self, words, lim_per_index):		
		if len(words) == 0: return tuple()
		if len(words) == 1:			
			return tuple([tuple([w]) for w in self.get_list_sim(words[-1])])
		cur_word = words[-1]
		# if has accent then not neccessary to guess
		if cur_word != Sentence().remove_accents(cur_word):
			if cur_word in self.index:
				cur_simwords = {self.index[cur_word]}
			else:
				cur_simwords = {self.index[Sentence().R_S]}
		else:
			cur_simwords = self.get_list_sim(cur_word)
		list_bef_words = self.get_words_continue_next(words[:-1], lim_per_index[:-1])
		list_choices = {}
		for bef_words in list_bef_words:			
			size_bef = len(bef_words)
			prop_next = {}
			for n in self.list_ngrams:				
				if n - 1 > size_bef: continue			
				check_words = bef_words[-n + 1:]
				for word in cur_simwords:
					tp = check_words + tuple([word])
					prop = 0 if tp not in self.prop[n] else self.prop[n][tp] / self.cnt[n]
					if word not in prop_next:
						prop_next[word] = prop
					else:
						prop_next[word] += prop
			cur_choices = [(k, prop_next[k]) for k in sorted(prop_next, key=prop_next.get, reverse=True)]			
			for choice in cur_choices[:lim_per_index[-1]]:
				if choice[1] < self.eta : break
				next_sentence = tuple(bef_words) + choice[:1]			
				list_choices[next_sentence] = self.max_prop_indices(next_sentence)
		res = tuple([k for k in sorted(list_choices, key=list_choices.get, reverse=True)])
		#print([(' '.join([self.word[index] for index in indices]), list_choices[indices]) for indices in res[:lim_per_index[-1]]])
		return res[:lim_per_index[-1]]
	def get_words_continue_prev(self, words, lim_per_index):
		if len(words) == 0: return tuple()
		if len(words) == 1:	
			return tuple([tuple([w]) for w in self.get_list_sim(words[0])])
		cur_word = words[0]
		# if has accent then not neccessary to guess
		if cur_word != Sentence().remove_accents(cur_word):
			if cur_word in self.index:
				cur_simwords = {self.index[cur_word]}
			else:
				cur_simwords = {self.index[Sentence().R_S]}
		else:
			cur_simwords = self.get_list_sim(cur_word)
		list_next_words = self.get_words_continue_prev(words[1:], lim_per_index[1:])		
		list_choices = {}
		for next_words in list_next_words:			
			size_next = len(next_words)
			prop_prev = {}
			for n in self.list_ngrams:			
				if n - 1 > size_next: continue			
				check_words = next_words[: n - 1]
				for word in cur_simwords:
					tp = tuple([word]) + check_words
					prop = 0 if tp not in self.prop[n] else self.prop[n][tp] / self.cnt[n]
					if word not in prop_prev:
						prop_prev[word] = prop
					else:
						prop_prev[word] += prop
			cur_choices = [(k, prop_prev[k]) for k in sorted(prop_prev, key=prop_prev.get, reverse=True)]			
			for choice in cur_choices[:lim_per_index[0]]:
				if choice[1] < self.eta : break
				prev_sentence = choice[:1] + tuple(next_words)				
				prop = self.max_prop_indices(prev_sentence)				
				list_choices[prev_sentence] = prop
		res = tuple([k for k in sorted(list_choices, key=list_choices.get, reverse=True)])
		#print([(' '.join([self.word[index] for index in indices]), list_choices[indices]) for indices in res[:lim_per_index[-1]]])
		return res[:lim_per_index[0]]	
	def fast_predict(self, testdata, list_of_indices=[10], output_size=5):
		print('Predicting...')
		y = []
		for sentence in testdata:			
			start = time.time()
			sentence = ' '.join(word_tokenize(sentence))			
			old_words = sentence.split()
			sentence = Sentence(sentence).remove_continue()
			#print(sentence)
			new_words = sentence.split()
			res = self.get_result_continue(old_words, new_words, list_of_indices, output_size)
			end = time.time()
			print('Done %f (ms)' % ((end-start) * 1000))
			self.maxtime = max(self.maxtime, end - start)
			y.append(res)
		print('Done!')
		return y
	def score(self, inp_list, label_list, list_of_indices):
		y_pred = self.fast_predict(inp_list)
		acc = 0
		for i in range(len(label_list)):
			acc += (label_list[i] in y_pred[i])
		return (acc / len(label_list)) * 100
	def fit(self):
		print('Fitting model...')	
		start_time = time.time()
		self.prop = {}
		self.cnt = {}
		self.simwords = {}
		self.word = {}
		self.index = {}
		for i in self.list_ngrams:
			self.prop[i] = {}
			self.cnt[i] = 0
		print('Extract n-gram ', self.list_ngrams)
		cnt, full_size = 1, len(self.list_sentences)
		for sentence in self.list_sentences:
			print('Processing at %d/%d (%.2f)' %(cnt, full_size, (cnt / full_size) * 100))
			list_indices = []
			words = word_tokenize(sentence)
			for word in words:
				if word not in self.index:					
					self.index[word] = len(self.word) + 1
				index = self.index[word]
				self.word[index] = word
				# build prop
				list_indices.append(index)
				for ngram in self.list_ngrams:
					if ngram > len(list_indices): continue
					word_encodes = tuple(list_indices[-ngram:])					
					if word_encodes not in self.prop[ngram]:
						self.prop[ngram][word_encodes] = 1
					else:
						self.prop[ngram][word_encodes] += 1
				# inscrease cnt 
			for ngram in self.list_ngrams:
				self.cnt[ngram] += max(0, len(words) - ngram + 1)
			cnt += 1	
		################# add __object__ #####################
		R_S = Sentence().R_S
		if R_S not in self.index:
			index = len(self.index) + 1
			self.index[R_S] = index
			self.word[index] = R_S
			self.prop[1][index] = 0			
		######################################################		
		print('Done!')		
		print('Extract similar non-accent words')		
		cnt, full_size = 1, len(self.index)
		# build sim words
		for word in self.index:
			print('Processing at %d/%d (%.2f)' %(cnt, full_size, (cnt / full_size) * 100))
			index = self.index[word]
			non_accent = Sentence().remove_accents(word)
			if non_accent not in self.simwords:
				self.simwords[non_accent] = {index}
			else:
				self.simwords[non_accent].add(index)
			cnt += 1
		print('Done!')
		end_time = time.time()
		print('Finished! Ellapse time: %f (ms)' %((end_time - start_time) * 1000))