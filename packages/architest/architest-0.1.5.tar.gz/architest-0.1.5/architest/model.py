import os
import enum
from collections import defaultdict
from dataclasses import dataclass
from architest.core import find_dependencies, find_extensions, find_instantiations
import yaml

@dataclass
class Connection:
    uml: str
    name: str
    lineno: int = 1

    def __hash__(self) -> int:
        return hash(self.name)


class ConnectionType(enum.Enum):
    DEPENDENCY = Connection(uml='..>', name='dependency')
    AGGREGATION = Connection(uml='--o', name='aggregation')
    ASSOCIATION = Connection(uml='-->', name='association')
    COMPOSITION = Connection(uml='--*', name='composition')
    IMPLEMENTATION = Connection(uml='..|>', name='implementation')
    EXTENSION = Connection(uml='--|>', name='extension')

mapping = {
    'dependency': ConnectionType.DEPENDENCY.value,
    'aggregation': ConnectionType.AGGREGATION.value,
    'assoctiation': ConnectionType.ASSOCIATION.value,
    'composition': ConnectionType.COMPOSITION.value,
    'implementation': ConnectionType.IMPLEMENTATION.value,
    'extension': ConnectionType.EXTENSION.value
}
    

def convert_connection_name_to_class(name: str) -> Connection:
    return mapping[name]


@dataclass
class Path:
    path: str
    lineno: int = 1

    # @property
    # def path_split(self):
    # 	return [module.replace('.py', '') for module in self.path.split(os.sep) if module != '..']

    # @property
    # def python_path(self):
    # 	return '.'.join(self.path_split)

    @property
    def python_name(self):
        return self.path.split('.')[-1]

    @property
    def module_path(self):
        if '.' in self.path:
            return self.path[:self.path.rfind('.')]
        return self.path

    def __repr__(self) -> str:
        return repr(f'{self.path}:{self.lineno}')

    def __hash__(self) -> int:
        return hash(self.path)
    
    def __eq__(self,other):
        if isinstance(other, self.__class__):
            return self.path == other.path
        else:
            return NotImplemented


class Module:
    def __init__(self, file_path, module_path) -> None:
        self.path: Path = Path(module_path)
        self.name = self.path.python_name
        self.file_path = file_path
        self.connections = defaultdict(set)
        self._imports = {}
        self._local_paths = {}

    @property
    def id(self):
        return self.path + self.name

    def full_path(self):
        return f'{self.path}.{self.name}'

    def update_imported_module_info(self, path: Path, lineno: int):
        return Path(path.path, lineno)

    @property
    def imports(self):
        if len(self._imports) == 0:
            self._imports = {Path(*path_lineno) for path_lineno in find_dependencies(self.file_path)}
            self._local_paths = {path.python_name: path for path in self._imports}
        return self._imports

    @property
    def local_paths(self) -> dict[str, Path]:
        if not self._local_paths:
            self.imports
        return self._local_paths

    @property
    def dependencies(self):
        return self.imports.difference(self.aggregations)

    @property
    def aggregations(self) -> set[Path]:
        return {self.update_imported_module_info(self.local_paths[name], lineno) 
                for name, lineno in find_instantiations(self.file_path)}\
                    .intersection(self.imports)

    @property
    def extensions(self):
        return {self.update_imported_module_info(self.local_paths[name], lineno)
                for name, lineno in find_extensions(self.file_path)}\
                    .intersection(self.imports)\
                    .difference(self.aggregations)
    
    def __hash__(self) -> int:
        return hash(self.module_path)


@dataclass
class Rule:
    module_from: Module
    connection: Connection
    module_to: Module
    
    def violation_error(self):
        return f'Illegal {self.connection.name}\t{self.module_from.name} {self.connection.uml} {self.module_to.name} @ {self.module_from.file_path}:{self.connection.lineno} '

    def __hash__(self) -> int:
        return hash(self.module_from.path.path + self.connection.uml + self.module_to.path.path)

    def __eq__(self, other) -> bool:
        return other.module_from.path.path == self.module_from.path.path\
            and self.module_to.path.path == other.module_to.path.path\
            and self.connection.uml == other.connection.uml


class RuleSet:
    rules: set[Rule] = set()

    def add(self, module_from: Module, module_to: Module, connection: Connection):
        self.rules.add(Rule(module_from=module_from, module_to=module_to, connection=connection))

    def drop(self, rule: Rule):
        self.rules.remove(rule)


class Project:
    def __init__(self, root: str) -> None:
        self._modules = {}
        self.root: str = root
        self._code_root = ''
        self.settled_rules = None
        self.real_rules = RuleSet()
        self.ignore = []
        self.violations = set()

    def build_connections_from_config(self, module):
        parsed_connections = set()
        module_from_path = self.code_root + '.' + module['name']
        module_from = Module(self.find_module_path(module_from_path), module_from_path.split('.')[-1], module_from_path)
        connections = {key: value for key, value in module.items() if key != 'name'}
        # print('CONNECTIONS:', connections)
        for connection_type, target_modules in connections.items():
            if not target_modules:
                continue
            for target_module in target_modules:
                # print(target_module, connection_type)
                # print(self.find_module_path(self.code_root + '.' + target_module))
                module_to = Module(self.find_module_path(self.code_root + '.' + target_module), self.code_root + '.' + target_module)
                self._modules.setdefault(self.code_root + '.' + target_module, module_to)
                self.settled_rules.add(module_from, module_to, convert_connection_name_to_class(connection_type))

    def read_config(self):
        file_path = self.root + '/' + '.architest.yml'
        if not os.path.exists(file_path):
            return
        with open(self.root + '/' + '.architest.yml', 'r') as config:
            try:
                self._read_config(config)
            except yaml.YAMLError as exc:
                print(exc)

    def _read_config(self, config):
        raw_rules = yaml.safe_load(config)
        self.ignore = raw_rules['ignore']
        self._code_root = raw_rules['code_root']
        self.settled_rules = RuleSet()

        self.settled_rules = raw_rules['modules']


    def find_module_path(self, module):
        pure_root_path = self.root.split(os.sep)
        start_node = pure_root_path[-1]
        if start_node not in module:
            return None
        module_path:list = module.split('.')
        module_path = module_path[module_path.index(start_node)+2:]
        return '/'.join(pure_root_path + module_path) + '.py'

    def _filter_files(self, files):
        return list(filter(lambda file: file.endswith('.py') and not file.startswith('__'), files))

    def _convert_path_to_module_path(self, path: str) -> str:
        return '.'.join(module.replace('.py', '') for module in path.split(os.sep) if module not in self.root.split(os.sep) and module != self.code_root)

    def _full_path_to_module(self, path: str, filename: str) -> str:
        return path + '/' + filename

    @property
    def code_root(self):
        if self._code_root == '':
            self.read_config()
        return self._code_root

    @property
    def modules(self):
        if self._modules:
            return self._modules
        for subdir, _, files in os.walk(self.root):	
            files = self._filter_files(files)
            if len(files) == 0: continue
            for file in files:
                full_path = self._full_path_to_module(subdir, file)
                module_path = self._convert_path_to_module_path(full_path)
                self._modules[module_path] = Module(full_path, module_path)

        return self._modules

    def _add_rules(self, module_from: Module, connection_paths: set[Path], connection_type: ConnectionType):
        for dependency in connection_paths:
            if dependency.module_path not in self.modules:
                continue
            connection = Connection(connection_type.value.uml, connection_type.value.name, dependency.lineno)
            self.real_rules.add(module_from, self.modules[dependency.module_path], connection) 

    def read_project(self):
        self.read_config()

        for module in self.modules.values():
            self._add_rules(module, module.dependencies, ConnectionType.DEPENDENCY)
            self._add_rules(module, module.aggregations, ConnectionType.AGGREGATION)
            self._add_rules(module, module.extensions, ConnectionType.EXTENSION)

        self._filter_connection_priority()

    # TODO: Redo as set functionality
    def _filter_connection_priority(self):
        priority_line = ['aggregation', 'extension', 'dependency']
        connections = {key: set() for key in priority_line}
        for rule in self.real_rules.rules:
            connections[rule.connection.name].add(rule)
        
        for i in range(len(priority_line) - 1):
            current_connection = priority_line[i]  # aggregation
            lower_connections = priority_line[i + 1:]  # extension, dependency
            for rule in connections[current_connection]:
                for lower_connection in lower_connections:
                    for lower_rule in connections[lower_connection]:
                        if lower_rule not in self.real_rules.rules:
                            continue
                        if rule.module_from == lower_rule.module_from and rule.module_to == lower_rule.module_to:
                            self.real_rules.drop(lower_rule)

    def search_violations(self):
        for rule in self.real_rules.rules:
            for module_path, constraints in self.settled_rules.items():
                if not rule.module_from.path.path.startswith(module_path):
                    continue
                for constraint, target_modules in constraints.items():
                    for target_module in target_modules:
                        if rule.module_to.path.path.startswith(target_module) or\
                             any(map(lambda target: rule.module_to.path.path.startswith(target), target_modules)):
                            continue
                        if rule.connection.name == constraint:
                            self.violations.add(rule)