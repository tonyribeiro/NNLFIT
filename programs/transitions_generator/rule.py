class Rule:
	""" Represent a logic program rule """
	
	head_variable = 0
	
	head_value = 0
	
	body = []
	
	# Empty rule
	def __init__(self,head_variable,head_value):
		self.head_variable = head_variable
		self.head_value = head_value
		self.body = []
	
	# Full body initialization
	def __init__(self,head_variable,head_value,body):
		self.head_variable = head_variable
		self.head_value = head_value
		self.body = body
		
	def to_string(self):
		output = str(self.head_variable) + "(" + str(self.head_value) + ",T) :- "
		for var,val,delay in self.body:
			output += str(var) + "(" + str(val) + ",T-" + str(delay) + "), "
		
		output = output[:len(output)-2] + "."
		return output
		
	def matches(self,state):
		for var,val,delay in self.body:
			if val != int(state[var]):
				return False
		return True
