import sys
import os
from architest.model import Project
from architest.utils.colorprint import ColorPrint as color

VERSION_NUMBER = '0.1'

def print_fill(message: str, fill_char: str = '=', print_function=print):
	terminal_width = os.get_terminal_size().columns
	wing_width = round((terminal_width - len(message) - 4)/ 2) - 1
	wing = fill_char * wing_width
	print_function(wing + f'  {message}  ' + wing)
	print()


def search_violations(project: Project):
	project.read_project()
	project.search_violations()
	return project.violations


def generate_plant_uml(root: str):
	project = Project(root)
	project.read_project()

	print('@startuml')
	for module in project.modules.values():
		print(f'rectangle {module.path.path} [')
		print(f'  <b>{module.path.path}</b>')
		print(']')
		print()
	for rule in project.real_rules.rules:
		print(f'{rule.module_from.path.path} {rule.connection.uml} {rule.module_to.path.path}')
	print('@enduml')


def main(root: str):
	print()
	print_fill('Starting Architest', print_function=color.print_bold)
	print_fill('firmitatis · utilitatis · venustatis', ' ')
	print(f'version: {VERSION_NUMBER} · target project: {root}\n')
	
	file_path = root + '/' + '.architest.yml'
	if not os.path.exists(file_path):
		print_fill('No .architest.yml file found at project root', print_function=color.print_warn)
		sys.exit(1)
	
	print_fill('Searching for design violations', '-')
	
	project = Project(root)
	violations = search_violations(project)
	if len(violations) > 0:
		for violation in violations:
			print(violation.violation_error())
		print()
		print_fill(f'Found {len(violations)} violation{"" if len(violations) == 1 else "s"}', print_function=color.print_fail)
		sys.exit(1)
	else:
		print_fill(f'Design conforms to config', print_function=color.print_pass)	

	print()
	sys.exit(0)


if __name__ == '__main__':
	if sys.argv[1] in {'-d', '--draw'}:
		generate_plant_uml(sys.argv[2])
		sys.exit(0)
	main(sys.argv[1])
