from . import compileLogicScheme

import argparse



parser = argparse.ArgumentParser(description='Compile logic schemes JSON representations to C file')
parser.add_argument('-i', '--input', type=str,
					required=True,
					help='Path to file with target function', default=None)
parser.add_argument('-t', '--target', type=str,
					help='Name of function to compile', default='MAIN')
parser.add_argument('-l', '--link', type=str, nargs='*',
					required=True,
					help='Paths to (input files) / (directories containing input files) with required functions descriptions', default=None)
parser.add_argument('-o', '--output', type=str,
					required=True,
					help='Path to output file', default=None)
args = parser.parse_args()

input_path = args.input
target_function_name = args.target
linked_paths = args.link
output_path = args.output


compileLogicScheme(input_path, target_function_name, linked_paths, output_path)