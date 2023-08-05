import ast
import importlib
import inspect
import logging
import os.path
import pkgutil


def number_callable_params(callable):
	"""
	Número de parámetros de una función o callable.
	:param callable: objeto que puede ser invocado
	:return:
	"""
	return len(inspect.signature(callable).parameters)


def function_has_return(callable):
	"""
	Devuelve True si la función tiene sentencia return, False en caso contrario.
	No funciona con funciones cuyo código no esté escrito en Python.
	:param callable:
	:return:
	"""
	return any(isinstance(node, ast.Return) for node in ast.walk(ast.parse(inspect.getsource(callable))))


def import_dir_classes(dir_path, base_class, recursive=True):
	"""
	Importar las clases de los scripts que estén en un directorio.
	:param dir_path: directorio de los scripts.
	:param base_class: clase base de las clases que se desean importar.
	:param recursive: si se desea buscar también en los subdirectorios.
	:return:
	"""
	classes = set()

	rel = os.path.relpath(dir_path)
	rel_stripped = rel.strip('./\\')
	absolute = os.path.abspath(dir_path)

	if '.' in absolute:
		logging.warning(f"Can't import modules from a directory with dot/s in it's path: {absolute}.")
		return classes

	module_dir = rel_stripped.replace('/', '.').replace('\\', '.')
	for (modinfo, name, ispkg) in pkgutil.iter_modules([dir_path]):
		module = f'{module_dir}.{name}'
		mod_classes = _import_module_classes(module, base_class)
		classes = classes.union(mod_classes)

	if recursive:
		for d in os.listdir(dir_path):
			subdir = os.path.join(dir_path, d)
			if os.path.isdir(subdir) and not subdir.endswith('__pycache__'):
				mod_classes = import_dir_classes(subdir, base_class, recursive)
				classes = classes.union(mod_classes)
	return classes


def _import_module_classes(module, base_class):
	"""
	Importar las clases de un módulo que hereden de una clase específica.
	:param module: dirección del módulo en string. e.g. mymodule.functions
	:param base_class: clase base de las clases que se desean importar.
	:return:
	"""
	imported_module = importlib.import_module(module)

	classes = set()
	for i in dir(imported_module):
		attribute = getattr(imported_module, i)
		if inspect.isclass(attribute)\
				and not inspect.isabstract(attribute)\
				and issubclass(attribute, base_class)\
				and attribute != base_class\
				and not issubclass(attribute, NotImport):
			classes.add(attribute)

	return classes


def next_class_in_mro(instance_class: type, current_class: type) -> type:
	mro = instance_class.__mro__
	for i, clazz in enumerate(mro):
		if clazz == current_class:
			if i < len(mro) - 1:
				return mro[i + 1]
	return None


def exist_method_in_parent_classes(instance: object, current_class: type, method_name: str) -> bool:
	instance_class = instance.__class__
	mro = instance_class.__mro__
	for i, clazz in enumerate(mro):
		if clazz == current_class:
			next_classes = mro[i + 1:]
			for next_class in next_classes:
				if method_name in dir(next_class):
					return True
	return False


class NotImport:
	"""
	Esta clase es solo para "marcar" otras clases como no importables. Es decir, las clases que hereden de NotImport
	no serán importadas de manera dinámica por el método import_module_classes.
	"""

	@staticmethod
	def notimport(clazz):
		"""
		Este método funciona como decorador de clases para añadir a NotImport como clase base a una clase.

		Uso:

		@notimport
		class A(object):
			pass

		:param clazz:
		:return:
		"""
		if inspect.isclass(clazz):
			clazz.__bases__ += (NotImport, )
		return clazz
