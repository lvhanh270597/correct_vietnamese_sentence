
from datastructures.node import Node

class Trie:
    def __init__(self, words=[], start=1):
        self.root = {}
        self.cnt = 0
        for word in words:
            if self.insertWord(word, self.cnt + start):
                self.cnt += 1
        print('The trie has been built successfully with %d different words!' % self.cnt)
    def insertWord(self, word, info, overwrite=False):
        if not overwrite and self.exist(word):
            return False
        self.root[word] = info
        return True   
    def searchWord(self, word):        
        if word in self.root:
            return self.root[word]        
        return False
    def exist(self, word):
        return word in self.root
