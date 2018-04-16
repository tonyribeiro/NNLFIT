from __future__ import print_function
import sys
import random

#-----------------------
# Stderr print function
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)
#-----------------------

#-----------------------
# Return a vector that gives for each variable the possible values concluded by the matching rules
def match(variables, state, rules):

	output = []

	for var in variables:
		output.append([])

	for rule in rules: # Check all rules
		#eprint("Check matching of ",rule.to_string(),"on",state)
		if rule.matches(state): # Matching conditions
			if rule.head_value not in output[rule.head_variable]: # New value
				output[rule.head_variable].append(rule.head_value)
	
	return output
#-----------------------

#-----------------------
# Generate a given number of transitions
def generate_transitions(variables, variables_values, rules, semantic, nb_transitions):

	for transition in range(0, nb_transitions):
	
		# Generate random initial state
		state = []
	
		for var in range(0, len(variables)):
			state.append(random.randint(0,1))
		
		# Print initial state
		for var in range(0,len(state)):
			print(variables[var]+"="+str(state[var])+" ", end='')
	
		print(": ", end='')

		# Extract matching rules
		matching = match(variables,state,rules)
	
		# DBG
		eprint(matching)

		# SYNCHRONOUS semantics: all variables updates
		if semantic == "synchronous":
			for var in range(0,len(matching)):
				if len(matching[var]) == 0:
					eprint("No rule match for variable \""+str(variables[var])+"\" for state",state)
					sys.exit()
				print(variables[var]+"="+str(matching[var][0])+" ", end='')
			
		# ASYNCHRONOUS semantics: only one variable can update in next state
		if semantic == "asynchronous":
			
			# Copy current state
			next_state = list(state)
			
			# check point attractor (dead end)
			dead_end = True
			
			for values in matching:
				if len(values) > 0: # At least one transition
					dead_end = False
					break
			
			if dead_end == False:
				
				no_matching = True
				var = 0
				
				while no_matching:
					# Pick a random variable that update
					var = random.randint(0,len(matching)-1)
					
					if len(matching[var]) > 0:
						no_matching = False
		
				#DBG
				eprint("Changing variable",variables[var])
		
				# Pick a random value
				val = random.choice(matching[var])
		
				next_state = list(state)
				next_state[var] = val
			
			# Print next state
			for v in range(0,len(next_state)):
				print(variables[v]+"="+str(next_state[v])+" ", end='')
				
		# GENERAL semantics: any number of variable can update in next state
		if semantic == "general":
			
			# explicit matching
			for var in range(0,len(matching)):
				matching[var] = [var,matching[var]]
		
			combinations = subsets(matching)
			# Remove emptyset
			combinations.pop(0)
			eprint(combinations)
			
			combi = random.choice(combinations)
			generate_transition(variables, state, combi)
			
		print()
	return


#-----------------------
# Generate all initial state
def generate_all_transitions(variables, variables_values, rules, var, state, semantic):

	eprint("Current state: ",state)

	# State fully initialized
	if var >= len(variables):
		matching = match(variables,state,rules)
		
		eprint(matching)
		
		# SYNCHRONOUS semantics: only one next state
		if semantic == "synchronous":
			for var in range(0,len(state)):
				print(variables[var]+"="+str(state[var])+" ", end='')
		
			print(": ", end='')
		
			for var in range(0,len(matching)):
				if len(matching[var]) == 0:
					eprint("No rule match for variable \""+str(variables[var])+"\" for state",state)
					sys.exit()
				print(variables[var]+"="+str(matching[var][0])+" ", end='')
		
			print()
		
			return
		
		# ASYNCHRONOUS semantics: only one variable can update in next state
		if semantic == "asynchronous":
		
			# Generate one transition for each variable...
			for var in range(0,len(matching)):
				eprint("Changing variable",variables[var])
				for val in matching[var]: # ...for each value it can takes
				
					# Print current state
					for v in range(0,len(state)):
						print(variables[v]+"="+str(state[v])+" ", end='')
					print(": ", end='')
					
					next_state = list(state)
					next_state[var] = val
					
					# Print next state
					for v in range(0,len(next_state)):
						print(variables[v]+"="+str(next_state[v])+" ", end='')
					print()
		
			print()
		
			return
			
		# GENERAL semantics: any number of variable can update in next state
		if semantic == "general":
		
			# explicit matching
			for var in range(0,len(matching)):
				matching[var] = [var,matching[var]]
		
			combinations = subsets(matching)
			eprint(combinations)
			
			for combi in combinations:
				# Print current state
				for v in range(0,len(state)):
					print(variables[v]+"="+str(state[v])+" ", end='')
				print(": ", end='')
				
				generate_transition(variables, state, combi)
				print()
			
			print()
		
			return
		

	for val in variables_values[var]:
		state.append(val)
	
		# continue state initialization
		generate_all_transitions(variables, variables_values, rules, var+1, state,semantic) 
		
		state.pop()
		
	return
#-----------------------

def generate_transition(variables, state, combi):
	
	eprint("Generating the next state for the combination:",combi)
	
	if combi == []:
		return
	
	next_state = list(state)
	
	for i in combi: # TODO: MULTI-VALUE
		var = i[0]
		next_state[var] = i[1][0] 
		
	# Print next state
	for v in range(0,len(next_state)):
		print(variables[v]+"="+str(next_state[v])+" ", end='')
	
	return

def subsets(s):
    sets = []
    for i in range(1 << len(s)):
        subset = [s[bit] for bit in range(len(s)) if is_bit_set(i, bit)]
        sets.append(subset)
    return sets

def is_bit_set(num, bit):
    return num & (1 << bit) > 0

