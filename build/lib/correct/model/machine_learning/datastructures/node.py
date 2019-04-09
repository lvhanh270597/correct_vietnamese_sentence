class Node:
    def __init__(self, info=None, finish=False):
        self.info = info
        self.childs = {}
        self.finish = finish
    def add_child(self, key, info=None):
    	child = Node(info)
    	self.childs[key] = child
    	return child
    def get_child(self, key):
    	return self.childs[key]
    def check_exist_child(self, key):
    	return key in self.childs
    def set_finish(self):
    	self.finish = True
    def get_all_childs(self):
    	return list(self.childs.items())    