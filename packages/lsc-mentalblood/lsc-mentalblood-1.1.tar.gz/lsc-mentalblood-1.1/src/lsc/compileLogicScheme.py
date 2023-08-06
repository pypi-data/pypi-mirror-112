import os
import json

from . import core



def joinPrograms(subpaths, root='.'):
	
	result = {}
	
	for sp in subpaths:
	
		p = os.path.join(root, sp)
	
		if not os.path.exists(p):
			print(f'No file/dir on path: {p}, skiping')
	
		elif os.path.isdir(p):
	
			dir_content = list(filter(
				lambda p: p.endswith('.json') or os.path.isdir(p),
				os.listdir(p)
			))
	
			if len(dir_content) > 0:
				result = {**result, **joinPrograms(dir_content, root=p)}
	
		else:
	
			with open(p) as f:
				result = {**result, **json.load(f)}
	
	return result


def unique(l):
	result = []
	for item in l:
		if not item in result:
			result.append(item)
	return result


def getNonstandardRequirements(
	target_function_name,
	target_function_description,
	available_functions_descriptions
):
	
	direct_requirements = core.getElementsTypes(target_function_description)
	
	direct_nonstandard_requirements = list(filter(
		lambda e: not (e in core.standard_elements),
		direct_requirements
	))
	
	indirect_nonstandard_requirements = []
	
	for d_r in direct_nonstandard_requirements:
	
		if not (d_r in available_functions_descriptions):
			raise Exception(f'Compile error: {target_function_name} requires {d_r}, but it is not presented')
	
		d_r_description = available_functions_descriptions[d_r]
		d_r_nonstandard_requirements = getNonstandardRequirements(
			d_r,
			d_r_description,
			available_functions_descriptions
		)
	
		indirect_nonstandard_requirements += d_r_nonstandard_requirements
	
	return unique(direct_nonstandard_requirements + indirect_nonstandard_requirements)


def compileLogicScheme(input_path, target_function_name, linked_paths, output_path):

	available_functions_descriptions = joinPrograms([input_path] + linked_paths)
	del available_functions_descriptions[target_function_name]
	
	with open(input_path) as f:
		target_function_description = json.load(f)[target_function_name]

	requirements = getNonstandardRequirements(
		target_function_name,
		target_function_description,
		available_functions_descriptions
	)
	requirements.reverse()
	
	functions_descriptions = {
		**{
			r_name: available_functions_descriptions[r_name]
			for r_name in requirements
		}, **{
			target_function_name: target_function_description
		}
	}

	compiled_program = core.compile(functions_descriptions, target_function_name, requirements)

	with open(output_path, 'w') as f:
		f.write(compiled_program)



import sys
sys.modules[__name__] = compileLogicScheme