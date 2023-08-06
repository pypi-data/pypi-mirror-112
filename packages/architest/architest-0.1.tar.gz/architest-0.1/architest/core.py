import sys
import ast
import itertools


def get_plain_imports(body):
	imports = [[(name.name, obj.lineno) for name in obj.names] for obj in body if isinstance(obj, ast.Import)]
	return list(itertools.chain.from_iterable(imports))


def get_imports_from(body):
	imports = [[(obj.module + '.' + name.name, obj.lineno) for name in obj.names] for obj in body if isinstance(obj, ast.ImportFrom)]
	# imports = [[(obj.module, obj.lineno) for name in obj.names] for obj in body if isinstance(obj, ast.ImportFrom)]
	# print('imports', imports)
	return list(itertools.chain.from_iterable(imports))


def get_calls(body):
	calls = [obj.func.id for obj in body if isinstance(obj, ast.Call)]


def find_dependencies(filename: str):
	with open(filename) as f:
		data = f.read()
		module = ast.parse(data)
		return get_plain_imports(module.body) + get_imports_from(module.body)

def find_in_class_calls(filename: str):
	with open(filename) as f:
		data = f.read()
		module = ast.parse(data)
		classes = [
			obj
			for obj in module.body
			if isinstance(obj, ast.ClassDef)
		]
		class_names = [obj.name for obj in classes]
		return [
		    (node.func.id, node.func.lineno) for node in ast.walk(module)
		    if (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
		         and node.func.id not in class_names)
		]
		

def find_instantiations(filename: str):
	with open(filename) as f:
		data = f.read()
		module = ast.parse(data)
		classes = [
			obj
			for obj in module.body
			if isinstance(obj, ast.ClassDef)
		]
		class_names = [obj.name for obj in classes]
		return [
		    (node.value.func.id, node.value.func.lineno) for node in ast.walk(module)
		    if (isinstance(node, ast.Assign) and isinstance(node.value, ast.Call)
		        and isinstance(node.value.func, ast.Name) and node.value.func.id[0].
		        isupper() and node.value.func.id not in class_names)
		]

def get_constants_in_base(base):
	if isinstance(base, ast.Subscript):
		if isinstance(base.slice, ast.Name):
			return {(base.slice.id, base.lineno)}
		return {(element.id, element.lineno) for element in base.slice.elts}
	elif isinstance(base, ast.Attribute):
		return {(base.value.id, base.lineno)}
	return {(base.id, base.lineno)}


def find_extensions(filename: str) -> list[str]:
	with open(filename) as f:
		data = f.read()
		module = ast.parse(data)
		classes = [
			obj
			for obj in module.body
			if isinstance(obj, ast.ClassDef)
		]
		class_names = [obj.name for obj in classes]
		extensions = []
		for _class in classes:
			extensions += [get_constants_in_base(base) for base in _class.bases]

		return {(name, lineno)
		        for name, lineno in itertools.chain.from_iterable(extensions)
		        if name not in class_names}


if __name__ == '__main__':
	filename = sys.argv[1]
	find_dependencies(filename)