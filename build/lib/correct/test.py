from machine_learning.hmm import HiddenMakovModel
from model.add_accents import CorrectVietnameseSentence
from datastructures.sentence import Sentence
import pickle

corrector = CorrectVietnameseSentence()
#hmm = HiddenMakovModel(list_ngrams=[2, 3, 4])

#hmm = pickle.load(open('./model/hmm.pickle', 'rb'))

#f = open('./data/VNESEcorpus.txt')
#full_data = f.readlines()[:100]
#n_train = int(0.7 * len(full_data))
#train = full_data[:n_train]
#test = full_data[n_train:n_train + 1]

#corrector.fit(train)

#hmm.set_data(train)

#hmm.fit()

#pickle.dump(hmm, open('./model/hmm.pickle', 'wb'))
'''
res = []
for window in [2, 3, 4, 5, 8]:
	test_set = []
	label_set = []
	for sen in test:
		words = sen.split()
		for i in range(len(words) // window):
			label = ' '.join(words[i * window : (i + 1) * window])
			inp = Sentence().remove_accents(label)
			test_set.append(inp)
			label_set.append(label)
	res.append((window, len(label_set), corrector.score(test_set, label_set, [10])))
for r in res:
	print('window : {0}, len : {1}, acc : {2}'.format(r[0], r[1], r[2]))
'''
while True:
	s = input('Already to test: ')
	print(corrector.predict([s], [10], 2))
