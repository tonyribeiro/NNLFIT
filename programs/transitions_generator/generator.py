#-----------------------
# @author: Tony Ribeiro
# @created: 2018/03/10
# @updated: 2018/03/10
#
# Boolean Network Time Series Generator
# 
#-----------------------

from __future__ import print_function
import sys
import random

import rule
from utils import eprint, generate_all_transitions, generate_transitions

random.seed(a=None)

# 0) Parameters management
#--------------------------

eprint("Starting Boolean Network Transition Generator...")
eprint("> Parameter extraction")

#******************
# parameters      *
#
input_file = "" 	# $1
semantic = ""		# $2
nb_transitions = 0	# $3
#                 *
#******************

param_id = 1

if len(sys.argv) < 2:
	eprint(">> No input file specified, script terminated")
	sys.exit()

input_file = sys.argv[param_id]
eprint(">> Input file specified: ",input_file)
param_id+=1

if len(sys.argv) > param_id:
	semantic = sys.argv[param_id]
	eprint(">> Semantic given: ",semantic)
	
	if semantic != "synchronous" and semantic != "asynchronous" and semantic != "general":
		eprint(">>> Bad value for semantic parameter, must be one of the following: synchronous, asynchronous, general")
	
else:
	eprint(">> No semantic specified, script terminated")
	sys.exit()
	
param_id+=1

if len(sys.argv) > param_id:
	nb_transitions = int(sys.argv[param_id])
	eprint(">> Number of nb_transitions given: ",nb_transitions)
else:
	eprint(">> No specific number of tranitions requested, all transitions will be generated")

eprint ("> Input file extraction...")

# 1) Extract variables
#------------------------

eprint (">> Extracting variables...")

variables = []
variables_values = []
f = open(input_file,"r")

for line in f:
	tokens = line.split()

	if len(tokens) == 0 or tokens[0] != "VAR":
		break
	
	variable = tokens[1]
	values = []
	
	for i in range(2,len(tokens)):
		values.append(tokens[i])
	
	eprint(">>> Extracted variable:",variable,"domain:",values)
	
	variables.append(variable)
	variables_values.append(values)


# 2) Extract rules
#------------------------

rules = []

for line in f:
	tokens = line.split()

	if len(tokens) == 0:
		continue

	head = tokens[0]
	
	# Extract variable
	beg = 0
	end = head.index('(')
	
	head_variable = head[beg:end]
	head_var_id = variables.index(head_variable)
	
	# Extract value
	beg = end+1
	end = head.index(',')
	
	head_value = head[beg:end]
	head_val_id = variables_values[head_var_id].index(head_value)
	
	eprint("Head extracted: ",head_var_id,"=",head_val_id)
		
		
	# Extract body
	body = []
	
	for i in range(2,len(tokens)):
		condition = tokens[i]
		
		# Extract variable
		beg = 0
		end = condition.index('(')
	
		variable = condition[beg:end]
		var_id = variables.index(variable)
	
		# Extract value
		beg = end+1
		end = condition.index(',')
	
		value = condition[beg:end]
		val_id = variables_values[var_id].index(value)
	
		# TODO: delay
	
		#eprint("Condition extracted: ",variable,"=",value)
		
		body.append([var_id,val_id,1])
		
	r = rule.Rule(head_var_id,head_val_id,body)
	rules.append(r)
	
	eprint("Extracted rule:",r.to_string())

# 3) Time series generation
#---------------------------

eprint ("Generating time series...")

# Print variables
for var in range(0,len(variables)):
	print ("VAR "+variables[var],end='')
	for val in variables_values[var]:
		print(" "+val,end='')
	print()
print()

# Generate all transitions
if nb_transitions == 0:
	initial_state = []

	generate_all_transitions(variables, variables_values, rules, 0, initial_state, semantic)
else:	
# Generate given number of transitions:
	generate_transitions(variables, variables_values, rules, semantic, nb_transitions)
	

#############
# OUTPUT:
# - serie
# - serie_noise
#############

print()


