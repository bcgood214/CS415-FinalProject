import random, primitives

class Node:
	def __init__(self):
		self.target = None
		self.left = None
		self.right = None
	
	def print_tree(self, level = 0):
		print("At level {}: {}".format(level, self.target))
		if self.right:
			self.right.print_tree(level + 1)
		if self.left:
			self.left.print_tree(level + 1)
	
	def run(self):
		if type(self.target) == float:
			return self.target
		
		return self.target(self.left.run(), self.right.run())

def gen_val():
	return random.random()

func_set = [primitives.add, primitives.sub, primitives.mult, primitives.div]
term_set = [gen_val]
prim_set = func_set + term_set

def copy_ind(old):
	new = Node()
	
	new.target = old.target
	if old.right:
		new.right = copy_ind(old.right)
	if old.left:
		new.left = copy_ind(old.left)
	
	return new

def gen_ind(n, depth = 3, no_term = False):
	choice = None
	if depth == 0:
		choice = gen_val
	elif no_term:
		choice = random.choice(func_set)
	else:
		choice = random.choice(prim_set)
	
	
	n.target = choice
	if choice in func_set:
		n.left = Node()
		n.left = gen_ind(n.left, depth = depth-1)
		n.right = Node()
		n.right = gen_ind(n.right, depth = depth-1)
	else:
		n.target = choice()
	
	return n

def find_depth(node, depth=1):
	max = 0

	# if not isinstance(node, Node):
	#     print("Wasn't a Node")
	#     return depth
	
	if node.left is None and node.right is None:
		return depth
	if node.left:
		max = find_depth(node.left, depth=depth+1)
	if node.right:
		right_depth = find_depth(node.right, depth=depth+1)
		if right_depth > max:
			max = right_depth
	
	return max


def select_sub(node, terminal=True):
	d = find_depth(node)
	if not terminal and d == 2:
		return node

	prob = 1/d

	if random.random() < prob:
		return node
	
	if random.random() > 0.5 and node.left:
		return select_sub(node.left, terminal=terminal)
	elif node.right:
		return select_sub(node.right, terminal=terminal)

	return select_sub(node.left, terminal=terminal)

def recombine(p1, p2):
	child = copy_ind(p1)
	sub = select_sub(child, terminal=False)
	new_sub = copy_ind(select_sub(p2))

	if random.random() < 0.5:
		sub.right = new_sub
	else:
		sub.left = new_sub
	
	return child

if __name__ == "__main__":
	p1 = gen_ind(Node(), no_term=True)
	p2 = gen_ind(Node(), no_term=True)
	child = recombine(p1, p2)
	print(child.run())
