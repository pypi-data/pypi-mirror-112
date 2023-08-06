import json
import re



standard_elements = {
	'NOT': 		{'inputs': 1, 'outputs': 1},
	'AND': 		{'inputs': 2, 'outputs': 1},
	'OR': 		{'inputs': 2, 'outputs': 1},
	'INPUT': 	{'inputs': 0, 'outputs': 1},
	'OUTPUT': 	{'inputs': 1, 'outputs': 0}
}


def getElementType(element):
	return '_'.join(element.split('_')[:-1])


def getElementName(element_input_or_output):
	return element_input_or_output.split('[')[0]


def getInputOutputIndex(element_input_or_output):
	return element_input_or_output[:-1].split('[')[1]


def getElementsTypes(description):

	result = {}

	for e in sum([[w['from'], w['to']] for w in description['wires']], []):
		element_type = getElementType(e)
		result[element_type] = None

	return result.keys()

def getElementsNumbers(description):

	result = {}

	for e in sum([[w['from'], w['to']] for w in description['wires']], []):
		
		element_name = getElementName(e)
		element_type = getElementType(e)
		
		if not element_type in result:
			result[element_type] = {}
		
		result[element_type][element_name] = None

	return {key: len(value.keys()) for key, value in result.items()}


def getInputsOutputsNumbersForType(description):

	elements_numbers = getElementsNumbers(description)

	return {
		'inputs': 0 if not ('INPUT' in elements_numbers) else elements_numbers['INPUT'],
		'outputs': 0 if not ('OUTPUT' in elements_numbers) else elements_numbers['OUTPUT']
	}

def getInputsOutputsNumbersForInnerElements(description):

	result = {}

	for w in description['wires']:
		
		from_element = getElementName(w['from'])
		if not from_element in result:
			result[from_element] = {'inputs': 0, 'outputs': 0}
		result[from_element]['outputs'] += 1
		
		to_element = getElementName(w['to'])
		if not to_element in result:
			result[to_element] = {'inputs': 0, 'outputs': 0}
		result[to_element]['inputs'] += 1

	return result

def getElementsInputs(description):

	result = {}

	for w in description['wires']:

		element = getElementName(w['to'])
		if not (element in result):
			result[element] = {}
		input_index = getInputOutputIndex(w['to'])

		try:
			result[element][int(input_index)] = w['from']
		except ValueError:
			result[element][1] = w['from']

	return result


def getExpression(inputs_by_element, element_input_or_output, non_standard_elements_expressions):

	e_type = getElementType(element_input_or_output)
	e_name = getElementName(element_input_or_output)
	if e_type == 'INPUT':
		return e_name

	getExpression_local = lambda v: getExpression(inputs_by_element, v, non_standard_elements_expressions)
	e_inputs = inputs_by_element[e_name]

	if e_type in standard_elements:

		if e_type == 'OUTPUT':
			return getExpression_local(e_inputs[1])

		elif e_type == 'NOT':
			return f'!{getExpression_local(e_inputs[1])}'

		elif e_type == 'OR':
			return f'({" || ".join(map(getExpression_local, e_inputs.values()))})'

		elif e_type == 'AND':
			return f'({" && ".join(map(getExpression_local, e_inputs.values()))})'

	else:

		e_info = non_standard_elements_expressions[e_type]
		e_index = getInputOutputIndex(element_input_or_output)
		expression = e_info['expressions'][int(e_index) - 1]

		inputs_expressions = [getExpression_local(v) for v in e_inputs.values()]
		
		inputs_dict = {
			f'INPUT_{i+1}': inputs_expressions[i]
			for i in range(e_info['inputs_number'])
		}

		return expression.format(**inputs_dict)

def getOutputsExpressions(inputs_by_element, non_standard_elements_expressions):
	
	result = {}

	for key in inputs_by_element.keys():
		if getElementType(key) == 'OUTPUT':
			result[getElementName(key)] = getExpression(inputs_by_element, key, non_standard_elements_expressions)

	return [result[k] for k in sorted(result.keys())]


find_inputs = re.compile(r'INPUT(_\d+)')

def defineFunction(name, description, non_standard_elements_expressions, is_target):

	elements_numbers = getElementsNumbers(description)

	inputs_number = elements_numbers['INPUT']
	outputs_number = elements_numbers['OUTPUT']

	inputs_by_element = getElementsInputs(description)
	outputs_expressions = getOutputsExpressions(inputs_by_element, non_standard_elements_expressions)
	
	inputs_string = ", ".join([f"int INPUT_{i+1}" for i in range(inputs_number)])

	if is_target:

		result  = f'int* {name}({inputs_string}) {{\n'
		result += f'\tint *result = malloc(sizeof(int) * {outputs_number});\n'

		for i in range(len(outputs_expressions)):
			result += f'\tresult[{i}] = {outputs_expressions[i]};\n'

		result += '\treturn result;\n'
		result += '}'

		return result

	else:

		non_standard_elements_expressions[name] = {
			'inputs_number': inputs_number,
			'expressions': [find_inputs.sub(r'{INPUT\1}', e) for e in outputs_expressions]
		}



def checkNoCycles(current_from, from_to, stack=[]):

	if current_from in stack:
		return False, f'Cycle: {stack + [current_from]}'

	if not (current_from in from_to):
		return True, None

	for _to in from_to[current_from]:
		c = checkNoCycles(_to, from_to, stack = stack + [current_from])
		if not c[0]:
			return False, c[1]

	return True, None

def checkFunctionNoCycles(description):

	from_to = {}

	for w in description['wires']:

		from_element = getElementName(w['from'])
		to_element = getElementName(w['to'])

		if not from_element in from_to:
			from_to[from_element] = []
		from_to[from_element].append(to_element)
	
	inputs = [e for e in from_to if getElementType(e) == 'INPUT']
	for initial_from in inputs:
		c = checkNoCycles(initial_from, from_to)
		if not c[0]:
			return False, c[1]

	return True, None

def checkFunction(description, checks=[checkFunctionNoCycles]):

	for c in checks:
		c_result = c(description)
		if not c_result[0]:
			return False, c_result[1]

	return True, None



def checkProgramRequirements(program):

	defined_elements = {**program, **standard_elements}.keys()

	for name, description in program.items():

		elements = getElementsTypes(description)

		for e in elements:
			if not (e in defined_elements):
				return False, f'Function {name}: Element not declared: {e}'

	return True, None

def checkProgramInputsOutputs(program):

	defined_elements = {**program, **standard_elements}.keys()
	non_standard_elements = {}

	for name, description in program.items():

		inputs_outputs_for_type = getInputsOutputsNumbersForType(description)
		non_standard_elements[name] = inputs_outputs_for_type

		if 'tests' in description:

			for t in description['tests']:

				for key in ['inputs', 'outputs']:

					have = len(t[key])
					should_have = inputs_outputs_for_type[key]
					if have != should_have:
						return False, f'Function {name}: Test {t}: {key} number does not match: have {have}, should have {should_have}'

			if inputs_outputs_for_type['inputs'] == 0:
				return False, f'Function {name}: 0 inputs'

			if inputs_outputs_for_type['outputs'] == 0:
				return False, f'Function {name}: 0 outputs'
	
	elements_types_inputs_outputs = {
		**standard_elements,
		**non_standard_elements
	}
	
	for f_name, description in program.items():

		elements_inputs_outputs = getInputsOutputsNumbersForInnerElements(description)

		for e_name, value in elements_inputs_outputs.items():

			e_type = getElementType(e_name)

			have = elements_inputs_outputs[e_name]
			have['outputs'] = bool(have['outputs'])

			should_have = elements_types_inputs_outputs[e_type]
			should_have['outputs'] = bool(should_have['outputs'])

			if have != should_have:
				return False, f'Function {f_name}: Element {e_name}: inputs/outputs do not match: have {have}, should have {should_have}'
	
	return True, None

def checkProgram(program, checks=[checkProgramRequirements, checkProgramInputsOutputs]):

	for c in checks:
		c_result = c(program)
		if not c_result[0]:
			return False, c_result[1]

	return True, None



def compile(program, target, requirements):

	check_program_result = checkProgram(program)
	if not check_program_result[0]:
		raise Exception(f'Program not correct: {check_program_result[1]}')

	non_standard_elements_expressions = {}

	for name in requirements:

		description = program[name]

		check_function_result = checkFunction(description)
		if not check_function_result[0]:
			raise Exception(f'Function "{name}" not correct: {check_function_result[1]}')

		defineFunction(name, description, non_standard_elements_expressions, is_target=False)

	definition = defineFunction(target, program[target], non_standard_elements_expressions, True)

	result  = '#include <stdio.h>\n'
	result += '#include <stdlib.h>\n'
	result += '\n'
	result += definition + '\n'
	result += '\n'
	result += 'void printArray(int *a, int length, const char *delimiter) {\n'
	result += '\tint i;\n'
	result += '\tprintf("%d", a[0]);\n'
	result += '\tfor (i = 1; i < length; i++)\n'
	result += '\t\tprintf("%s%d", delimiter, a[i]);\n'
	result += '}\n'
	result += '\n'
	result += 'int isEqual(int *a, int *b, int length) {\n'
	result += '\tint i;\n'
	result += '\tfor (i = 0; i < length; i++)\n'
	result += '\t\tif (a[i] != b[i])\n'
	result += '\t\treturn 0;\n'
	result += '\treturn 1;\n'
	result += '}\n'
	result += '\n'

	result += 'int main(void) {\n'
	if 'tests' in program[target]:

		result += f'\tprintf("tests for {target}:\\n");\n'

		tests_number = len(program[target]['tests'])
		inputs_number = len(program[target]['tests'][0]['inputs'])
		outputs_number = len(program[target]['tests'][0]['outputs'])

		for s in ['inputs', 'outputs']:
			list_init_values_list = map(lambda i: f"{{{i}}}", [", ".join(map(str, t[s])) for t in program[target]['tests']])
			result += f'\tint tests_{s}[{tests_number}][{inputs_number if s == "inputs" else outputs_number}] = {{{", ".join(list_init_values_list)}}};\n'
		
		result += '\tint i;\n'
		result += '\tint *output;\n'
		result += f'\tfor (i = 0; i < {tests_number}; i++) {{\n'
		
		inputs_values_list = [f'tests_inputs[i][{j}]' for j in range(inputs_number)]
		outputs_values_list = [f'tests_outputs[i][{j}]' for j in range(outputs_number)]
		inputs_values_string = ", ".join(inputs_values_list)
		
		result += f'\t\toutput = {target}({inputs_values_string});\n'
		result += '\t\tprintf("[");\n'
		result += f'\t\tprintArray(tests_inputs[i], {inputs_number}, ", ");\n'
		result += '\t\tprintf("] => [");\n'
		result += f'\t\tprintArray(tests_outputs[i], {outputs_number}, ", ");\n'
		result += f'\t\tprintf("] %s\\n", isEqual(tests_outputs[i], output, {outputs_number}) ? "passed" : "failed");\n'
		result += '\t\tfree(output);\n'
		
		result += '\t}\n'
		result += '\treturn 0;\n'

	result += '}'

	result = find_inputs.sub(r'\1', result)

	return result