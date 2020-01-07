from datastructures.node import Node

class PrefixTree():
	def __init__(self):
		self.root = Node()		
	def insertListWord(self, list_words, info):
		p = self.root
		for word in list_words:
			if not p.check_exist_child(word):
				p.add_child(word)
			p = p.get_child(word)
		p.set_finish()
		p.info = info
	def get_next(self, list_words, step):
		p = self.root
		for word in list_words:			
			if not p.check_exist_child(word):
				return []
			p = p.get_child(word)
		list_nodes = [p.get_all_childs()]			
		for level in range(1, step):			
			for parent in list_nodes[-1]:
				list_nodes.append(parent.get_all_childs())
		res = []
		for (word, node) in list_nodes[-1]:
			if node.finish:
				res.append((word, node.info))
		return res