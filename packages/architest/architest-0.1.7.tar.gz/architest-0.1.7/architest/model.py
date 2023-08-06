import enum
import os
from collections import defaultdict
from dataclasses import dataclass

import yaml

from architest.core import (find_dependencies, find_docstrings,
                            find_extensions, find_instantiations)


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

    @property
    def upper_module_name(self):
        if '.' in self.path:
            return self.path.split('.')[0]
        return self.path

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

    def __eq__(self, other):
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
    def docstrings(self):
        return find_docstrings(self.file_path)

    @property
    def imports(self):
        if len(self._imports) == 0:
            self._imports = {Path(*path_lineno)
                             for path_lineno in find_dependencies(self.file_path)}
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
                for name, lineno in find_instantiations(self.file_path) if name in self.local_paths}\
            .intersection(self.imports)

    @property
    def extensions(self):
        return {self.update_imported_module_info(self.local_paths[name], lineno)
                for name, lineno in find_extensions(self.file_path) if name in self.local_paths}\
            .intersection(self.imports)\
            .difference(self.aggregations)

    def __hash__(self) -> int:
        return hash(self.path.path)


@dataclass
class Rule:
    module_from: Module
    connection: Connection
    module_to: Module

    def _dependency_direction(self):
        return f'{self.module_from.path.path} {self.connection.uml} {self.module_to.path.path}'

    def _dependency_path(self):
        return f'{self.module_from.file_path}:{self.connection.lineno}'

    def violation_error(self):
        return f'Illegal {self.connection.name}\t{self._dependency_direction()} @ {self._dependency_path()}'

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
        self.is_package = False
        self.raw_rules = None
        self.real_rules = RuleSet()
        self.ignore = []
        self.violations = set()
        self.hidden_connections = []

    def read_config(self):
        file_path = self.root + '/' + '.architest.yml'
        if not os.path.exists(file_path):
            return
        with open(self.root + '/' + '.architest.yml', 'r') as config:
            try:
                self._read_config(config)
            except yaml.YAMLError as exc:
                print(exc)  # noqa: T001

    def _read_config(self, config):
        raw_rules = yaml.safe_load(config)
        self.ignore = raw_rules['ignore']
        self.hidden_connections = self.hidden_connections + raw_rules.get('hide_connections', [])
        self._code_root = raw_rules['code_root']
        self.is_package = raw_rules.get('is_package', False)
        self._code_root = '' if self._code_root is None else self._code_root
        self.raw_rules = RuleSet()

        self.raw_rules = raw_rules['modules']

    def _module_not_in_rules(self, module):
        return module not in \
            {rule.module_from for rule in self.real_rules.rules
            if rule.connection.name not in self.hidden_connections} | \
            {rule.module_to for rule in self.real_rules.rules
            if rule.connection.name not in self.hidden_connections}

    @property
    def modules_in_rules(self):
        return list(filter(lambda module: not self._module_not_in_rules(module), self.modules.values()))

    def _filter_files(self, files):
        return list(filter(lambda file: file.endswith('.py') and not file.startswith('__'), files))

    def _convert_path_to_module_path(self, path: str) -> str:
        return '.'.join(module.replace('.py', '') for module in path.split(os.sep)
                        if module not in self.root.split(os.sep))

    def _full_path_to_module(self, path: str, filename: str) -> str:
        return path + '/' + filename

    @property
    def code_root(self):
        if self._code_root == '':
            self.read_config()
        return self._code_root

    def _is_ignored(self, module_path: str):
        return any(map(lambda ignored: ignored in module_path, self.ignore))

    # TODO: Split into less complex chunks
    @property
    def modules(self):  # noqa: C901
        if self._modules:
            return self._modules
        for subdir, _, files in os.walk(self.root):
            files = self._filter_files(files)
            if len(files) == 0:
                continue
            for file in files:

                full_path = self._full_path_to_module(subdir, file)
                module_path = self._convert_path_to_module_path(full_path)
                if not module_path.startswith(self.code_root) or self._is_ignored(module_path):
                    continue

                if not self.is_package and self.code_root:
                    module_path = module_path.replace(self.code_root + '.', '')

                self._modules[module_path] = Module(full_path, module_path)

        return self._modules

    def _add_rules(self, module_from: Module, connection_paths: set[Path], connection_type: ConnectionType):
        for dependency in connection_paths:
            if dependency.module_path not in self.modules:
                continue
            connection = Connection(connection_type.value.uml,
                                    connection_type.value.name, dependency.lineno)
            self.real_rules.add(module_from, self.modules[dependency.module_path], connection)

    def read_project(self):
        self.read_config()

        for module in self.modules.values():
            self._add_rules(module, module.dependencies, ConnectionType.DEPENDENCY)
            self._add_rules(module, module.aggregations, ConnectionType.AGGREGATION)
            self._add_rules(module, module.extensions, ConnectionType.EXTENSION)

        self._filter_connection_priority()

    # TODO: Redo as set functionality
    def _filter_connection_priority(self):  # noqa: C901
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
            self._check_rule_against_config(rule)

    def _check_rule_against_config(self, rule: Rule):
        if rule.module_from.path.path not in self.raw_rules.keys():
            self.violations.add(rule)
            return
        for module_path, constraints in self.raw_rules.items():
            if not self._is_inside_path(rule.module_from, module_path):
                continue
            self._check_rule_conformance_to_constraints(rule, constraints)

    def _check_rule_conformance_to_constraints(self, rule, constraints):
        if rule.connection.name not in constraints:
            self.violations.add(rule)
            return
        for constraint, target_modules in constraints.items():
            if not target_modules:
                self._handle_possible_violation(rule, constraint)
                continue
            self._search_non_conformant_rules(rule, target_modules, constraint)

    def _search_non_conformant_rules(self, rule, target_modules, constraint):
        for target_module in target_modules:
            if self._is_inside_path(rule.module_to, target_module) or \
                    self._is_module_specified_in_config(rule.module_to, target_modules):
                continue
            self._handle_possible_violation(rule, constraint)

    def _is_inside_path(self, module, path):
        return module.path.path.startswith(path)

    def _is_module_specified_in_config(self, module: Module, all_target_modules: list[str]):
        return any(map(lambda target: self._is_inside_path(module, target), all_target_modules))

    def _handle_possible_violation(self, rule, constraint):
        if rule.connection.name == constraint:
            self.violations.add(rule)
